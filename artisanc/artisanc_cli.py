#!/usr/bin/env python3
"""
artisanc - Command line interface for Artisan Roaster Scope log files (*.alog)
"""

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional


class AlogParser:
    """Parser for Artisan Roaster Scope .alog files"""
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data: Dict[str, Any] = {}
        self._load()
    
    def _load(self):
        """Load and parse the .alog file"""
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                # Try parsing as Python dict first
                self.data = ast.literal_eval(content)
            except (ValueError, SyntaxError):
                # Fall back to JSON if dict parsing fails
                try:
                    self.data = json.loads(content)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid .alog file format: {e}")
    
    def save(self):
        """Save the modified data back to the .alog file"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            # Save as Python dict format (repr)
            f.write(repr(self.data))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Extract roast profile metrics"""
        metrics = {}
        
        # Basic roast information
        metrics['roast_id'] = self.data.get('roastUUID', 'N/A')
        metrics['date'] = self.data.get('roastdate', 'N/A')
        metrics['batch_size'] = self.data.get('weight', [0, 0, 'N/A'])
        metrics['beans'] = self.data.get('beans', 'N/A')
        metrics['color'] = self.data.get('ground_color', 'N/A')
        
        # Get computed data if available
        computed = self.data.get('computed', {})
        
        # Event metrics from computed data
        events = {}
        
        # CHARGE event
        if 'CHARGE_BT' in computed:
            events['CHARGE'] = {
                'time': '0:00',
                'ET': computed.get('CHARGE_ET', 'N/A'),
                'BT': computed.get('CHARGE_BT', 'N/A')
            }
        
        # TP (Turning Point) event
        if 'TP_time' in computed:
            tp_time = computed['TP_time']
            events['TP'] = {
                'time': self._format_time(tp_time),
                'ET': computed.get('TP_ET', 'N/A'),
                'BT': computed.get('TP_BT', 'N/A')
            }
        
        # DE (Dry End) event
        if 'DRY_time' in computed:
            dry_time = computed['DRY_time']
            events['DE'] = {
                'time': self._format_time(dry_time),
                'ET': computed.get('DRY_ET', 'N/A'),
                'BT': computed.get('DRY_BT', 'N/A')
            }
        
        # FCs (First Crack Start) event
        if 'FCs_time' in computed:
            fcs_time = computed['FCs_time']
            events['FCs'] = {
                'time': self._format_time(fcs_time),
                'ET': computed.get('FCs_ET', 'N/A'),
                'BT': computed.get('FCs_BT', 'N/A'),
                'ROR': computed.get('fcs_ror', 'N/A')
            }
        
        # FCe (First Crack End) - from timeindex[5] if available
        timeindex = self.data.get('timeindex', [])
        if len(timeindex) > 5 and timeindex[5] > 0:
            fce_idx = int(timeindex[5])
            events['FCe'] = {
                'time': self._format_time(timeindex[5]),
                'ET': self._get_temp_at_index(fce_idx, 'temp1'),
                'BT': self._get_temp_at_index(fce_idx, 'temp2')
            }
        
        # SCs (Second Crack Start) - from timeindex[2] if available
        if len(timeindex) > 2 and timeindex[2] > 0:
            scs_idx = int(timeindex[2])
            events['SCs'] = {
                'time': self._format_time(timeindex[2]),
                'ET': self._get_temp_at_index(scs_idx, 'temp1'),
                'BT': self._get_temp_at_index(scs_idx, 'temp2')
            }
        
        # DROP event
        if 'DROP_time' in computed:
            drop_time = computed['DROP_time']
            events['DROP'] = {
                'time': self._format_time(drop_time),
                'ET': computed.get('DROP_ET', 'N/A'),
                'BT': computed.get('DROP_BT', 'N/A')
            }
        
        metrics['events'] = events
        
        # Phase metrics
        if computed:
            metrics['total_time'] = self._format_time(computed.get('totaltime', 0))
            metrics['dry_phase_time'] = self._format_time(computed.get('dryphasetime', 0))
            metrics['mid_phase_time'] = self._format_time(computed.get('midphasetime', 0))
            metrics['finish_phase_time'] = self._format_time(computed.get('finishphasetime', 0))
            metrics['dry_phase_ror'] = computed.get('dry_phase_ror', 'N/A')
            metrics['mid_phase_ror'] = computed.get('mid_phase_ror', 'N/A')
            metrics['finish_phase_ror'] = computed.get('finish_phase_ror', 'N/A')
            metrics['total_ror'] = computed.get('total_ror', 'N/A')
            metrics['weight_loss'] = f"{computed.get('weight_loss', 'N/A')}%"
        
        return metrics
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds as MM:SS"""
        if seconds == 'N/A' or seconds < 0:
            return 'N/A'
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def _get_temp_at_index(self, index: int, temp_key: str) -> Any:
        """Get temperature at a specific index"""
        temps = self.data.get(temp_key, [])
        if 0 <= index < len(temps):
            temp = temps[index]
            return temp if temp >= 0 else 'N/A'
        return 'N/A'
    
    def get_roast_notes(self) -> str:
        """Get roasting notes"""
        return self.data.get('roastingnotes', '')
    
    def get_cup_notes(self) -> str:
        """Get cupping notes"""
        return self.data.get('cuppingnotes', '')
    
    def update_roast_notes(self, notes: str, append: bool = True):
        """Update roasting notes"""
        if append and 'roastingnotes' in self.data:
            existing = self.data.get('roastingnotes', '')
            self.data['roastingnotes'] = existing + '\n' + notes if existing else notes
        else:
            self.data['roastingnotes'] = notes
    
    def update_cup_notes(self, notes: str, append: bool = True):
        """Update cupping notes"""
        if append and 'cuppingnotes' in self.data:
            existing = self.data.get('cuppingnotes', '')
            self.data['cuppingnotes'] = existing + '\n' + notes if existing else notes
        else:
            self.data['cuppingnotes'] = notes


class OutputFormatter:
    """Format output in different formats"""
    
    @staticmethod
    def format_metrics(metrics: Dict[str, Any], format_type: str) -> str:
        """Format metrics in specified format"""
        if format_type == 'json':
            return json.dumps(metrics, indent=2)
        elif format_type == 'md':
            return OutputFormatter._format_metrics_markdown(metrics)
        else:  # text
            return OutputFormatter._format_metrics_text(metrics)
    
    @staticmethod
    def _format_metrics_text(metrics: Dict[str, Any]) -> str:
        """Format metrics as plain text"""
        lines = ["ROAST PROFILE METRICS", "=" * 50, ""]
        
        # Basic info
        lines.append(f"Roast ID         : {metrics.get('roast_id', 'N/A')}")
        lines.append(f"Date             : {metrics.get('date', 'N/A')}")
        
        batch = metrics.get('batch_size', [])
        if isinstance(batch, list) and len(batch) >= 3:
            lines.append(f"Batch Size       : {batch[0]}{batch[2]} → {batch[1]}{batch[2]}")
        
        lines.append(f"Beans            : {metrics.get('beans', 'N/A')}")
        lines.append(f"Color            : {metrics.get('color', 'N/A')}")
        lines.append(f"Weight Loss      : {metrics.get('weight_loss', 'N/A')}")
        
        # Events section
        events = metrics.get('events', {})
        if events:
            lines.append("\n" + "ROAST EVENTS")
            lines.append("-" * 50)
            lines.append(f"{'Event':<8} {'Time':>8} {'ET':>8} {'BT':>8} {'ROR':>8}")
            lines.append("-" * 50)
            
            for event_name in ['CHARGE', 'TP', 'DE', 'FCs', 'FCe', 'SCs', 'DROP']:
                if event_name in events:
                    event = events[event_name]
                    time_str = event.get('time', 'N/A')
                    et = event.get('ET', 'N/A')
                    bt = event.get('BT', 'N/A')
                    ror = event.get('ROR', '-')
                    
                    et_str = f"{et:.1f}" if isinstance(et, (int, float)) else str(et)
                    bt_str = f"{bt:.1f}" if isinstance(bt, (int, float)) else str(bt)
                    ror_str = f"{ror:.1f}" if isinstance(ror, (int, float)) and ror != '-' else str(ror)
                    
                    lines.append(f"{event_name:<8} {time_str:>8} {et_str:>8} {bt_str:>8} {ror_str:>8}")
        
        # Phase metrics
        lines.append("\n" + "PHASE METRICS")
        lines.append("-" * 50)
        lines.append(f"Total Time       : {metrics.get('total_time', 'N/A')}")
        lines.append(f"Dry Phase        : {metrics.get('dry_phase_time', 'N/A')} (ROR: {metrics.get('dry_phase_ror', 'N/A')})")
        lines.append(f"Mid Phase        : {metrics.get('mid_phase_time', 'N/A')} (ROR: {metrics.get('mid_phase_ror', 'N/A')})")
        lines.append(f"Finish Phase     : {metrics.get('finish_phase_time', 'N/A')} (ROR: {metrics.get('finish_phase_ror', 'N/A')})")
        lines.append(f"Total ROR        : {metrics.get('total_ror', 'N/A')}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _format_metrics_markdown(metrics: Dict[str, Any]) -> str:
        """Format metrics as markdown"""
        lines = ["# Roast Profile Metrics", ""]
        
        # Basic info
        lines.append("## Basic Information")
        lines.append(f"**Roast ID**: {metrics.get('roast_id', 'N/A')}  ")
        lines.append(f"**Date**: {metrics.get('date', 'N/A')}  ")
        
        batch = metrics.get('batch_size', [])
        if isinstance(batch, list) and len(batch) >= 3:
            lines.append(f"**Batch Size**: {batch[0]}{batch[2]} → {batch[1]}{batch[2]}  ")
        
        lines.append(f"**Beans**: {metrics.get('beans', 'N/A')}  ")
        lines.append(f"**Color**: {metrics.get('color', 'N/A')}  ")
        lines.append(f"**Weight Loss**: {metrics.get('weight_loss', 'N/A')}  ")
        
        # Events table
        events = metrics.get('events', {})
        if events:
            lines.append("\n## Roast Events")
            lines.append("\n| Event | Time | ET | BT | ROR |")
            lines.append("|-------|------|----|----|-----|")
            
            for event_name in ['CHARGE', 'TP', 'DE', 'FCs', 'FCe', 'SCs', 'DROP']:
                if event_name in events:
                    event = events[event_name]
                    time_str = event.get('time', 'N/A')
                    et = event.get('ET', 'N/A')
                    bt = event.get('BT', 'N/A')
                    ror = event.get('ROR', '-')
                    
                    et_str = f"{et:.1f}" if isinstance(et, (int, float)) else str(et)
                    bt_str = f"{bt:.1f}" if isinstance(bt, (int, float)) else str(bt)
                    ror_str = f"{ror:.1f}" if isinstance(ror, (int, float)) and ror != '-' else str(ror)
                    
                    lines.append(f"| {event_name} | {time_str} | {et_str} | {bt_str} | {ror_str} |")
        
        # Phase metrics
        lines.append("\n## Phase Metrics")
        lines.append(f"**Total Time**: {metrics.get('total_time', 'N/A')}  ")
        lines.append(f"**Dry Phase**: {metrics.get('dry_phase_time', 'N/A')} (ROR: {metrics.get('dry_phase_ror', 'N/A')})  ")
        lines.append(f"**Mid Phase**: {metrics.get('mid_phase_time', 'N/A')} (ROR: {metrics.get('mid_phase_ror', 'N/A')})  ")
        lines.append(f"**Finish Phase**: {metrics.get('finish_phase_time', 'N/A')} (ROR: {metrics.get('finish_phase_ror', 'N/A')})  ")
        lines.append(f"**Total ROR**: {metrics.get('total_ror', 'N/A')}  ")
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_notes(notes: str, title: str, format_type: str) -> str:
        """Format notes in specified format"""
        if format_type == 'json':
            return json.dumps({title.lower().replace(' ', '_'): notes}, indent=2)
        elif format_type == 'md':
            return f"# {title}\n\n{notes}"
        else:  # text
            return f"{title}\n{'=' * len(title)}\n\n{notes}"


def main():
    parser = argparse.ArgumentParser(
        description='CLI tool for Artisan Roaster Scope log files (*.alog)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('file', help='Path to .alog file')
    
    # Display options
    display_group = parser.add_mutually_exclusive_group()
    display_group.add_argument('--metrics', action='store_true',
                              help='Show roast profile metrics')
    display_group.add_argument('--roast', action='store_true',
                              help='Show roasting notes')
    display_group.add_argument('--cup', action='store_true',
                              help='Show cupping notes')
    
    # Output format
    parser.add_argument('-o', '--output', choices=['text', 'md', 'json'],
                       default='text', help='Output format (default: text)')
    
    # Update options
    parser.add_argument('--update', action='store_true',
                       help='Update notes from stdin (modifies file)')
    parser.add_argument('--append', action='store_true', default=True,
                       help='Append to existing notes instead of overwriting (default)')
    parser.add_argument('--overwrite', dest='append', action='store_false',
                       help='Overwrite existing notes instead of appending')
    
    args = parser.parse_args()
    
    try:
        alog = AlogParser(args.file)
        
        # Handle update mode
        if args.update:
            if not (args.roast or args.cup):
                print("Error: --update requires either --roast or --cup to specify which notes to update",
                      file=sys.stderr)
                sys.exit(1)
            
            # Read from stdin
            input_text = sys.stdin.read().strip()
            
            if args.roast:
                alog.update_roast_notes(input_text, append=args.append)
                print(f"Updated roasting notes ({'appended' if args.append else 'overwritten'})")
            elif args.cup:
                alog.update_cup_notes(input_text, append=args.append)
                print(f"Updated cupping notes ({'appended' if args.append else 'overwritten'})")
            
            alog.save()
            print(f"Saved changes to {args.file}")
        
        # Handle display mode
        else:
            formatter = OutputFormatter()
            
            if args.metrics:
                metrics = alog.get_metrics()
                output = formatter.format_metrics(metrics, args.output)
                print(output)
            
            elif args.roast:
                notes = alog.get_roast_notes()
                output = formatter.format_notes(notes, "Roasting Notes", args.output)
                print(output)
            
            elif args.cup:
                notes = alog.get_cup_notes()
                output = formatter.format_notes(notes, "Cupping Notes", args.output)
                print(output)
            
            else:
                # Default: show metrics
                metrics = alog.get_metrics()
                output = formatter.format_metrics(metrics, args.output)
                print(output)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
