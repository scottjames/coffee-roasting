#!/usr/bin/env python3
"""
Pytest test suite for artisanc CLI tool
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
import sys

# Import the module under test
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artisanc_cli import AlogParser, OutputFormatter


# Sample test data
SAMPLE_ALOG_DATA = {
    'roastUUID': 'test-uuid-12345',
    'roastdate': 'Sat Sep 28 2025',
    'beans': 'Guatemala Test Beans\n150 grams',
    'weight': [150.0, 128.0, 'g'],
    'ground_color': 55,
    'timeindex': [16, 188, 343, 0, 0, 0, 446, 0],
    'timex': [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
    'temp1': [90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0],
    'temp2': [130.0, 125.0, 135.0, 145.0, 155.0, 165.0, 175.0],
    'roastingnotes': 'Initial test notes',
    'cuppingnotes': 'Initial cup notes',
    'computed': {
        'CHARGE_ET': 90.2,
        'CHARGE_BT': 131.0,
        'TP_idx': 1,
        'TP_time': 10.0,
        'TP_ET': 91.2,
        'TP_BT': 125.0,
        'DRY_time': 16.0,
        'DRY_ET': 105.5,
        'DRY_BT': 139.9,
        'FCs_time': 188.0,
        'FCs_ET': 118.4,
        'FCs_BT': 165.5,
        'fcs_ror': 6.9,
        'DROP_time': 446.0,
        'DROP_ET': 126.4,
        'DROP_BT': 181.0,
        'totaltime': 446.0,
        'dryphasetime': 172.0,
        'midphasetime': 155.0,
        'finishphasetime': 119.0,
        'dry_phase_ror': 8.9,
        'mid_phase_ror': 6.5,
        'finish_phase_ror': 5.8,
        'total_ror': 7.1,
        'weight_loss': 15
    }
}

MINIMAL_ALOG_DATA = {
    'roastUUID': 'minimal-uuid',
    'roastdate': 'Sun Sep 29 2025',
    'beans': 'Minimal Test',
    'weight': [150.0, 130.0, 'g'],
    'ground_color': 0,
    'timeindex': [20, 200, 0, 0, 0, 0, 450, 0],
    'timex': [0.0, 20.0, 200.0, 450.0],
    'temp1': [88.0, 92.0, 110.0, 120.0],
    'temp2': [128.0, 120.0, 160.0, 178.0],
    'roastingnotes': '',
    'cuppingnotes': ''
}


@pytest.fixture
def temp_alog_file():
    """Create a temporary alog file with sample data"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.alog', delete=False) as f:
        f.write(repr(SAMPLE_ALOG_DATA))
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_minimal_alog():
    """Create a temporary alog file with minimal data"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.alog', delete=False) as f:
        f.write(repr(MINIMAL_ALOG_DATA))
        temp_path = f.name
    
    yield temp_path
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestAlogParser:
    """Test AlogParser class"""
    
    def test_load_valid_file(self, temp_alog_file):
        """Test loading a valid alog file"""
        parser = AlogParser(temp_alog_file)
        assert parser.data['roastUUID'] == 'test-uuid-12345'
        assert parser.data['beans'] == 'Guatemala Test Beans\n150 grams'
    
    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist"""
        with pytest.raises(FileNotFoundError):
            AlogParser('/nonexistent/file.alog')
    
    def test_load_invalid_format(self):
        """Test loading a file with invalid format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.alog', delete=False) as f:
            f.write('invalid data format {{')
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError):
                AlogParser(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_get_metrics_with_computed(self, temp_alog_file):
        """Test extracting metrics with computed data"""
        parser = AlogParser(temp_alog_file)
        metrics = parser.get_metrics()
        
        assert metrics['roast_id'] == 'test-uuid-12345'
        assert metrics['date'] == 'Sat Sep 28 2025'
        assert 'events' in metrics
        assert 'CHARGE' in metrics['events']
        assert 'TP' in metrics['events']
        assert 'DE' in metrics['events']
        assert 'FCs' in metrics['events']
        assert 'DROP' in metrics['events']
    
    def test_get_metrics_minimal_data(self, temp_minimal_alog):
        """Test extracting metrics with minimal data (no computed dict)"""
        parser = AlogParser(temp_minimal_alog)
        metrics = parser.get_metrics()
        
        assert metrics['roast_id'] == 'minimal-uuid'
        assert 'events' in metrics
        assert 'CHARGE' in metrics['events']
        assert metrics['events']['CHARGE']['BT'] == 128.0
    
    def test_get_roast_notes(self, temp_alog_file):
        """Test getting roasting notes"""
        parser = AlogParser(temp_alog_file)
        notes = parser.get_roast_notes()
        assert notes == 'Initial test notes'
    
    def test_get_cup_notes(self, temp_alog_file):
        """Test getting cupping notes"""
        parser = AlogParser(temp_alog_file)
        notes = parser.get_cup_notes()
        assert notes == 'Initial cup notes'
    
    def test_update_roast_notes_overwrite(self, temp_alog_file):
        """Test updating roast notes with overwrite"""
        parser = AlogParser(temp_alog_file)
        parser.update_roast_notes('New notes', append=False)
        assert parser.data['roastingnotes'] == 'New notes'
    
    def test_update_roast_notes_append(self, temp_alog_file):
        """Test updating roast notes with append"""
        parser = AlogParser(temp_alog_file)
        parser.update_roast_notes('Additional notes', append=True)
        assert 'Initial test notes' in parser.data['roastingnotes']
        assert 'Additional notes' in parser.data['roastingnotes']
    
    def test_update_cup_notes_overwrite(self, temp_alog_file):
        """Test updating cup notes with overwrite"""
        parser = AlogParser(temp_alog_file)
        parser.update_cup_notes('New cup notes', append=False)
        assert parser.data['cuppingnotes'] == 'New cup notes'
    
    def test_update_cup_notes_append(self, temp_alog_file):
        """Test updating cup notes with append"""
        parser = AlogParser(temp_alog_file)
        parser.update_cup_notes('More cup notes', append=True)
        assert 'Initial cup notes' in parser.data['cuppingnotes']
        assert 'More cup notes' in parser.data['cuppingnotes']
    
    def test_save_file(self, temp_alog_file):
        """Test saving modified data"""
        parser = AlogParser(temp_alog_file)
        parser.update_roast_notes('Modified notes', append=False)
        parser.save()
        
        # Reload and verify
        parser2 = AlogParser(temp_alog_file)
        assert parser2.data['roastingnotes'] == 'Modified notes'
    
    def test_format_time(self, temp_alog_file):
        """Test time formatting"""
        parser = AlogParser(temp_alog_file)
        assert parser._format_time(0) == '0:00'
        assert parser._format_time(65) == '1:05'
        assert parser._format_time(446) == '7:26'
        assert parser._format_time(-1) == 'N/A'
    
    def test_find_time_index(self, temp_alog_file):
        """Test finding time index"""
        parser = AlogParser(temp_alog_file)
        idx = parser._find_time_index(20.0)
        assert idx >= 0
        assert abs(parser.data['timex'][idx] - 20.0) < 1.0


class TestOutputFormatter:
    """Test OutputFormatter class"""
    
    def test_format_metrics_text(self):
        """Test text formatting"""
        metrics = {
            'roast_id': 'test-123',
            'date': 'Sep 28 2025',
            'batch_size': [150.0, 128.0, 'g'],
            'beans': 'Test Beans',
            'color': 55,
            'weight_loss': '15%',
            'events': {
                'CHARGE': {'time': '0:00', 'ET': 90.0, 'BT': 130.0},
                'DROP': {'time': '7:26', 'ET': 126.0, 'BT': 181.0}
            },
            'total_time': '7:26'
        }
        
        output = OutputFormatter.format_metrics(metrics, 'text')
        assert 'ROAST PROFILE METRICS' in output
        assert 'test-123' in output
        assert 'CHARGE' in output
        assert 'DROP' in output
    
    def test_format_metrics_json(self):
        """Test JSON formatting"""
        metrics = {'test_key': 'test_value'}
        output = OutputFormatter.format_metrics(metrics, 'json')
        parsed = json.loads(output)
        assert parsed['test_key'] == 'test_value'
    
    def test_format_metrics_markdown(self):
        """Test markdown formatting"""
        metrics = {
            'roast_id': 'test-123',
            'date': 'Sep 28 2025',
            'batch_size': [150.0, 128.0, 'g'],
            'beans': 'Test Beans',
            'events': {
                'CHARGE': {'time': '0:00', 'ET': 90.0, 'BT': 130.0}
            }
        }
        
        output = OutputFormatter.format_metrics(metrics, 'md')
        assert '# Roast Profile Metrics' in output
        assert '**Roast ID**' in output
        assert '| Event |' in output
    
    def test_format_notes_text(self):
        """Test notes formatting as text"""
        notes = "Test notes content"
        output = OutputFormatter.format_notes(notes, "Roasting Notes", 'text')
        assert 'Roasting Notes' in output
        assert 'Test notes content' in output
    
    def test_format_notes_json(self):
        """Test notes formatting as JSON"""
        notes = "Test notes"
        output = OutputFormatter.format_notes(notes, "Roasting Notes", 'json')
        parsed = json.loads(output)
        assert 'roasting_notes' in parsed
    
    def test_format_notes_markdown(self):
        """Test notes formatting as markdown"""
        notes = "Test notes"
        output = OutputFormatter.format_notes(notes, "Roasting Notes", 'md')
        assert '# Roasting Notes' in output
        assert 'Test notes' in output


class TestCLI:
    """Test CLI functionality"""
    
    def test_metrics_display(self, temp_alog_file, capsys):
        """Test --metrics flag"""
        with patch('sys.argv', ['artisanc', temp_alog_file, '--metrics']):
            from artisanc_cli import main
            main()
            captured = capsys.readouterr()
            assert 'ROAST PROFILE METRICS' in captured.out
    
    def test_roast_notes_display(self, temp_alog_file, capsys):
        """Test --roast flag"""
        with patch('sys.argv', ['artisanc', temp_alog_file, '--roast']):
            from artisanc_cli import main
            main()
            captured = capsys.readouterr()
            assert 'Initial test notes' in captured.out
    
    def test_cup_notes_display(self, temp_alog_file, capsys):
        """Test --cup flag"""
        with patch('sys.argv', ['artisanc', temp_alog_file, '--cup']):
            from artisanc_cli import main
            main()
            captured = capsys.readouterr()
            assert 'Initial cup notes' in captured.out
    
    def test_json_output_format(self, temp_alog_file, capsys):
        """Test -o json flag"""
        with patch('sys.argv', ['artisanc', temp_alog_file, '--metrics', '-o', 'json']):
            from artisanc_cli import main
            main()
            captured = capsys.readouterr()
            # Should be valid JSON
            parsed = json.loads(captured.out)
            assert 'roast_id' in parsed
    
    def test_markdown_output_format(self, temp_alog_file, capsys):
        """Test -o md flag"""
        with patch('sys.argv', ['artisanc', temp_alog_file, '--metrics', '-o', 'md']):
            from artisanc_cli import main
            main()
            captured = capsys.readouterr()
            assert '# Roast Profile Metrics' in captured.out
    
    def test_update_roast_notes(self, temp_alog_file):
        """Test --update with --roast"""
        new_notes = "Updated roast notes via stdin"
        
        with patch('sys.argv', ['artisanc', temp_alog_file, '--roast', '--update']):
            with patch('sys.stdin.read', return_value=new_notes):
                from artisanc_cli import main
                main()
        
        # Verify update
        parser = AlogParser(temp_alog_file)
        assert new_notes in parser.data['roastingnotes']
    
    def test_update_overwrite_mode(self, temp_alog_file):
        """Test --update with --overwrite"""
        new_notes = "Completely new notes"
        
        with patch('sys.argv', ['artisanc', temp_alog_file, '--roast', '--update', '--overwrite']):
            with patch('sys.stdin.read', return_value=new_notes):
                from artisanc_cli import main
                main()
        
        parser = AlogParser(temp_alog_file)
        assert parser.data['roastingnotes'] == new_notes
        assert 'Initial test notes' not in parser.data['roastingnotes']
    
    def test_nonexistent_file_error(self, capsys):
        """Test error handling for nonexistent file"""
        with patch('sys.argv', ['artisanc', '/nonexistent/file.alog', '--metrics']):
            from artisanc_cli import main
            with pytest.raises(SystemExit):
                main()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
