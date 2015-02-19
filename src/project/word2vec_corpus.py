import sys
from os.path import isdir, isfile
from corpus import Corpus
from gensim import models


class W2VCorpus(Corpus):

    def __init__(self, dir, dict_loc, vec_loc):
        Corpus.__init__(self, dir)
        # Todo: Tweak the default paramaters
        self.model = models.Word2Vec(self.docs.get_texts(), size=100, window=5, min_count=5, workers=4)
        return

    def similarity(self, word1, word2):
        return self.model.similarity(word1, word2)


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        corpus = W2VCorpus(sys.argv[1], sys.argv[2], sys.argv[3])
        #print "Sim: column <-> row\t" + str(corpus.similarity("column", "row"))
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()