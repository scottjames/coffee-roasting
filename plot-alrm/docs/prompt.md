

create python script that will plot artisan alarm files as SVG graph:
- read the required cmdline arg 'in' as the file name of .alrm file.
- read the optional cmdline arg 'out' as the file name to output svg file, default is 'out.svg'. overwrite any existing out file.
- read parameter 'tp' as turning-point from command line arg, default value 1:00 minute.
- read parameter 'de' as dry-end from command line arg, default value 5:00 minute.
- read parameter 'fcs' as first-crack-start from command line arg, default value 8:30 minute.
- read parameter 'fce' as first-crack-end from command line arg, default value 9:30 minute.
- read parameter 'drop' as drop from command line arg, default value 10:30 minute.

use model to collect the events from the alrm file.
- parse the alarm .alrm file parameters for the specified events to change burner and air settings in reference to tip, de, fcs, fce and drop events.
keep data model with burner and air along with trigger type, time and setting value along with 'comment' from the alrm file.

plot as svg graph in same style that Artisan software plots:
- use y axis range of 0 to 100.
- plot blue boxes with white numbers to show air event.
- plot red boxes with white numbers to show burner event.
- plot lines to connect the boxes along horizontal direction showing continuity.
- draw black oval comment bubble just above and right of each event showing the trigger.
  * for example show  "TP+1:45" for 1:45 after turning point, also show any optional user comment in the bubble as second line.
  * for example show  "TP+1:45" for 1:45 after turning point.
- plot large SVG chart as full page view on us letter landscape mode.
- plot title with alarm input filename from 'in' cmdline arg.

an example alrm file is included.
an example artisan png graph is included.

