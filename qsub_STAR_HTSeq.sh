#/bin/bash

SAMPLE_LIST=$1
SCRIPT_DIR=/mnt/HDD/share/RNA_seq
JOB_SCRIPT=${SCRIPT_DIR}/STAR_HTSeq.sh
REQ_CPU=8

while read row; do
  column1=`echo ${row} | cut -d , -f 1 | tr -d '\n' | tr -d '\r'`
  column2=`echo ${row} | cut -d , -f 2 | tr -d '\n' | tr -d '\r'`
  bash $JOB_SCRIPT ${column1} ${column2} $REQ_CPU
done < "${SAMPLE_LIST}"

