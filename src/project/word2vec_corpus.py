import sys
import datetime
from os.path import isdir, isfile
from corpus import Corpus
from gensim import models


class W2VCorpus(Corpus):
    # TODO: the clipped corpus class doesn't implement get_texts(), investigate this
    def __init__(self, directory=None, dictionary=None, corpus=None, w2v_model=None, max_docs=None):
        Corpus.__init__(self, directory=directory, dictionary=dictionary, corpus=corpus, max_docs=max_docs)
        self.dict_loc = dictionary
        self.vec_loc = corpus
        self.model = None
        start_time = datetime.datetime.now()
        if not w2v_model:
            # Todo: Tweak the default parameter
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

    def save(self, dictionary_file="w2v_corpus.dict", corpus_file="corpus.mm", sup_file="vector.w2vs"):
        Corpus.save(self, dictionary_file, corpus_file)
        if self.model: self.model.save(sup_file)

    @classmethod
    def load(cls, dictionary_file=None, corpus_file=None, sup_file=None):
        return cls(dictionary=dictionary_file, corpus=corpus_file, w2v_model=sup_file)

    def clip_corpus(self, max_docs=None):
        # Override the default clip_corpus function to do nothing.
        pass


def main():
    w2v = "w2vcorpus.w2v"
    if len(sys.argv) is 4 and isdir(sys.argv[1]):
        if not isfile(w2v):
            corpus = W2VCorpus(directory=sys.argv[1])
            corpus.save(dictionary_file=sys.argv[2], corpus_file=sys.argv[3] ,sup_file=w2v)
        else:
            corpus = W2VCorpus.load(dictionary_file=sys.argv[2], corpus_file=sys.argv[3], sup_file=w2v)
        time = corpus.get_train_time()
        print "W2V Train Time:\t" + str(time)
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()