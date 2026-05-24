#!/usr/bin/env python3
import json
import pytest
import os
from plot_alarms import parse_time, format_time_mm_ss, parse_alarms

# ==========================================
# 1. TEST TIME UTILITIES
# ==========================================

def test_parse_time_string():
    """Test that MM:SS strings convert accurately to seconds."""
    assert parse_time("1:00") == 60.0
    assert parse_time("0:30") == 30.0
    assert parse_time("10:15") == 615.0

def test_parse_time_float():
    """Test that a minutes-based float or integer converts accurately to seconds."""
    assert parse_time("1.5") == 90.0
    assert parse_time("2") == 120.0

def test_format_time_mm_ss():
    """Test that seconds format correctly back into MM:SS strings."""
    assert format_time_mm_ss(60) == "1:00"
    assert format_time_mm_ss(30) == "0:30"
    assert format_time_mm_ss(615) == "10:15"


# ==========================================
# 2. TEST ALARM FILE PARSING
# ==========================================

@pytest.fixture
def mock_alrm_file(tmp_path):
    """Fixture that builds a temporary .alrm JSON file resembling Artisan data."""
    alarm_data = {
        "alarmflags": [1, 1, 1],
        "alarmguards": [-1, -1, -1],
        "alarmnegguards": [-1, -1, -1],
        "alarmtimes": [0, 1, 1],         # 0 = CHARGE, 1 = Turning Point (TP)
        "alarmoffsets": [4, 30, 60],     # Time offsets in seconds
        "alarmconds": [1, 2, 2],         # 1 = Absolute, 2 = Relative Offset
        "alarmsources": [1, -3, -3],
        "alarmtemperatures": [140.0, 0.0, 0.0],
        "alarmactions": [0, 3, 6],
        "alarmbeep": [1, 1, 1],
        "alarmstrings": [
            "140 Ready Charge 250gm",   # Non-setting event / Initial charge info
            "60 # convection",          # Burner setting 60 with comment
            "A70 # secondary airflow"    # Air setting 70 with comment
        ]
    }
    
    file_path = tmp_path / "test_profile.alrm"
    with open(file_path, "w") as f:
        json.dump(alarm_data, f)
        
    return str(file_path)


def test_parse_alarms_logic(mock_alrm_file):
    """Validates that alarms parse, calculate relative timeline offsets, and tag categories correctly."""
    # Define our baseline roaster milestone timeline parameters
    base_times = {
        'CHARGE': 0.0,
        'TP': 75.0,  # Let's assume Turning Point happened at 1:15 (75 seconds)
        'DE': 300.0,
        'FCs': 510.0,
        'FCe': 570.0,
        'DROP': 630.0
    }

    events = parse_alarms(mock_alrm_file, base_times)

    # 1. Check total functional timeline events found
    # (The first element '140 Ready Charge' should be skipped because it maps to value 140, 
    # which exceeds our 0-100 range validation filter).
    assert len(events) == 2

    # 2. Inspect the first parsed event (The Burner Setting)
    burner_event = events[0]
    assert burner_event['type'] == 'burner'
    assert burner_event['value'] == 60.0
    # Relative offset calculation: TP (75s) + offset (30s) = 105s
    assert burner_event['time'] == 105.0 
    assert "TP" in burner_event['trigger']
    assert burner_event['comment'] == 'convection'

    # 3. Inspect the second parsed event (The Air Setting)
    air_event = events[1]
    assert air_event['type'] == 'air'
    assert air_event['value'] == 70.0
    # Relative offset calculation: TP (75s) + offset (60s) = 135s
    assert air_event['time'] == 135.0
    assert "TP" in air_event['trigger']
    assert air_event['comment'] == 'secondary airflow'


def test_parse_alarms_file_missing():
    """Asserts that a clean FileNotFoundError is raised if the target file target is missing."""
    with pytest.raises(FileNotFoundError):
        parse_alarms("non_existent_file.alrm", base_times={})