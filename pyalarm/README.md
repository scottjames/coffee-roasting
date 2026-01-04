

The script can accept command line arguments.  Use it like this:

**Basic usage:**
```bash
python script.py --alarm trigger-alarms-10-200g.alrm
```

**With custom output file:**
```bash
python script.py --alarm myalarms.alrm --output custom_output.md
```

**Key features added:**

1. **`--alarm` flag** (required): Specifies the input .alrm file
2. **`--output` flag** (optional): Specifies custom output filename
   - If not provided, auto-generates: `<input_filename>_output.md`
3. **Error handling**: Validates file exists and handles parsing errors
4. **Help text**: Run `python script.py --help` to see usage information

The script will now:
- Check if the input file exists
- Parse it and show a summary in the terminal
- Export the markdown table to the specified (or auto-generated) output file
- Display a success message with the output location

