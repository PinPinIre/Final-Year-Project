import sys
from os.path import isdir, isfile
from corpus import Corpus


class W2VCorpus(Corpus):

    def __init__(self, dict_loc, vec_loc):
        Corpus.__init__(self)
        Corpus.load(self, dict_loc, vec_loc)
        # Set up for Word-to-Vec
        return


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        corpus = Corpus(sys.argv[1])
        corpus.save(sys.argv[2], sys.argv[3])
        corpus = W2VCorpus(sys.argv[2], sys.argv[3])
        corpus.print_topics()
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()