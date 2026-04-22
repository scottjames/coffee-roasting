
write a python script to:
- read and parse alarm (*.alrm) files from artisan scope coffee roasting software.
- parse the alarm file contents into a memory model.
- output the model in one of the following formats: markdown, json, text, ascii, pdf.
- user will select the output format as command line argument.
- add output format 'ascii' which is a space delimited ascii table used for nice formatting in terminal.
- add pdf output format which prints a very readable, full 1-page format.
- Decode enum values into readable labels.
- Decode guards into roast phases (CHARGE, DRY, FC, SC).
- Interpret time vs offset into actual roast timeline triggers.
- display times as mm:ss.
- Add human-readable trigger sentence.
- An example alrm file is attached.

