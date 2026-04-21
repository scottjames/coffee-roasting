#!/usr/bin/env python3

import json
import argparse
import sys
from pathlib import Path

# PDF imports (reportlab)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


def load_alarm_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_model(raw):
    length = len(raw["alarmstrings"])
    alarms = []

    for i in range(length):
        alarms.append({
            "index": i,
            "enabled": bool(raw["alarmflags"][i]),
            "guard": raw["alarmguards"][i],
            "neg_guard": raw["alarmnegguards"][i],
            "time": raw["alarmtimes"][i],
            "offset": raw["alarmoffsets"][i],
            "condition": raw["alarmconds"][i],
            "source": raw["alarmsources"][i],
            "temperature": raw["alarmtemperatures"][i],
            "action": raw["alarmactions"][i],
            "beep": bool(raw["alarmbeep"][i]),
            "label": raw["alarmstrings"][i],
        })

    return {"count": length, "alarms": alarms}


# -----------------------
# OUTPUT FORMATS
# -----------------------

def output_json(model):
    print(json.dumps(model, indent=2))


def output_text(model):
    for a in model["alarms"]:
        print(f"[{a['index']}] {a['label']}")
        print(f"  enabled: {a['enabled']}")
        print(f"  time: {a['time']} offset: {a['offset']}")
        print(f"  temp: {a['temperature']}")
        print(f"  action: {a['action']} beep: {a['beep']}")
        print("")


def output_markdown(model):
    print("| idx | enabled | time | offset | temp | action | beep | label |")
    print("|-----|--------|------|--------|------|--------|------|-------|")

    for a in model["alarms"]:
        print(
            f"| {a['index']} | {a['enabled']} | {a['time']} | "
            f"{a['offset']} | {a['temperature']} | {a['action']} | "
            f"{a['beep']} | {a['label']} |"
        )


def output_ascii(model):
    headers = ["idx", "enabled", "time", "offset", "temp", "action", "beep", "label"]

    rows = []
    for a in model["alarms"]:
        rows.append([
            str(a["index"]),
            str(a["enabled"]),
            str(a["time"]),
            str(a["offset"]),
            str(a["temperature"]),
            str(a["action"]),
            str(a["beep"]),
            a["label"],
        ])

    # compute column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(val))

    def format_row(row):
        return "  ".join(val.ljust(col_widths[i]) for i, val in enumerate(row))

    print(format_row(headers))
    print("  ".join("-" * w for w in col_widths))

    for row in rows:
        print(format_row(row))


def output_pdf(model, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph("Artisan Alarm Configuration", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    headers = ["idx", "enabled", "time", "offset", "temp", "action", "beep", "label"]

    data = [headers]
    for a in model["alarms"]:
        data.append([
            a["index"],
            str(a["enabled"]),
            a["time"],
            a["offset"],
            a["temperature"],
            a["action"],
            str(a["beep"]),
            a["label"],
        ])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

        ("ALIGN", (0, 0), (-2, -1), "CENTER"),
        ("ALIGN", (-1, 1), (-1, -1), "LEFT"),
    ]))

    elements.append(table)

    doc.build(elements)
    print(f"PDF written to: {output_path}")


# -----------------------
# MAIN
# -----------------------

def main():
    parser = argparse.ArgumentParser(description="Parse Artisan .alrm file")
    parser.add_argument("file", help="Path to .alrm file")
    parser.add_argument(
        "--format",
        choices=["json", "text", "markdown", "ascii", "pdf"],
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--output",
        help="Output file (required for pdf)"
    )

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    raw = load_alarm_file(path)
    model = build_model(raw)

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
            print("PDF output requires --output <file.pdf>", file=sys.stderr)
            sys.exit(1)
        output_pdf(model, args.output)


if __name__ == "__main__":
    main()
