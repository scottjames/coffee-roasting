import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO
import tempfile

from alrm_parser import main, parse_alrm, Alarm


@pytest.fixture
def sample_alrm_data():
    """Sample alarm JSON data for testing."""
    return {
        "alarmflags": [True, False],
        "alarmoffsets": [60, 120],
        "alarmguards": [-1, 0],
        "alarmnegguards": [-1, 1],
        "alarmtimes": [0, 2],
        "alarmconds": [2, 1],
        "alarmsources": [1, 0],
        "alarmtemperatures": [200.0, 180.0],
        "alarmactions": [0, 4],
        "alarmbeep": [True, False],
        "alarmstrings": ["First alarm", "Second alarm"],
    }


@pytest.fixture
def temp_alrm_file(sample_alrm_data, tmp_path):
    """Create a temporary .alrm file."""
    alrm_file = tmp_path / "test.alrm"
    alrm_file.write_text(json.dumps(sample_alrm_data))
    return str(alrm_file)


def test_main_text_format_default(temp_alrm_file, capsys):
    """Test main with default text format."""
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file]):
        main()
    captured = capsys.readouterr()
    assert "Artisan Alarm File" in captured.out
    assert "Alarm #1" in captured.out
    assert "[ENABLED]" in captured.out


def test_main_text_format_explicit(temp_alrm_file, capsys):
    """Test main with explicit text format."""
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file, "--format", "text"]):
        main()
    captured = capsys.readouterr()
    assert "Artisan Alarm File" in captured.out


def test_main_json_format_stdout(temp_alrm_file, capsys):
    """Test main with JSON format to stdout."""
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file, "--format", "json"]):
        main()
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["index"] == 1
    assert data[0]["enabled"] is True


def test_main_json_format_file_output(temp_alrm_file, tmp_path):
    """Test main with JSON format to file."""
    output_file = tmp_path / "output.json"
    with patch.object(sys, "argv", 
                     ["alrm_parser.py", temp_alrm_file, "--format", "json", 
                      "--output", str(output_file)]):
        main()
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert len(data) == 2


def test_main_markdown_format(temp_alrm_file, tmp_path, capsys):
    """Test main with markdown format."""
    output_file = tmp_path / "output.md"
    with patch.object(sys, "argv",
                     ["alrm_parser.py", temp_alrm_file, "--format", "md",
                      "--output", str(output_file)]):
        main()
    assert output_file.exists()
    content = output_file.read_text()
    assert "# Artisan Alarm:" in content
    assert "| #" in content  # markdown table


def test_main_ascii_format(temp_alrm_file, capsys):
    """Test main with ASCII format."""
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file, "--format", "ascii"]):
        main()
    captured = capsys.readouterr()
    assert "ARTISAN ALARM FILE" in captured.out
    assert "#" in captured.out


def test_main_pdf_format(temp_alrm_file, tmp_path, capsys):
    """Test main with PDF format (requires reportlab)."""
    pytest.importorskip("reportlab")
    output_file = tmp_path / "output.pdf"
    with patch.object(sys, "argv",
                     ["alrm_parser.py", temp_alrm_file, "--format", "pdf",
                      "--output", str(output_file)]):
        main()
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_main_explain_flag(temp_alrm_file, capsys):
    """Test main with --explain flag."""
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file, "--explain"]):
        main()
    captured = capsys.readouterr()
    assert "→" in captured.out  # trigger summary includes arrow


def test_main_explain_with_json(temp_alrm_file, capsys):
    """Test main with --explain flag in JSON format."""
    with patch.object(sys, "argv", 
                     ["alrm_parser.py", temp_alrm_file, "--format", "json", "--explain"]):
        main()
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "trigger_summary" in data[0]


def test_main_file_not_found(capsys):
    """Test main with non-existent file."""
    with patch.object(sys, "argv", ["alrm_parser.py", "/nonexistent/file.alrm"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
    assert "File not found" in captured.err


def test_main_short_format_flag(temp_alrm_file, capsys):
    """Test main with short format flag."""
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file, "-f", "json"]):
        main()
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data, list)


def test_main_short_explain_flag(temp_alrm_file, capsys):
    """Test main with short explain flag."""
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file, "-e"]):
        main()
    captured = capsys.readouterr()
    assert "→" in captured.out


def test_main_short_output_flag(temp_alrm_file, tmp_path):
    """Test main with short output flag."""
    output_file = tmp_path / "out.json"
    with patch.object(sys, "argv",
                     ["alrm_parser.py", temp_alrm_file, "-f", "json", "-o", str(output_file)]):
        main()
    assert output_file.exists()


def test_main_pdf_auto_named(temp_alrm_file, tmp_path, monkeypatch):
    """Test main with PDF auto-naming."""
    pytest.importorskip("reportlab")
    monkeypatch.chdir(tmp_path)
    with patch.object(sys, "argv", ["alrm_parser.py", temp_alrm_file, "--format", "pdf"]):
        main()
    pdf_file = tmp_path / "test_alarms.pdf"
    assert pdf_file.exists()