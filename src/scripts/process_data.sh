#!/bin/sh

function processFile {
    pandoc -f latex -t plain $1 -o "${1}.txt"
    detex "${1}.txt"        # Strip any remaining LaTeX from file. Data is noisey
}

export -f processFile   # Make function executable by parallel
DIR=$1
FILES=`find ${DIR} -type f ! -name "*.*"`
parallel processFile ::: $FILES

