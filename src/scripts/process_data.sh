#!/bin/sh

function processFile {
    iconv -f WINDOWS-1252 -t UTF-8 $1 > "${1}.tex"
    pandoc -f latex -t plain "${1}.tex" -o "${1}.txt"
    detex "${1}.txt"        # Strip any remaining LaTeX from file. Data is noisey
}

export -f processFile   # Make function executable by parallel
DIR=$1
find ${DIR} -type f ! -name "*.*" | parallel processFile ::: $FILES

