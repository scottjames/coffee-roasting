#!/usr/bin/env python3
import json
import argparse
import os
import svgwrite

def parse_time(time_str):
    """Parses MM:SS string or a float number into seconds."""
    if ':' in time_str:
        parts = time_str.split(':')
        return float(parts[0]) * 60 + float(parts[1])
    return float(time_str) * 60

def format_time_mm_ss(seconds):
    """Formats seconds into MM:SS format."""
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes}:{secs:02d}"

def parse_alarms(file_path, base_times):
    """Parses the .alrm JSON data into ordered burner and air events."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Alarm file not found: {file_path}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Reconstruct the list of events from parallel arrays
    events = []
    num_alarms = len(data.get("alarmflags", []))
    
    for i in range(num_alarms):
        # Extract metadata
        action = data["alarmactions"][i]
        source = data["alarmsources"][i]
        cond = data["alarmconds"][i]
        offset = data["alarmoffsets"][i]
        raw_string = data["alarmstrings"][i]
        
        # Determine Event Type: Burner vs Air
        # Artisan actions: 3 & 6 change settings. Sources define target.
        # Typically Source -3 indicates Heater/Burner or Air depending on setup, 
        # but let's parse from string flags ('#' for Burner vs 'A' for Fan/Air) 
        # or defaults matching the provided graph style.
        is_air = 'A' in raw_string and ('#' not in raw_string.split('A')[0])
        event_type = 'air' if is_air else 'burner'
        
        # Extract target numeric value from the description string
        # e.g., "30 # soak" -> value 30; "A60" or "60 #" -> value 60
        clean_str = raw_string.replace('#', '').strip()
        tokens = clean_str.split()
        val_token = tokens[0] if tokens else "0"
        if val_token.startswith('A'):
            val_token = val_token[1:]
        
        try:
            value = float(val_token)
        except ValueError:
            continue # Skip non-setting/informational alarms if they don't map to 0-100 values

        # Isolate the user comment
        comment = " ".join(tokens[1:]) if len(tokens) > 1 else ""

        # Calculate time based on condition rules (cond mapping to event triggers)
        # 1: absolute time/temp, 2: offset from an event index
        ref_event = data["alarmtimes"][i]
        trigger_label = ""
        event_time = 0.0

        if cond == 2:
            # Map event reference indexes to anchor names
            # Artisan mappings: 0=CHARGE, 1=TP, 2=DE, 6=FCs, 7=FCe, 8=DROP, etc.
            ref_map = {0: 'CHARGE', 1: 'TP', 2: 'DE', 6: 'FCs', 7: 'FCe', 8: 'DROP'}
            ref_name = ref_map.get(ref_event, f"REF_{ref_event}")
            
            anchor_time = base_times.get(ref_name, 0.0)
            event_time = anchor_time + offset
            
            offset_sign = "+" if offset >= 0 else ""
            trigger_label = f"{ref_name}{offset_sign}{format_time_mm_ss(offset)}"
        else:
            # Absolute condition
            if data["alarmtemperatures"][i] > 0:
                event_time = base_times.get('CHARGE', 0.0) # Absolute placement placeholder
                trigger_label = f"{data['alarmtemperatures'][i]}°C"
            else:
                event_time = float(offset)
                trigger_label = format_time_mm_ss(offset)

        events.append({
            'type': event_type,
            'time': event_time,
            'value': value,
            'trigger': trigger_label,
            'comment': comment
        })

    # Sort sequentially by timeline execution
    events.sort(key=lambda x: x['time'])
    return events


def create_artisan_svg(events, filename, title_name, max_time=720):
    """Generates an Artisan-styled landscape US Letter SVG graph."""
    # US Letter Landscape dimensions in points/pixels (11in x 8.5in at 96 DPI)
    width, height = 1056, 816
    dwg = svgwrite.Drawing(filename, size=(f"{width}px", f"{height}px"), profile='full')

    # Background canvas
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='#f8f9fa'))

    # Plot view margins
    pad_left, pad_right = 80, 80
    pad_top, pad_bottom = 100, 100
    graph_w = width - pad_left - pad_right
    graph_h = height - pad_top - pad_bottom

    # Define scales
    def get_x(t): return pad_left + (t / max_time) * graph_w
    def get_y(v): return pad_top + graph_h - (v / 100.0) * graph_h

    # Draw grid background lines (Y-axis 0 to 100 steps of 25)
    for y_val in [0, 25, 50, 75, 100]:
        y_pos = get_y(y_val)
        dwg.add(dwg.line((pad_left, y_pos), (width - pad_right, y_pos), stroke='#e9ecef', stroke_width=1))
        dwg.add(dwg.text(f"{y_val}", insert=(pad_left - 15, y_pos + 5), text_anchor="end", font_size="14px", font_family="sans-serif", fill="#6c757d"))

    # Draw Timeline X Axis intervals (every 2 minutes up to max time)
    for t_sec in range(0, int(max_time) + 1, 120):
        x_pos = get_x(t_sec)
        dwg.add(dwg.line((x_pos, pad_top), (x_pos, pad_top + graph_h), stroke='#e9ecef', stroke_width=1))
        dwg.add(dwg.text(format_time_mm_ss(t_sec), insert=(x_pos, pad_top + graph_h + 25), text_anchor="middle", font_size="14px", font_family="sans-serif", fill="#6c757d"))

    # Graph Title
    dwg.add(dwg.text(f"Artisan Profile Alarms: {title_name}", insert=(pad_left, 50), font_size="24px", font_family="sans-serif", font_weight="bold", fill="#1a252f"))

    # Separate events by actor
    burner_events = [e for e in events if e['type'] == 'burner']
    air_events = [e for e in events if e['type'] == 'air']

    def draw_sequence(seq_events, color_hex, text_color="#ffffff"):
        """Draws connecting step-lines, control setting block nodes, and data callout tags."""
        for i, ev in enumerate(seq_events):
            cx, cy = get_x(ev['time']), get_y(ev['value'])

            # Continuity Step Line Connection
            if i > 0:
                prev_ev = seq_events[i-1]
                px, py = get_x(prev_ev['time']), get_y(prev_ev['value'])
                # Artisan draws square horizontal/vertical step progressions
                dwg.add(dwg.line((px, py), (cx, py), stroke=color_hex, stroke_width=2))
                dwg.add(dwg.line((cx, py), (cx, cy), stroke=color_hex, stroke_width=2))
            elif cx > pad_left:
                # Extend line backwards to tracking start point
                dwg.add(dwg.line((pad_left, cy), (cx, cy), stroke=color_hex, stroke_width=2, stroke_dasharray="4,4"))

            # Draw outer continuity path to grid edge for the final setting state
            if i == len(seq_events) - 1:
                dwg.add(dwg.line((cx, cy), (width - pad_right, cy), stroke=color_hex, stroke_width=2))

            # Event Node Rectangle representation (Artisan Badge style)
            box_w, box_h = 36, 22
            dwg.add(dwg.rect(insert=(cx - box_w/2, cy - box_h/2), size=(box_w, box_h), fill=color_hex, rx=3, ry=3))
            
            # Formatted value output inside block
            disp_val = f"A{int(ev['value'])}" if ev['type'] == 'air' else f"B{int(ev['value'])}"
            dwg.add(dwg.text(disp_val, insert=(cx, cy + 5), text_anchor="middle", font_size="11px", font_family="sans-serif", font_weight="bold", fill=text_color))

            # Trigger Label Comment Bubble Oval
            bubble_w, bubble_h = 90, 36
            bx = cx + 20
            by = cy - bubble_h - 12
            
            # Anchor dynamic bounding limit corrections
            if bx + bubble_w > width - pad_right:
                bx = cx - bubble_w - 20
            
            dwg.add(dwg.rect(insert=(bx, by), size=(bubble_w, bubble_h), fill="#212529", rx=6, ry=6, opacity=0.85))
            
            # Primary Event Offset String Line
            dwg.add(dwg.text(ev['trigger'], insert=(bx + bubble_w/2, by + 15), text_anchor="middle", font_size="11px", font_family="sans-serif", font_weight="bold", fill="#ffffff"))
            
            # Secondary Optional Comments Metadata String Line
            if ev['comment']:
                truncated_comment = ev['comment'][:13] + '..' if len(ev['comment']) > 14 else ev['comment']
                dwg.add(dwg.text(truncated_comment, insert=(bx + bubble_w/2, by + 28), text_anchor="middle", font_size="9px", font_family="sans-serif", fill="#f8f9fa"))

    # Execute graphic render matrices for Burner (Crimson Red) and Airflow (Sky Blue) Channel paths
    draw_sequence(burner_events, color_hex="#dc3545")
    draw_sequence(air_events, color_hex="#17a2b8")

    # Save SVG Document
    dwg.save()

def main():
    parser = argparse.ArgumentParser(description="Convert Artisan .alrm files into custom SVG profile charts.")
    parser.add_argument('--in', dest='input_file', required=True, help="Path to input .alrm file")
    parser.add_argument('--out', dest='output_file', default='out.svg', help="Path to output SVG graph destination")
    parser.add_argument('--tp', default='1:00', help="Turning Point milestone time (MM:SS or minutes float)")
    parser.add_argument('--de', default='5:00', help="Dry End milestone time (MM:SS or minutes float)")
    parser.add_argument('--fcs', default='8:30', help="First Crack Start milestone time (MM:SS or minutes float)")
    parser.add_argument('--fce', default='9:30', help="First Crack End milestone time (MM:SS or minutes float)")
    parser.add_argument('--drop', default='10:30', help="Drop phase milestone time (MM:SS or minutes float)")

    args = parser.parse_args()

    # Normalize anchors to structural timeline offsets mapping back to the baseline model indices
    base_times = {
        'CHARGE': 0.0,
        'TP': parse_time(args.tp),
        'DE': parse_time(args.de),
        'FCs': parse_time(args.fcs),
        'FCe': parse_time(args.fce),
        'DROP': parse_time(args.drop)
    }

    # Determine maximum bounding X-Axis timeline constraint dynamically 
    max_timeline_limit = max(base_times.values()) + 120.0 

    try:
        events = parse_alarms(args.input_file, base_times)
        create_artisan_svg(events, args.output_file, os.path.basename(args.input_file), max_time=max_timeline_limit)
        print(f"Success! Scalable Artisan template visualization exported to: '{args.output_file}'")
    except Exception as e:
        print(f"Error compiling alarm visualization: {e}")

if __name__ == '__main__':
    main()
