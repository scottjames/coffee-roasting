import json
import argparse
from dataclasses import dataclass
from typing import List
from pathlib import Path


@dataclass
class Alarm:
    """Represents a single alarm configuration"""
    index: int
    flag: int
    guard: int
    neg_guard: int
    time: int
    offset: float
    condition: int
    source: int
    temperature: float
    action: int
    beep: int
    description: str
    
    def get_time_display(self) -> str:
        """Convert time code to readable format"""
        time_map = {
            -1: "N/A",
            0: "START",
            1: "CHARGE",
            2: "DRY END",
            6: "FC START",
            7: "FC END",
            8: "SC START"
        }
        return time_map.get(self.time, f"Time {self.time}")
    
    def get_condition_display(self) -> str:
        """Convert condition code to readable format"""
        cond_map = {
            1: "Temperature",
            2: "Time"
        }
        return cond_map.get(self.condition, f"Cond {self.condition}")
    
    def get_source_display(self) -> str:
        """Convert source code to readable format"""
        source_map = {
            1: "BT (Bean Temp)",
            -3: "Time-based"
        }
        return source_map.get(self.source, f"Source {self.source}")
    
    def get_action_display(self) -> str:
        """Convert action code to readable format"""
        action_map = {
            0: "None",
            3: "Play Sound",
            6: "Notification"
        }
        return action_map.get(self.action, f"Action {self.action}")


class ArtisanAlarmParser:
    """Parser for Artisan Roaster .alrm files"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.alarms: List[Alarm] = []
        
    def parse(self) -> List[Alarm]:
        """Parse the alarm file and return list of Alarm objects"""
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        
        num_alarms = len(data['alarmflags'])
        
        for i in range(num_alarms):
            alarm = Alarm(
                index=i + 1,
                flag=data['alarmflags'][i],
                guard=data['alarmguards'][i],
                neg_guard=data['alarmnegguards'][i],
                time=data['alarmtimes'][i],
                offset=data['alarmoffsets'][i],
                condition=data['alarmconds'][i],
                source=data['alarmsources'][i],
                temperature=data['alarmtemperatures'][i],
                action=data['alarmactions'][i],
                beep=data['alarmbeep'][i],
                description=data['alarmstrings'][i]
            )
            self.alarms.append(alarm)
        
        return self.alarms
    
    def to_markdown(self, output_path: str = "alarms_output.md"):
        """Export alarms to a markdown table"""
        if not self.alarms:
            self.parse()
        
        with open(output_path, 'w') as f:
            f.write("# Artisan Roaster Alarm Configuration\n\n")
            f.write(f"**Source File:** `{Path(self.filepath).name}`\n\n")
            f.write(f"**Total Alarms:** {len(self.alarms)}\n\n")
            
            # Summary table
            f.write("## Alarm Summary\n\n")
            f.write("| # | Active | Trigger | Offset | Condition | Source | Action | Description |\n")
            f.write("|---|--------|---------|--------|-----------|--------|--------|-------------|\n")
            
            for alarm in self.alarms:
                active = "✓" if alarm.flag == 1 else "✗"
                trigger = alarm.get_time_display()
                offset_str = f"{alarm.offset:.0f}s" if alarm.condition == 2 else f"{alarm.temperature:.1f}°"
                
                f.write(f"| {alarm.index} | {active} | {trigger} | {offset_str} | "
                       f"{alarm.get_condition_display()} | {alarm.get_source_display()} | "
                       f"{alarm.get_action_display()} | {alarm.description} |\n")
            
            # Detailed table
            f.write("\n## Detailed Alarm Configuration\n\n")
            f.write("| # | Flag | Time | Offset | Cond | Source | Temp | Action | Beep | Guard | Neg Guard | Description |\n")
            f.write("|---|------|------|--------|------|--------|------|--------|------|-------|-----------|-------------|\n")
            
            for alarm in self.alarms:
                f.write(f"| {alarm.index} | {alarm.flag} | {alarm.time} | {alarm.offset} | "
                       f"{alarm.condition} | {alarm.source} | {alarm.temperature} | {alarm.action} | "
                       f"{alarm.beep} | {alarm.guard} | {alarm.neg_guard} | {alarm.description} |\n")
            
            # Legend
            f.write("\n## Legend\n\n")
            f.write("### Time Codes\n")
            f.write("- `-1`: N/A\n")
            f.write("- `0`: START\n")
            f.write("- `1`: CHARGE\n")
            f.write("- `2`: DRY END\n")
            f.write("- `6`: FC START (First Crack Start)\n")
            f.write("- `7`: FC END (First Crack End)\n")
            f.write("- `8`: SC START (Second Crack Start)\n\n")
            
            f.write("### Condition Codes\n")
            f.write("- `1`: Temperature-based\n")
            f.write("- `2`: Time-based\n\n")
            
            f.write("### Source Codes\n")
            f.write("- `1`: BT (Bean Temperature)\n")
            f.write("- `-3`: Time-based trigger\n\n")
            
            f.write("### Action Codes\n")
            f.write("- `0`: None\n")
            f.write("- `3`: Play Sound\n")
            f.write("- `6`: Notification\n")
        
        print(f"Markdown table exported to: {output_path}")


# Example usage
if __name__ == "__main__":
    # Set up argument parser
    arg_parser = argparse.ArgumentParser(
        description="Parse Artisan Roaster alarm files (.alrm) and export to markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script.py --alarm trigger-alarms-10-200g.alrm
  python script.py --alarm myalarms.alrm --output custom_output.md
        """
    )
    
    arg_parser.add_argument(
        '--alarm',
        required=True,
        type=str,
        help='Path to the .alrm alarm file to parse'
    )
    
    arg_parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output markdown file path (default: <input_filename>_output.md)'
    )
    
    args = arg_parser.parse_args()
    
    # Validate input file exists
    if not Path(args.alarm).exists():
        print(f"Error: File '{args.alarm}' not found!")
        exit(1)
    
    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        input_path = Path(args.alarm)
        output_file = input_path.stem + "_output.md"
    
    try:
        # Parse the alarm file
        parser = ArtisanAlarmParser(args.alarm)
        alarms = parser.parse()
        
        # Print summary
        print(f"Parsed {len(alarms)} alarms from '{args.alarm}'\n")
        
        print("Active Alarms:")
        active_count = 0
        for alarm in alarms:
            if alarm.flag == 1:
                print(f"  [{alarm.index}] {alarm.get_time_display()} + {alarm.offset}: {alarm.description}")
                active_count += 1
        
        if active_count == 0:
            print("  (none)")
        
        # Export to markdown
        parser.to_markdown(output_file)
        print(f"\n✓ Markdown table exported to: {output_file}")
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in alarm file - {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
