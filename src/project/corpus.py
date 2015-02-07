import sys
from os import listdir
from os.path import isdir, isfile, join


class Corpus(object):

    def __init__(self, dir):
        self.docs = [join(dir, doc) for doc in listdir(dir) if isfile(join(dir, doc))]
        print self.docs
        return


def main():
    if len(sys.argv) > 1 and isdir(sys.argv[1]):
        corpus = Corpus(sys.argv[1])
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()
