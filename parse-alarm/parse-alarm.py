#!/usr/bin/env python3

import json
import argparse
import sys
from pathlib import Path

# PDF (reportlab)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


# -----------------------
# ENUM MAPS
# -----------------------

CONDITION_MAP = {
    0: "==",
    1: ">",
    2: "<",
    3: ">=",
    4: "<=",
    5: "!=",
}

SOURCE_MAP = {
    0: "BT",
    1: "ET",
    2: "ΔBT",
    3: "ΔET",
    4: "Time",
    5: "Event",
}

ACTION_MAP = {
    0: "None",
    1: "Beep",
    2: "Command",
    3: "Slider",
    4: "Mark",
    5: "Message",
}

GUARD_MAP = {
    1 << 0: "CHARGE",
    1 << 1: "DRY",
    1 << 2: "FC_START",
    1 << 3: "FC_END",
    1 << 4: "SC_START",
    1 << 5: "SC_END",
    1 << 6: "DROP",
}


def decode(mapping, value):
    return mapping.get(value, f"unknown({value})")


def decode_guard(mask):
    if mask == 0:
        return ["ANY"]
    out = [name for bit, name in GUARD_MAP.items() if mask & bit]
    return out or [f"unknown({mask})"]


# -----------------------
# TIME INTERPRETATION
# -----------------------

def fmt_time(sec):
    if sec < 0:
        return None
    m = int(sec) // 60
    s = int(sec) % 60
    return f"{m:02d}:{s:02d}"


def interpret_time_offset(a):
    t = a["time"]
    offset = a["offset"]
    phases = a["guard_labels"]

    if offset > 0:
        ref = phases[0] if phases and phases[0] != "ANY" else "event"
        return f"{fmt_time(offset)} after {ref}"

    if t > 0:
        return f"at {fmt_time(t)}"

    return None


# -----------------------
# TRIGGER SENTENCE
# -----------------------

def build_trigger_sentence(a):
    src = a["source_label"]
    cond = a["condition_label"]
    temp = a["temperature"]

    guard = a["guard_labels"]
    neg_guard = a["neg_guard_labels"]

    parts = []

    # condition
    if src == "Time":
        parts.append(f"time {cond} {temp}")
    else:
        parts.append(f"{src} {cond} {temp}")

    # time
    tpart = interpret_time_offset(a)
    if tpart:
        parts.append(tpart)

    # guard include
    if guard != ["ANY"]:
        parts.append(f"during {'/'.join(guard)}")

    # guard exclude
    if a["neg_guard"] != 0:
        parts.append(f"not during {'/'.join(neg_guard)}")

    sentence = "Trigger when " + ", ".join(parts)

    if a["action_label"] != "None":
        sentence += f" → {a['action_label']}"

    if a["beep"]:
        sentence += " + beep"

    return sentence


# -----------------------
# MODEL
# -----------------------

def load_alarm_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_model(raw):
    length = len(raw["alarmstrings"])
    alarms = []

    for i in range(length):
        cond = raw["alarmconds"][i]
        src = raw["alarmsources"][i]
        act = raw["alarmactions"][i]

        alarm = {
            "index": i,
            "enabled": bool(raw["alarmflags"][i]),
            "time": raw["alarmtimes"][i],
            "offset": raw["alarmoffsets"][i],
            "temperature": raw["alarmtemperatures"][i],
            "condition": cond,
            "condition_label": decode(CONDITION_MAP, cond),
            "source": src,
            "source_label": decode(SOURCE_MAP, src),
            "action": act,
            "action_label": decode(ACTION_MAP, act),
            "beep": bool(raw["alarmbeep"][i]),
            "label": raw["alarmstrings"][i],
            "guard": raw["alarmguards"][i],
            "guard_labels": decode_guard(raw["alarmguards"][i]),
            "neg_guard": raw["alarmnegguards"][i],
            "neg_guard_labels": decode_guard(raw["alarmnegguards"][i]),
        }

        alarm["trigger"] = build_trigger_sentence(alarm)
        alarms.append(alarm)

    return {"count": length, "alarms": alarms}


# -----------------------
# OUTPUTS
# -----------------------

def output_json(model):
    print(json.dumps(model, indent=2))


def output_text(model):
    for a in model["alarms"]:
        print(f"[{a['index']}] {a['label']}")
        print(f"  {a['trigger']}")
        print("")


def output_markdown(model):
    print("| idx | en | trigger |")
    print("|-----|----|---------|")
    for a in model["alarms"]:
        print(f"| {a['index']} | {'Y' if a['enabled'] else 'N'} | {a['trigger']} |")


def output_ascii(model):
    headers = ["idx", "en", "trigger"]
    rows = []

    for a in model["alarms"]:
        rows.append([
            str(a["index"]),
            "Y" if a["enabled"] else "N",
            a["trigger"],
        ])

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, v in enumerate(row):
            col_widths[i] = max(col_widths[i], len(v))

    def fmt(row):
        return "  ".join(v.ljust(col_widths[i]) for i, v in enumerate(row))

    print(fmt(headers))
    print("  ".join("-" * w for w in col_widths))

    for r in rows:
        print(fmt(r))


def output_pdf(model, path):
    doc = SimpleDocTemplate(path, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Artisan Alarm Summary", styles["Title"]))
    elements.append(Spacer(1, 12))

    data = [["idx", "enabled", "trigger"]]

    for a in model["alarms"]:
        data.append([
            a["index"],
            "Y" if a["enabled"] else "N",
            a["trigger"],
        ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))

    elements.append(table)
    doc.build(elements)

    print(f"PDF written to: {path}")


# -----------------------
# MAIN
# -----------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument(
        "--format",
        choices=["json", "text", "markdown", "ascii", "pdf"],
        default="json",
    )
    parser.add_argument("--output")

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print("file not found", file=sys.stderr)
        sys.exit(1)

    model = build_model(load_alarm_file(path))

    if args.format == "json":
        output_json(model)
    elif args.format == "text":
        output_text(model)
    elif args.format == "markdown":
        output_markdown(model)
    elif args.format == "ascii":
        output_ascii(model)
    elif args.format == "pdf":
        if not args.output:
            print("pdf requires --output file.pdf", file=sys.stderr)
            sys.exit(1)
        output_pdf(model, args.output)


if __name__ == "__main__":
    main()
