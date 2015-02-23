import sys
from os.path import isdir, isfile
from corpus import Corpus
from lda_corpus import LDACorpus


class WordCloud(object):

    def __init__(self, lda_corpus):
        self.corpus = lda_corpus


    def draw_topics(self):
        print self.corpus
        topics = self.corpus.print_topics()
        print topics


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]):

        if not isfile(sys.argv[2]) and not isfile(sys.argv[3]):
            corpus = Corpus(sys.argv[1])
            corpus.save(sys.argv[2], sys.argv[3])
        corpus = LDACorpus(sys.argv[2], sys.argv[3], no_topics=25)
        wc = WordCloud(corpus)
        print wc.draw_topics()
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()