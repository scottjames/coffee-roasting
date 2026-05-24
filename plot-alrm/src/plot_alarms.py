#!/usr/bin/env python3
import json
import argparse
import os
import logging
import svgwrite

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    """Parses the .alrm JSON data into ordered burner and air events"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Alarm file not found: {file_path}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    events = []
    num_alarms = len(data.get("alarmflags", [])) # [cite: 1]
    
    for i in range(num_alarms):
        action = data["alarmactions"][i] # [cite: 1]
        # source = data["alarmsources"][i] # [cite: 1]
        cond = data["alarmconds"][i] # [cite: 1]
        offset = data["alarmoffsets"][i] # [cite: 1]
        raw_string = data["alarmstrings"][i] # [cite: 1]
        
        # Check if the event is an airflow modification
        if action == 3:
            event_type = 'air'
        elif action == 6:
            event_type = 'burner'
        else:
            event_type = 'unk'
        # is_air = 'A' in action and ('#' not in raw_string.split('A')[0])
        # event_type = 'air' if is_air else 'burner'
        
        # Extract target numeric value from description string
        clean_str = raw_string.replace('#', '').strip()
        tokens = clean_str.split()
        val_token = tokens[0] if tokens else "0"
        if val_token.startswith('A'):
            val_token = val_token[1:]
        
        try:
            value = float(val_token)
        except ValueError:
            continue 

        comment = " ".join(tokens[1:]) if len(tokens) > 1 else ""
        ref_event = data["alarmtimes"][i] # [cite: 1]
        trigger_label = ""
        event_time = 0.0

        if cond == 2: # [cite: 1]
            ref_map = {0: 'CHARGE', 1: 'TP', 2: 'DE', 6: 'FCs', 7: 'FCe', 8: 'DROP'}
            ref_name = ref_map.get(ref_event, f"REF_{ref_event}")
            
            anchor_time = base_times.get(ref_name, 0.0)
            event_time = anchor_time + offset
            
            offset_sign = "+" if offset >= 0 else ""
            trigger_label = f"{ref_name}{offset_sign}{format_time_mm_ss(offset)}"
        else:
            if data["alarmtemperatures"][i] > 0: # [cite: 1]
                event_time = base_times.get('CHARGE', 0.0)
                trigger_label = f"{data['alarmtemperatures'][i]}°C" # [cite: 1]
            else:
                event_time = float(offset)
                trigger_label = format_time_mm_ss(offset)

        events.append({
            'time': event_time,
            'type': event_type,
            'value': value,
            'trigger': trigger_label,
            'comment': comment
        })

    events.sort(key=lambda x: x['time'])
    return events


def create_artisan_svg(events, filename, title_name, base_times, max_time=720):
    """Generates an Artisan-styled landscape US Letter SVG graph."""
    width, height = 1056, 816
    dwg = svgwrite.Drawing(filename, size=(f"{width}px", f"{height}px"), profile='full')

    # Background canvas
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='#f8f9fa'))

    # Plot view margins
    pad_left, pad_right = 80, 80
    pad_top, pad_bottom = 100, 100
    graph_w = width - pad_left - pad_right
    graph_h = height - pad_top - pad_bottom

    def get_x(t): return pad_left + (t / max_time) * graph_w
    def get_y(v): return pad_top + graph_h - (v / 100.0) * graph_h

    # Draw grid background lines (Y-axis 0 to 100 steps of 10)
    for y_val in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        y_pos = get_y(y_val)
        # use dotted gride lines to reduce visual clutter
        dwg.add(dwg.line((pad_left, y_pos), (width - pad_right, y_pos),
                         stroke="#777777", stroke_width=1, stroke_dasharray="4,4"))
        dwg.add(dwg.text(f"{y_val}", insert=(pad_left - 15, y_pos + 5),
                          text_anchor="end", font_size="14px", font_family="sans-serif", fill="#6c757d"))

    # Draw Timeline X Axis intervals (every 1 minutes)
    for t_sec in range(0, int(max_time) + 1, 60):
        x_pos = get_x(t_sec)
        dwg.add(dwg.line((x_pos, pad_top), (x_pos, pad_top + graph_h),
                         stroke="#777777", stroke_width=1, stroke_dasharray="4,4"))
        dwg.add(dwg.text(format_time_mm_ss(t_sec), insert=(x_pos, pad_top + graph_h + 25),
                         text_anchor="middle", font_size="14px", font_family="sans-serif", fill="#6c757d"))

    # Draw vertical blue dotted line markers for major roast phases
    milestones = ['TP', 'DE', 'FCs', 'FCe', 'DROP']
    for milestone in milestones:
        m_time = base_times.get(milestone, None)
        if m_time is not None and m_time > 0:
            mx = get_x(m_time)
            # Vertical dotted indicator line
            dwg.add(dwg.line((mx, pad_top), (mx, pad_top + graph_h),
                             stroke='#007bff', stroke_width=2.5, stroke_dasharray='4,4'))
            # Milestone top anchor text label
            dwg.add(dwg.text(milestone, insert=(mx, pad_top - 15),
                             text_anchor='middle', font_size='12px', font_family='sans-serif',
                             font_weight='bold', fill='#007bff'))

    # Graph Title
    dwg.add(dwg.text(f"Artisan Profile Alarms: {title_name}",
                      insert=(pad_left, 50), font_size="24px",
                      font_family="sans-serif", font_weight="bold", fill="#1a252f"))

    # Separate events by actor
    burner_events = [e for e in events if e['type'] == 'burner']
    air_events = [e for e in events if e['type'] == 'air']

    def draw_sequence(seq_events, color_hex, text_color="#ffffff", show_comments=True):
        """Draws connecting step-lines, control setting block nodes, and data callout tags."""
        for i, ev in enumerate(seq_events):
            cx, cy = get_x(ev['time']), get_y(ev['value'])

            # draw step lines from previous event to current event
            if i > 0:
                prev_ev = seq_events[i-1]
                px, py = get_x(prev_ev['time']), get_y(prev_ev['value'])
                dwg.add(dwg.line((px, py), (cx, py), stroke=color_hex, stroke_width=2))
                dwg.add(dwg.line((cx, py), (cx, cy), stroke=color_hex, stroke_width=2))
            elif cx > pad_left:
                dwg.add(dwg.line((pad_left, cy), (cx, cy),
                                 stroke=color_hex, stroke_width=2, stroke_dasharray="4,4"))

            if i == len(seq_events) - 1:
                dwg.add(dwg.line((cx, cy), (width - pad_right, cy),
                                 stroke=color_hex, stroke_width=2))

            # Event Node Badge
            box_w, box_h = 42, 22
            dwg.add(dwg.rect(insert=(cx - box_w/2, cy - box_h/2), size=(box_w, box_h),
                             fill=color_hex, rx=3, ry=3, opacity=1))
            
            # Label generation: render as "A##" or "B" inside boxes
            if ev['type'] == 'air':
                disp_val = f"A{int(ev['value'])}"
                comment_y_offset = 36
            elif ev['type'] == 'burner':
                disp_val = f"B{int(ev['value'])}"
                comment_y_offset = -12
            else:
                disp_val = "X"
            # disp_val = f"A{int(ev['value'])}" if ev['type'] == 'air' else f"B{int(ev['value'])}"
            dwg.add(dwg.text(disp_val, insert=(cx, cy + 5), text_anchor="middle",
                             font_size="11px", font_family="sans-serif",
                             font_weight="bold", fill=text_color, opacity=1))

            if show_comments:
                # Trigger Label Comment Bubble Oval
                bubble_w, bubble_h = 90, 36
                bx = cx + 24
                by = cy - bubble_h + comment_y_offset
                
                if bx + bubble_w > width - pad_right:
                    bx = cx - bubble_w - 24
                
                dwg.add(dwg.rect(insert=(bx, by), size=(bubble_w, bubble_h), fill="#212529",
                                rx=6, ry=6, opacity=1))
                dwg.add(dwg.text(ev['trigger'], insert=(bx + bubble_w/2, by + 15),
                                text_anchor="middle", font_size="11px", font_family="sans-serif",
                                font_weight="bold", fill="#ffffff", opacity=1))
                
                if ev['comment']:
                    truncated_comment = ev['comment'][:13] + '..' if len(ev['comment']) > 14 else ev['comment']
                    dwg.add(dwg.text(truncated_comment, insert=(bx + bubble_w/2, by + 28),
                                text_anchor="middle", font_size="9px", font_family="sans-serif",
                                fill="#f8f9fa"))

    # Render configurations: Burner (Crimson Red) & Air (Sky Blue)
    draw_sequence(burner_events, color_hex="#dc3545", show_comments=False)
    draw_sequence(air_events, color_hex="#17a2b8", show_comments=False)

    dwg.save()

def dump_events(events):
    """Utility function to print parsed events to console for debugging."""
    print("Parsed Events:")
    for ev in events:
        print(f"  - Time: {format_time_mm_ss(ev['time'])}, Type: {ev['type']}, Value: {ev['value']}, Trigger: {ev['trigger']}, Comment: {ev['comment']}")   


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

    base_times = {
        'CHARGE': 0.0,
        'TP': parse_time(args.tp),
        'DE': parse_time(args.de),
        'FCs': parse_time(args.fcs),
        'FCe': parse_time(args.fce),
        'DROP': parse_time(args.drop)
    }

    max_timeline_limit: int = int(max(base_times.values())) + 120

    try:
        events = parse_alarms(args.input_file, base_times)
        dump_events(events)
        create_artisan_svg(events, args.output_file, os.path.basename(args.input_file), base_times, max_time=max_timeline_limit)
        print(f"Success! Scalable Artisan template visualization exported to: '{args.output_file}'")
    except Exception as e:
        print(f"Error compiling alarm visualization: {e}")

if __name__ == '__main__':
    main()
