#!/bin/bash
#
# example usage: ./parse-alog.sh roast_25-09-20_1234.alog
# assumes alog file is in current directory
# output is roast_25-09-20_1234.j4
# requires fix-alog.py in same directory
if [ "$1" == "" ]; then
  echo "usage: $0 alog-file"
  exit 1
fi

# cp $1 .
alogfile=$1
basefile=$(basename $alogfile .alog)
echo "basefile=$basefile"
# step 1: reformat alog to make it easier to parse
echo "step 1: reformat alog to make it easier to parse"
# change , to ,\n   (to put each field on its own line)
# sed 's/,/,\n/g' $basefile.alog > $basefile.tmp1
# wc -l $basefile.tmp1

# step 2: change single quote to double quote
echo "step 2: change single quote to double quote"
# sed "s/'/\"/g" $basefile.tmp1 > $basefile.tmp2
sed "s/'/\"/g" $basefile.alog > $basefile.tmp2
wc -l $basefile.tmp2

# step 3: change False/True to false/true
echo "step 3: change False/True to false/true"
sed "s/False/false/g" $basefile.tmp2 > $basefile.tmp3
sed "s/True/true/g" $basefile.tmp3 > $basefile.tmp4
wc -l $basefile.tmp4

# step 4: parse json lines to verify and reformat
echo "EXEC: python3 fix-alog.py $basefile.tmp4"
python3 fix-alog.py $basefile.tmp4 > $basefile.tmp5

# step 5: write to output file

# step 6: cleanup intermediate files
# rm -f $basefile.tmp?
echo "output file: $basefile"



