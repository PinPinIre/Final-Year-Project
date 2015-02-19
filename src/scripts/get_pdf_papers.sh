#!/bin/sh
# This script should not be used on large number of files. Just for a handful. Use arxiv S3 bucket for batches

DIR=$1
export PDF="${DIR}pdf"

# Function to download a pdf to a directory
function download_file {
    FILE=$(basename $1)
    python ./get_arxiv.py $FILE $PDF
}

export -f download_file   # Make function executable by parallel
# Save generated files in seperate directories

mkdir $PDF

find ${DIR} -type f ! -name "*.*" | parallel download_file ::: $FILES
