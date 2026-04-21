#!/usr/bin/env python3

import json
import argparse
import sys
from pathlib import Path


def load_alarm_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_model(raw):
    keys = [
        "alarmflags",
        "alarmguards",
        "alarmnegguards",
        "alarmtimes",
        "alarmoffsets",
        "alarmconds",
        "alarmsources",
        "alarmtemperatures",
        "alarmactions",
        "alarmbeep",
        "alarmstrings",
    ]

    length = len(raw["alarmstrings"])
    alarms = []

    for i in range(length):
        alarm = {
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
        }
        alarms.append(alarm)

    return {"count": length, "alarms": alarms}


def output_json(model):
    print(json.dumps(model, indent=2))


def output_text(model):
    for a in model["alarms"]:
        print(f"[{a['index']}] {a['label']}")
        print(f"  enabled: {a['enabled']}")
        print(f"  time: {a['time']}  offset: {a['offset']}")
        print(f"  temp: {a['temperature']}")
        print(f"  action: {a['action']}  beep: {a['beep']}")
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


def main():
    parser = argparse.ArgumentParser(description="Parse Artisan .alrm file")
    parser.add_argument("file", help="Path to .alrm file")
    parser.add_argument(
        "--format",
        choices=["json", "text", "markdown"],
        default="json",
        help="Output format",
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


if __name__ == "__main__":
    main()
