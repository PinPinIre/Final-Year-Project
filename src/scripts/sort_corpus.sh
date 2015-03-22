#!/bin/sh
DIR=$1

NAMES="$(find ${DIR} -name '[a-z\-]*[0-9]*.*.txt' -exec basename {} \; | grep --only-matching '^[a-z\-]*' | sort -u)"

for NAME in $NAMES
do
    OUT_DIR="${DIR}${NAME}"
	mkdir -p $OUT_DIR
	find ${DIR} -name "${NAME}[0-9]*.*.txt" -exec mv {} $OUT_DIR \;
done
