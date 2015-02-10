import sys
from os import listdir
from os.path import isdir, isfile, join
from gensim.corpora import Dictionary, MmCorpus


class Corpus(object):
    """Wrapper class around Corpus streaming"""

    def __init__(self, dir=None):
        if dir:
            docs = [join(dir, doc) for doc in listdir(dir) if isfile(join(dir, doc))]
            """ Construct dictionary without having all texts in memory, based off the example in the Gensim docs"""
            dictionary = Dictionary(open(doc).read().lower().split() for doc in docs)
            once_words = [id for id, freq in dictionary.dfs.iteritems() if freq is 1]
            dictionary.filter_tokens(once_words) # Exclude if appears once
            dictionary.compactify() # Remove gaps in ids left by removing words
            self.dictionary = dictionary
            self.docs = docs
        else:
            self.dictionary = []
            self.docs = []
        return

    def __iter__(self):
        if type(self.docs) is list:
            for doc in self.docs:
                handle = open(doc, "r")
                yield self.dictionary.doc2bow(handle.read().lower().split())
        else:
            for doc in self.docs:
                yield doc

    def save(self, file):
        # TODO: Investigate saving to another file format
        corpus = [vector for vector in self]
        MmCorpus.serialize(file, corpus)
        Dictionary.save(self.dictionary, file+".dict")

    def load(self, dictionary, mm):
        if isfile(dictionary) and isfile(mm):
            self.dictionary = Dictionary.load(dictionary)
            self.docs = MmCorpus(mm)
            return True
        return False

    def transform_corpus(self, transformation):
        """Function to transform one corpus into another"""
        # TODO: Handle the transformation from one representation to another, transformations can be applied on top
        # TODO: of each other so this must also be considered. Maybe track current representation in corpus class?
        return self


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]):
        corpus = Corpus(sys.argv[1])
        for vector in corpus:
            print vector
        corpus.save(sys.argv[2])
        load_corpus = Corpus()
        print "Testing Load Corpus empty"
        for vector in load_corpus:
            print vector
        print "Testing Load Corpus after load"
        load_corpus.load(sys.argv[2]+".dict", sys.argv[2])
        for vector in load_corpus:
            print vector
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()
