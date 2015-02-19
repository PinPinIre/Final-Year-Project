#!/bin/sh

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
