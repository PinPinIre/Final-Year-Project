import sys
import logging
from os.path import isdir, isfile
from gensim import models
from corpus import Corpus
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class LDACorpus(Corpus):

    def __init__(self, dict_loc, vec_loc, no_topics=100, update=1, chunksize=10000, passes=1):
        Corpus.__init__(self)
        Corpus.load(self, dict_loc, vec_loc)
        self.no_topics = no_topics
        self.update = update
        self.chunksize = chunksize
        self.passes = passes
        self.dict_loc = dict_loc
        self.vec_loc = vec_loc
        self.transformation = models.ldamodel.LdaModel(corpus=self.docs, id2word=self.dictionary, num_topics=self.no_topics, update_every=self.update, chunksize=self.chunksize, passes=self.passes)

    def print_topics(self):
        self.transformation.print_topics(20)


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        corpus = Corpus(sys.argv[1])
        corpus.save(sys.argv[2], sys.argv[3])
        corpus = LDACorpus(sys.argv[2], sys.argv[3], no_topics=25)
        corpus.print_topics()
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()