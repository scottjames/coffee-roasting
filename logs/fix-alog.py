#!/usr/bin/env python3

import os,sys,json,pathlib
import argparse
import ast
# import markdown

# Parse Artisan Roasting Log file (.alog) and convert to JSON format
# write roastingnotes, cuppingnotes into .md file along with link to image of chart.

# parse logs/<basename>.alog file (which is python literal format) into python dict
# extract fields like: roastingnotes and cuppingnotes
# write roastingnotes and cuppingnotes to logs/notes/<basename>.md file
# README.md will link to image of chart: logs/img/<basename>.png and notes/<basename>.md


argparser=argparse.ArgumentParser(description="fix alog file")
argparser.add_argument("file",nargs=1,help="alog file to fix")
args=argparser.parse_args()
args.file=args.file[0]
if not os.path.isfile(args.file):
    print(f"file {args.file} not found")
    exit(1)

filebase= pathlib.Path(args.file).stem
print(f"filebase={filebase}")

print(f"fix file {args.file}")
with open(args.file,"r") as f:
    raw_chars = f.read().strip()
    print(f"read {len(raw_chars)} characters")
    alog_dict = ast.literal_eval(raw_chars)  # verify it is valid python literal
    print(f"converted to python dict with {len(alog_dict)} keys")

    # html_roastingnotes = markdown.markdown(alog_dict.get('roastingnotes',""))
    # print(f"converted roastingnotes to html with {len(html_roastingnotes)} characters")
    # print(f"first 100 chars: {html_roastingnotes[:100]}")

    json_string = json.dumps(alog_dict,indent=4)  # convert to json string
    print(f"converted to json string with {len(json_string)} characters")
    print(f"first 100 chars: {json_string[:100]}")

    # jsonlines = [json.loads(l) for l in json_string.split("\n") if l.strip()]
    # print(f"converted to list of {len(jsonlines)} json lines")
    # print(f"first line: {jsonlines[0]}")

    # lines=f.readlines()
    # lines=json.load(f)
    # json_string=[json.loads(l) for l in f.readlines()]
    # jsonlines=json.load(f)
    # jsonlines = json.loads(json_string.replace("'", "\""))
    # jsonlines = json.loads(lines.replace("'", "\""))

    # fixedlines=[json.dumps(l)+"\n" for l in jsonlines]
    outfile = f"{filebase}.json"
    with open(outfile,"w") as f:
        f.write(json_string)
    print(f"wrote fixed json file {outfile}")
exit(0)

