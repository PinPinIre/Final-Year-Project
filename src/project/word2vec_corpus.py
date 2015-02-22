import sys
from os.path import isdir, isfile
from corpus import Corpus
from gensim import models


class W2VCorpus(Corpus):

    def __init__(self, dict_loc, vec_loc, dir=None):
        Corpus.__init__(self, dir)
        self.dict_loc = dict_loc
        self.vec_loc = vec_loc
        self.model = None
        if dir:
            # Todo: Tweak the default paramaters
            self.model = models.Word2Vec(self.docs.get_texts(), size=100, window=5, min_count=5, workers=4)
        return

    def similarity(self, word1, word2):
        if self.model:
            return self.model.similarity(word1, word2)
        else:
            # Todo: Raise exception?
            return None

    def save(self, file):
        super(W2VCorpus, self).save(self.dict_loc, self.vec_loc)
        if self.model: self.model.save(file)

    def load(self, file):
        super(W2VCorpus, self).load(self.dict_loc, self.vec_loc)
        self.model = models.Word2Vec.load(file)


def main():
    w2v = "w2vcorpus.w2v"
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        if not isfile(w2v):
            corpus = W2VCorpus(sys.argv[2], sys.argv[3], sys.argv[1])
            corpus.save(w2v)
        else:
            corpus = W2VCorpus(sys.argv[2], sys.argv[3])
            corpus.load(w2v)
        print "Sim: velocity <-> speed\t" + str(corpus.similarity("velocity", "speed"))
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()