#!/bin/bash

# get filename for report
REPORT_FILE=$1
OUTPUT_FILE=`basename $1 .report`.output
EXPECTED_RESULT=$2
TARGET=$3
if [ ! "$4" = "--" ]; then
  echo "error: argument error, \$4 has to be '--'!"
  exit 2
fi
shift 4

# run simulavr, this uses all other arguments
echo "$*"
if [ ${GNUTIME} = yes ]; then
  TIME_CMD=/usr/bin/time
else
  # bash builtin time command!
  TIME_CMD=time
fi
(${TIME_CMD} -p $*) > ${REPORT_FILE}.stdout 2> ${REPORT_FILE}.stderr
RESULT=$?

# write report
echo "${TARGET} `tail -n 2 ${REPORT_FILE}.stderr | head -1 | cut "-d " -f 2`" > ${REPORT_FILE}

# write output
echo "stdout:" > $OUTPUT_FILE
cat ${REPORT_FILE}.stdout >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE
echo "stderr:" >> $OUTPUT_FILE
cat ${REPORT_FILE}.stderr >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# give back exit code
RES=0
if [ ! $RESULT = $EXPECTED_RESULT ]; then
  echo ""
  echo "error: return code from avrs = $RESULT, expected = $EXPECTED_RESULT!"
  echo ""
  cat $OUTPUT_FILE
  RES=1
fi
rm -f ${REPORT_FILE}.stdout ${REPORT_FILE}.stderr
exit $RES

# EOF
