#!/bin/sh
# TODO: Remove duplication in functions

# Function to extract textual content from a LaTeX source
function processFile {
    TEX="${1}.tex"
    TXT="${1}.txt"
    ENCODING=`python ./detect_encoding.py $1`

    if [ "${ENCODING}" == 'None' ]; then
        dir=$(dirname $1)
        echo $1 >> "${dir}/failed.log"
        exit 0;
    fi
    iconv -f ${ENCODING} -t UTF-8 $1 > "${1}.tex"
    #pandoc -f latex -t plain "${1}.tex" -o "${1}.txt" # Fails on most files
    detex -n "${1}.tex" > "${1}.txt"
}

# Function to compile a LaTeX source and then extract plain text content
function processFilePDF {
    TEX="${1}.tex"
    PDF="${1}.pdf"
    ENCODING=`python ./detect_encoding.py $1`

    if [ "${ENCODING}" == 'None' ]; then
        dir=$(dirname $1)
        echo $1 >> "${dir}/failed.log"
        exit 0;
    fi
    iconv -f ${ENCODING} -t UTF-8 $1 > $TEX
    latex -interaction=nonstopmode $TEX
    # TODO: Add Catdvi to extract plain text
}

export -f processFile   # Make function executable by parallel
DIR=$1

# Save generated files in seperate directories
LATEX="${DIR}latex"
TXT="${DIR}txt"
PDF="${DIR}pdf"
rm "${DIR}/failed.log"

rm -rf $LATEX
rm -rf $TXT
#rm -rf $PDF

mkdir $LATEX
mkdir $TXT
#mkdir $PDF

find ${DIR} -type f ! -name "*.*" | parallel processFile ::: $FILES

mv "${DIR}"*.txt "${TXT}"
mv "${DIR}"*.tex "${LATEX}"
#mv "${DIR}"*.pdf "${PDF}"

