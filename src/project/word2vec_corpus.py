import sys
import datetime
from os.path import isdir, isfile
from corpus import Corpus
from gensim import models


class W2VCorpus(Corpus):

    def __init__(self, directory=None, dictionary=None, corpus=None, w2v_model=None, max_docs=None):
        Corpus.__init__(self, directory=directory, dictionary=dictionary, corpus=corpus)
        self.clip_corpus(max_docs)
        self.dict_loc = dictionary
        self.vec_loc = corpus
        self.model = None
        start_time = datetime.datetime.now()
        if not w2v_model:
            # Todo: Tweak the default paramaters
            self.model = models.Word2Vec(self.docs.get_texts(), size=100, window=5, min_count=5, workers=4)
        else:
            self.model = models.Word2Vec.load(w2v_model)
        end_time = datetime.datetime.now()
        self.train_time = end_time - start_time
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

    @classmethod
    def load(cls, dictionary, corpus, w2v_file):
        return cls(dictionary=dictionary, corpus=corpus, w2v_model=w2v_file)


def main():
    w2v = "w2vcorpus.w2v"
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        if not isfile(w2v):
            corpus = W2VCorpus(sys.argv[1], sys.argv[2], sys.argv[3])
            corpus.save(w2v)
        else:
            corpus = W2VCorpus.load(sys.argv[2], sys.argv[3], w2v)
        print "Sim: velocity <-> speed\t" + str(corpus.similarity("velocity", "speed"))
        time = corpus.get_train_time()
        print "W2V Train Time:\t" + str(time)
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()