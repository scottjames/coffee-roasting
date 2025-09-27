
#!/usr/bin/env python3
"""
Artisan Scope ALOG File Parser
Reads .alog files and extracts bean temperature data to JSON format
Supports the Python dictionary format used by Artisan Scope
"""

import json
import sys
import os
import ast
from datetime import datetime, timedelta
from pathlib import Path

class AlogParser:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = []
        self.metadata = {}
        self.alog_data = None
        
    def parse_alog_file(self):
        """Parse the .alog file and extract bean temperature data"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Parse the Python dictionary from the file
            self.alog_data = ast.literal_eval(content)
            
            # Extract metadata
            self._extract_metadata()
            
            # Extract temperature data
            self._extract_temperature_data()
            
            return True
            
        except Exception as e:
            print(f"Error parsing file: {e}")
            return False
    
    def _extract_metadata(self):
        """Extract metadata from the alog data"""
        # Basic metadata
        metadata_keys = [
            'version', 'revision', 'build', 'title', 'beans', 'weight', 
            'roastdate', 'roastisodate', 'roasttime', 'roastbatchnr',
            'roastertype', 'operator', 'organization', 'roastingnotes',
            'cuppingnotes', 'samplinginterval'
        ]
        
        for key in metadata_keys:
            if key in self.alog_data:
                self.metadata[key] = self.alog_data[key]
        
        # Computed values if available
        if 'computed' in self.alog_data:
            computed = self.alog_data['computed']
            computed_keys = [
                'totaltime', 'CHARGE_BT', 'TP_time', 'TP_BT', 'DRY_time', 'DRY_BT',
                'FCs_time', 'FCs_BT', 'DROP_time', 'DROP_BT', 'total_ror'
            ]
            
            for key in computed_keys:
                if key in computed:
                    self.metadata[f'computed_{key}'] = computed[key]
    
    def _extract_temperature_data(self):
        """Extract time and bean temperature data from the alog file"""
        if 'timex' not in self.alog_data or 'temp2' not in self.alog_data:
            print("Error: Required temperature data not found in file")
            return
        
        timex = self.alog_data['timex']
        temp2 = self.alog_data['temp2']  # temp2 is typically bean temperature
        
        if len(timex) != len(temp2):
            print(f"Warning: Time and temperature arrays have different lengths ({len(timex)} vs {len(temp2)})")
        
        # Get roast start time if available
        roast_start = None
        if 'roastisodate' in self.alog_data and 'roasttime' in self.alog_data:
            try:
                date_str = self.alog_data['roastisodate']
                time_str = self.alog_data['roasttime']
                roast_start = datetime.fromisoformat(f"{date_str}T{time_str}")
            except:
                pass
        
        # Process each data point
        for i, (time_val, temp_val) in enumerate(zip(timex, temp2)):
            # Skip invalid temperature readings
            if temp_val == -1.0:
                continue
            
            # Create timestamp
            if roast_start:
                timestamp = roast_start + timedelta(seconds=time_val)
                time_str = timestamp.isoformat()
            else:
                time_str = f"{time_val:.2f}s"
            
            # Format time in minutes:seconds as well
            minutes = int(time_val // 60)
            seconds = int(time_val % 60)
            time_display = f"{minutes:02d}:{seconds:02d}"
            
            self.data.append({
                "time_seconds": round(time_val, 2),
                "time_display": time_display,
                "time_iso": time_str,
                "bean_temperature": round(temp_val, 2),
                "temperature_unit": "°C"  # We use Celcius
            })
    
    def export_to_json(self, output_path=None):
        """Export parsed data to JSON file"""
        if not output_path:
            output_path = self.file_path.with_suffix('.json')
        
        # Additional statistics
        if self.data:
            temps = [d['bean_temperature'] for d in self.data]
            stats = {
                "min_temperature": min(temps),
                "max_temperature": max(temps),
                "temperature_range": max(temps) - min(temps),
                "duration_seconds": self.data[-1]['time_seconds'],
                "duration_display": self.data[-1]['time_display']
            }
        else:
            stats = {}
        
        output_data = {
            "metadata": {
                "source_file": str(self.file_path),
                "parsed_at": datetime.now().isoformat(),
                "total_data_points": len(self.data),
                "parser_version": "2.0",
                "statistics": stats,
                **self.metadata
            },
            "temperature_data": self.data
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully exported {len(self.data)} data points to {output_path}")
            print(f"Temperature range: {stats.get('min_temperature', 'N/A')}°F - {stats.get('max_temperature', 'N/A')}°F")
            print(f"Total roast time: {stats.get('duration_display', 'N/A')}")
            return str(output_path)
            
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python alog_parser.py <path_to_alog_file>")
        print("Example: python alog_parser.py roast_25-09-20_1215.alog")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    parser = AlogParser(file_path)
    
    if parser.parse_alog_file():
        output_file = parser.export_to_json()
        if output_file:
            print(f"\nParsing completed successfully!")
            print(f"Output saved to: {output_file}")
            
            # Show some sample data
            if parser.data:
                print(f"\nSample data points:")
                for i in [0, len(parser.data)//4, len(parser.data)//2, -1]:
                    if i < len(parser.data):
                        d = parser.data[i]
                        print(f"  {d['time_display']}: {d['bean_temperature']}°F")
        else:
            print("Failed to export JSON file")
    else:
        print("Failed to parse the .alog file")

if __name__ == "__main__":
    main()

