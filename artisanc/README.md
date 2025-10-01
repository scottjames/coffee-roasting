
# artisanc - Artisan Roaster Scope command line interface

A comprehensive Python script for parsing and managing Artisan Roaster Scope log files.
This will handle metrics, notes management, and multiple output formats.

## Features:

**Display Options:**
- `--metrics` - Shows roast profile metrics (duration, temperatures, phases, beans, etc.)
- `--roast` - Displays roasting notes
- `--cup` - Shows cupping notes

**Output Formats:**
- `-o text` - Plain text (default)
- `-o md` - Markdown format
- `-o json` - JSON format

**Update Functionality:**
- `--update` - Reads from stdin and modifies the .alog file
- `--append` - Appends to existing notes (default behavior)
- `--overwrite` - Replaces existing notes completely

## Usage Examples:

```bash
# View metrics
python artisanc roast.alog --metrics

# View roasting notes in markdown
python artisanc roast.alog --roast -o md

# Update cupping notes (append)
echo "Fruity notes, bright acidity" | python artisanc roast.alog --cup --update

# Overwrite roasting notes
echo "New notes only" | python artisanc roast.alog --roast --update --overwrite

# Export to JSON
python artisanc roast.alog --metrics -o json
```

The script parses the JSON structure of .alog files, extracts key roasting data,
and provides flexible note management with stdin input for automation workflows.


