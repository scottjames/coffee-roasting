#!/usr/bin/env python3
"""
alrm_parser.py — Artisan Scope alarm file parser & formatter

Usage:
    python alrm_parser.py <file.alrm> [--format md|json|text|ascii|pdf] [--explain]

Arguments:
    file.alrm           Path to an Artisan .alrm file
    --format            Output format (default: text)
    --explain           Add human-readable trigger sentence to each alarm
    --output            Output file path (for pdf/md/json; default: stdout or auto-named)
"""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────
#  ENUM DECODERS
# ─────────────────────────────────────────────

ALARM_COND = {
    0: "falling",
    1: "below",
    2: "above",
}

# alarmtimes: -1 = absolute time, else = phase index
ALARM_TIME_PHASES = {
    -1: "CHARGE",   # "FROM_TIME" — absolute offset from start
     0: "CHARGE",
     1: "DRY END",
     2: "FC START",
     3: "FC END",
     4: "SC START",
     5: "SC END",
     6: "DROP",
     7: "COOL END",
     8: "TP",        # Turning Point
}

# alarmsources
ALARM_SOURCE = {
    -3: "Time",
    -2: "DeltaBT",
    -1: "DeltaET",
     0: "ET",
     1: "BT",
     2: "Extra1",
     3: "Extra2",
}

# alarmactions
ALARM_ACTION = {
    0:  "Pop-up message",
    1:  "Call program",
    2:  "Set SV bottom",
    3:  "Set Fan",   # TC4 (documented duplicate in artisan source)
    4:  "Set SV",
    5:  "Start timer",
    6:  "Set Burner", # TC4
    7:  "Set drum speed / event",
    8:  "Set damper / event",
    9:  "Set burner / event",
    10: "Set SV2",
    11: "Set heater",
    12: "Set fan",
    13: "Set drum",
    14: "Set damper",
}

# Guard phases (alarmguards / alarmnegguards): same index as alarmtimes
GUARD_PHASES = ALARM_TIME_PHASES


def decode_source(v: int) -> str:
    return ALARM_SOURCE.get(v, f"Source({v})")

def decode_cond(v: int) -> str:
    return ALARM_COND.get(v, f"Cond({v})")

def decode_action(v: int) -> str:
    return ALARM_ACTION.get(v, f"Action({v})")

def decode_phase(v: int) -> str:
    return ALARM_TIME_PHASES.get(v, f"Phase({v})")

def decode_guard(v: int) -> str:
    if v == -1:
        return "—"
    return GUARD_PHASES.get(v, f"Guard({v})")

def fmt_time(seconds: int) -> str:
    """Format seconds as mm:ss."""
    if seconds < 0:
        return "--:--"
    m, s = divmod(abs(seconds), 60)
    sign = "-" if seconds < 0 else ""
    return f"{sign}{m:02d}:{s:02d}"


# ─────────────────────────────────────────────
#  DATA MODEL
# ─────────────────────────────────────────────

@dataclass
class Alarm:
    index: int
    enabled: bool
    guard: str           # decoded phase guard (must be active)
    neg_guard: str       # decoded phase neg-guard (must NOT be active)
    phase: str           # decoded trigger phase
    offset_sec: int      # offset in seconds within that phase
    cond: str            # above / below / falling
    source: str          # BT, ET, Time, etc.
    temperature: float   # threshold temperature (0 = n/a for time-based)
    action: str          # decoded action
    beep: bool
    label: str           # user string / notes

    # ── derived ──
    trigger_summary: str = field(default="", init=False)

    def build_trigger_summary(self):
        """Build a plain-English trigger sentence."""
        parts = []

        # Phase context
        if self.phase == "CHARGE":
            parts.append(f"At {fmt_time(self.offset_sec)} from Charge")
        else:
            parts.append(f"{fmt_time(self.offset_sec)} after {self.phase}")

        # Source & condition
        if self.source == "Time":
            parts.append("(time-based trigger)")
        else:
            cond_word = {"above": "exceeds", "below": "drops below", "falling": "is falling"}.get(self.cond, self.cond)
            if self.temperature > 0:
                parts.append(f"when {self.source} {cond_word} {self.temperature:.0f}°")
            else:
                parts.append(f"when {self.source} {cond_word} threshold")

        # Guard
        if self.guard != "—":
            parts.append(f"[only during {self.guard} phase]")
        if self.neg_guard != "—":
            parts.append(f"[not during {self.neg_guard} phase]")

        # Action
        parts.append(f"→ {self.action}")

        # Beep
        if self.beep:
            parts.append("🔔")

        self.trigger_summary = " ".join(parts)


# ─────────────────────────────────────────────
#  PARSER
# ─────────────────────────────────────────────

def parse_alrm(path: str) -> list[Alarm]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    n = len(raw["alarmflags"])
    alarms = []

    for i in range(n):
        offset_raw = raw["alarmoffsets"][i]
        # Artisan stores offsets in seconds
        offset_sec = int(offset_raw)

        a = Alarm(
            index        = i + 1,
            enabled      = bool(raw["alarmflags"][i]),
            guard        = decode_guard(raw["alarmguards"][i]),
            neg_guard    = decode_guard(raw["alarmnegguards"][i]),
            phase        = decode_phase(raw["alarmtimes"][i]),
            offset_sec   = offset_sec,
            cond         = decode_cond(raw["alarmconds"][i]),
            source       = decode_source(raw["alarmsources"][i]),
            temperature  = float(raw["alarmtemperatures"][i]),
            action       = decode_action(raw["alarmactions"][i]),
            beep         = bool(raw["alarmbeep"][i]),
            label        = raw["alarmstrings"][i].strip(),
        )
        a.build_trigger_summary()
        alarms.append(a)

    return alarms


# ─────────────────────────────────────────────
#  FORMATTERS
# ─────────────────────────────────────────────

COLUMNS = ["#", "On", "Phase", "Offset", "Guard", "NegGuard",
           "Source", "Cond", "Temp°", "Action", "Beep", "Label"]

def alarm_row(a: Alarm) -> list:
    return [
        str(a.index),
        "✓" if a.enabled else "✗",
        a.phase,
        fmt_time(a.offset_sec),
        a.guard,
        a.neg_guard,
        a.source,
        a.cond,
        f"{a.temperature:.0f}" if a.temperature > 0 else "—",
        a.action,
        "✓" if a.beep else "✗",
        a.label,
    ]

# ── TEXT ──────────────────────────────────────

def fmt_text(alarms: list[Alarm], explain: bool) -> str:
    lines = ["Artisan Alarm File\n" + "=" * 60]
    for a in alarms:
        lines.append(f"\nAlarm #{a.index} {'[ENABLED]' if a.enabled else '[DISABLED]'}")
        lines.append(f"  Label   : {a.label}")
        lines.append(f"  Phase   : {a.phase} +{fmt_time(a.offset_sec)}")
        lines.append(f"  Guard   : {a.guard}  NegGuard: {a.neg_guard}")
        lines.append(f"  Trigger : {a.source} {a.cond} {a.temperature:.0f}°" if a.temperature > 0
                     else f"  Trigger : {a.source} (time-based)")
        lines.append(f"  Action  : {a.action}  Beep: {'yes' if a.beep else 'no'}")
        if explain:
            lines.append(f"  → {a.trigger_summary}")
    return "\n".join(lines)

# ── JSON ──────────────────────────────────────

def fmt_json(alarms: list[Alarm], explain: bool) -> str:
    data = []
    for a in alarms:
        d = {
            "index": a.index,
            "enabled": a.enabled,
            "label": a.label,
            "phase": a.phase,
            "offset": fmt_time(a.offset_sec),
            "offset_seconds": a.offset_sec,
            "guard": a.guard,
            "neg_guard": a.neg_guard,
            "source": a.source,
            "condition": a.cond,
            "temperature": a.temperature if a.temperature > 0 else None,
            "action": a.action,
            "beep": a.beep,
        }
        if explain:
            d["trigger_summary"] = a.trigger_summary
        data.append(d)
    return json.dumps(data, indent=2)

# ── MARKDOWN ──────────────────────────────────

def fmt_markdown(alarms: list[Alarm], explain: bool) -> str:
    lines = ["# Artisan Alarm Configuration\n"]
    header = "| " + " | ".join(COLUMNS) + " |"
    sep    = "| " + " | ".join(["---"] * len(COLUMNS)) + " |"
    lines += [header, sep]
    for a in alarms:
        row = alarm_row(a)
        lines.append("| " + " | ".join(row) + " |")
    if explain:
        lines.append("\n## Trigger Descriptions\n")
        for a in alarms:
            lines.append(f"**#{a.index} — {a.label}**  \n{a.trigger_summary}\n")
    return "\n".join(lines)

# ── ASCII TABLE ───────────────────────────────

def fmt_ascii(alarms: list[Alarm], explain: bool) -> str:
    rows = [COLUMNS] + [alarm_row(a) for a in alarms]
    widths = [max(len(r[c]) for r in rows) for c in range(len(COLUMNS))]

    def fmt_row(r):
        return " ".join(cell.ljust(widths[i]) for i, cell in enumerate(r))

    separator = " ".join("-" * w for w in widths)
    lines = ["ARTISAN ALARM FILE", separator, fmt_row(COLUMNS), separator]
    for a, row in zip(alarms, rows[1:]):
        lines.append(fmt_row(row))
        if explain:
            lines.append("  >> " + a.trigger_summary)
    lines.append(separator)
    return "\n".join(lines)

# ── PDF ───────────────────────────────────────

def fmt_pdf(alarms: list[Alarm], explain: bool, out_path: str):
    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                        Paragraph, Spacer, HRFlowable)
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
    except ImportError:
        print("ERROR: reportlab is required for PDF output. Install with: pip install reportlab")
        sys.exit(1)

    PAGE = landscape(letter)
    doc = SimpleDocTemplate(
        out_path,
        pagesize=PAGE,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.5*inch,  bottomMargin=0.5*inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Title"],
                                  fontSize=16, spaceAfter=4)
    sub_style   = ParagraphStyle("sub", parent=styles["Normal"],
                                  fontSize=9, textColor=colors.HexColor("#555555"),
                                  spaceAfter=10)
    note_style  = ParagraphStyle("note", parent=styles["Normal"],
                                  fontSize=7.5, textColor=colors.HexColor("#333333"),
                                  leading=10)
    label_style = ParagraphStyle("label", parent=styles["Normal"],
                                  fontSize=8, textColor=colors.HexColor("#111122"),
                                  leading=10)

    story = []

    # Title block
    # story.append(Paragraph("Artisan Alarm Configuration", title_style))
    title = f"{Path(out_path).stem}".replace("_alarms","")
    story.append(Paragraph(f"{title}", title_style))
    enabled_count = sum(1 for a in alarms if a.enabled)
    story.append(Paragraph(
        f"{len(alarms)} alarms total &nbsp;·&nbsp; {enabled_count} enabled &nbsp;·&nbsp; "
        # f"Artisan file: <i>{Path(out_path).stem}</i>"
        , sub_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc"), spaceAfter=8))

    # Table headers
    col_labels = ["#", "On", "Phase", "Offset", "Guard", "NegGuard",
                  "Source", "Cond", "Temp°", "Action", "Beep", "Label / Notes"]
    col_widths  = [0.35, 0.3, 0.85, 0.55, 0.75, 0.75,
                   0.65, 0.65, 0.5,  1.4,  0.4, 2.5]  # inches
    col_widths  = [w * inch for w in col_widths]

    header_row = [Paragraph(f"<b>{h}</b>", note_style) for h in col_labels]
    table_data = [header_row]

    PHASE_COLORS = {
        "CHARGE":   "#dce8ff",
        "DRY END":  "#fff0cc",
        "FC START": "#ffe0cc",
        "FC END":   "#ffd0cc",
        "SC START": "#f0ccff",
        "SC END":   "#e8ccff",
        "DROP":     "#f5f5f5", #"#ccffe8",
        "COOL END": "#e0f0ff",
        "TP":       "#ccffe8", #"#f5f5f5",
    }

    row_phase_colors = []
    for a in alarms:
        row = [
            Paragraph(str(a.index), note_style),
            Paragraph("<b>✓</b>" if a.enabled else "<font color='#aaaaaa'>✗</font>", note_style),
            Paragraph(f"<b>{a.phase}</b>", note_style),
            Paragraph(fmt_time(a.offset_sec), note_style),
            Paragraph(a.guard, note_style),
            Paragraph(a.neg_guard, note_style),
            Paragraph(a.source, note_style),
            Paragraph(a.cond, note_style),
            Paragraph(f"{a.temperature:.0f}°" if a.temperature > 0 else "—", note_style),
            Paragraph(a.action, note_style),
            Paragraph("✓" if a.beep else "—", note_style),
            Paragraph(a.label, label_style),
        ]
        table_data.append(row)
        row_phase_colors.append(PHASE_COLORS.get(a.phase, "#ffffff"))

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Base style
    ts = [
        ("BACKGROUND",   (0,0),  (-1,0),  colors.HexColor("#c7c7da")),
        ("TEXTCOLOR",    (0,0),  (-1,0),  colors.white),
        ("FONTNAME",     (0,0),  (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),  (-1,0),  8),
        ("TOPPADDING",   (0,0),  (-1,-1), 4),
        ("BOTTOMPADDING",(0,0),  (-1,-1), 4),
        ("LEFTPADDING",  (0,0),  (-1,-1), 5),
        ("RIGHTPADDING", (0,0),  (-1,-1), 5),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white]),
        ("GRID",         (0,0),  (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN",       (0,0),  (-1,-1), "MIDDLE"),
    ]

    # Phase-tinted rows
    for i, bg in enumerate(row_phase_colors):
        r = i + 1  # skip header
        ts.append(("BACKGROUND", (0, r), (2, r), colors.HexColor(bg)))

    # Disabled alarm rows: grey out
    for i, a in enumerate(alarms):
        if not a.enabled:
            r = i + 1
            ts.append(("TEXTCOLOR", (0, r), (-1, r), colors.HexColor("#bbbbbb")))

    tbl.setStyle(TableStyle(ts))
    story.append(tbl)

    # Explain section
    if explain:
        story.append(Spacer(1, 14))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc"), spaceAfter=6))
        story.append(Paragraph("<b>Trigger Descriptions</b>", styles["Heading2"]))
        story.append(Spacer(1, 4))

        exp_style = ParagraphStyle("exp", parent=styles["Normal"], fontSize=8,
                                    leading=12, spaceAfter=5)
        lbl_bold  = ParagraphStyle("lbl", parent=styles["Normal"], fontSize=8,
                                    leading=12, textColor=colors.HexColor("#1a1a2e"),
                                    fontName="Helvetica-Bold")
        for a in alarms:
            story.append(Paragraph(f"#{a.index} — {a.label}", lbl_bold))
            story.append(Paragraph(a.trigger_summary, exp_style))

    doc.build(story)
    print(f"PDF written to: {out_path}")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Parse and display Artisan .alrm alarm files."
    )
    parser.add_argument("file", help="Path to .alrm file")
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "markdown", "md", "ascii", "pdf"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--explain", "-e",
        action="store_true",
        help="Add human-readable trigger sentence for each alarm",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (for pdf/md/json; default: auto-named beside input file)",
    )
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    alarms = parse_alrm(args.file)
    fmt = args.format.lower()

    if fmt == "text":
        print(fmt_text(alarms, args.explain))

    elif fmt == "json":
        out = fmt_json(alarms, args.explain)
        if args.output:
            Path(args.output).write_text(out)
            print(f"JSON written to: {args.output}")
        else:
            print(out)

    elif fmt in ("md", "markdown"):
        out = fmt_markdown(alarms, args.explain)
        if args.output:
            Path(args.output).write_text(out)
            print(f"Markdown written to: {args.output}")
        else:
            print(out)

    elif fmt == "ascii":
        print(fmt_ascii(alarms, args.explain))

    elif fmt == "pdf":
        stem = Path(args.file).stem
        out_path = args.output or f"{stem}_alarms.pdf"
        fmt_pdf(alarms, args.explain, out_path)


if __name__ == "__main__":
    main()
