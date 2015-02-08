import sys
from os import listdir
from os.path import isdir, isfile, join
from gensim.corpora import Dictionary, MmCorpus


class Corpus(object):
    # TODO: Add a load function
    def __init__(self, dir):
        docs = [join(dir, doc) for doc in listdir(dir) if isfile(join(dir, doc))]
        """ Construct dictionary without having all texts in memory, based off the example in the Gensim docs"""
        dictionary = Dictionary(open(doc).read().lower().split() for doc in docs)
        once_words = [id for id, freq in dictionary.dfs.iteritems() if freq is 1]
        dictionary.filter_tokens(once_words) # Exclude if appears once
        dictionary.compactify() # Remove gaps in ids left by removing words
        self.dictionary = dictionary
        self.docs = docs

    def __iter__(self):
        for doc in self.docs:
            handle = open(doc, "r")
            yield self.dictionary.doc2bow(handle.read().lower().split())

    def save(self, file):
        # TODO: Investigate saving to another file format and save dictionary
        corpus = [vector for vector in self]
        MmCorpus.serialize(file, corpus)


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]):
        corpus = Corpus(sys.argv[1])
        for vector in corpus:
            print vector
        corpus.save(sys.argv[2])
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()
