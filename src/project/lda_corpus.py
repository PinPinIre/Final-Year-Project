import sys
from os.path import isdir, isfile
from gensim import models
from corpus import Corpus
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class LDACorpus(Corpus):

    def __init__(self, dictionary=None, corpus=None, lda_corpus=None, no_topics=100, update=1, chunksize=10000, passes=1):
        Corpus.__init__(self, dictionary=dictionary, corpus=corpus)
        self.no_topics = no_topics
        self.update = update
        self.chunksize = chunksize
        self.passes = passes
        self.dict_loc = dictionary
        self.vec_loc = corpus
        if not lda_corpus:
            self.transform_corpus(models.TfidfModel)
            self.model = self.train_model()
        else:
            self.model = models.ldamodel.LdaModel.load(lda_corpus)

    def print_topics(self, num_words=10):
        if self.model: return self.model.print_topics(100, num_words=num_words)

    def train_model(self):
        #self.model = models.ldamodel.LdaModel(corpus=self, id2word=self.dictionary, num_topics=self.no_topics, update_every=self.update, chunksize=self.chunksize, passes=self.passes)
        return models.ldamodel.LdaModel(corpus=self, id2word=self.dictionary, num_topics=self.no_topics, iterations=500)

    def save(self, dictionary, file, lda_file):
        Corpus.save(self, dictionary, file)
        self.model.save(lda_file)

    @classmethod
    def load(cls, dictionary, corpus, lda_file):
        return cls(dictionary=dictionary, corpus=corpus, lda_corpus=lda_file)


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        corpus = LDACorpus(sys.argv[2], sys.argv[3], no_topics=100)
        corpus.train_model()
        corpus.print_topics()
        #corpus.save("LDA.dict", "LDA.mm")
        #corpus = LDACorpus.load("LDA.dict", "LDA.mm")
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()