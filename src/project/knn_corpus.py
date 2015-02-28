import sys
from os.path import isdir, isfile
from corpus import Corpus
from gensim.matutils import corpus2csc
from gensim import models
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class KNNCorpus(Corpus):

    def __init__(self, dictionary=None, corpus=None):
        Corpus.__init__(self, dictionary=dictionary, corpus=corpus)
        # Set up for KNN
        self.transform_corpus(models.TfidfModel)
        scipi_sparse = corpus2csc(self)
        print scipi_sparse
        return


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        corpus = KNNCorpus(sys.argv[2], sys.argv[3])
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()