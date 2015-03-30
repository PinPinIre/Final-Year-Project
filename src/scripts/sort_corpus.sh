#!/bin/sh
DIR=$1
log="${DIR}/paperstats.log"

NAMES="$(find ${DIR} -name '[a-z\-]*[0-9]*.*.txt' -maxdepth 1 -exec basename {} \; | grep --only-matching '^[a-z\-]*' | sort -u)"

for NAME in $NAMES
do
    OUT_DIR="${DIR}/${NAME}"
	mkdir -p $OUT_DIR
	find ${DIR} -name "${NAME}[0-9]*.*.txt" -exec mv {} $OUT_DIR \;
done

NAMES="$(find ${DIR} -mindepth 1 -type d -maxdepth 1 -exec basename {} \; | sort -u)"

for NAME in $NAMES
do
    OUT_DIR="${DIR}/${NAME}"
    count="$(find ${OUT_DIR} -name '*.txt' -maxdepth 1 | wc -l)"
    echo "${NAME}\t${count}" >> $log
done
