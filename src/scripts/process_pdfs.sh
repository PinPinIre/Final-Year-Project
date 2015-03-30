#!/bin/sh

DIR=$1
OUTPUT_DIR=$2
export TXT="${OUTPUT_DIR}/txt"

# Function to convert from a pdf to a txt file
function process_file {
    FILE=$(basename $1)
    pdftotext $1 "${TXT}/${FILE}.txt"
}

export -f process_file   # Make function executable by parallel

mkdir $TXT

find ${DIR} -type f -name "*.pdf" | parallel process_file
