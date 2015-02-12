import sys
import copy
from os import listdir
from os.path import isdir, isfile, join
from gensim import models
from gensim.corpora import Dictionary, MmCorpus, TextCorpus


class Corpus(object):
    """Wrapper class around Corpus streaming"""

    def __init__(self, dir=None):
        if dir:
            docs = [join(dir, doc) for doc in listdir(dir) if isfile(join(dir, doc))]
            """ Construct dictionary without having all texts in memory, based off the example in the Gensim docs"""
            dictionary = Dictionary(open(doc).read().lower().split() for doc in docs)
            once_words = [id for id, freq in dictionary.dfs.iteritems() if freq is 1]
            dictionary.filter_tokens(once_words)    # Exclude if appears once
            dictionary.compactify()                 # Remove gaps in ids left by removing words
            self.dictionary = dictionary
            self.docs = PaperCorpus(docs)
        else:
            self.dictionary = Dictionary([])
            self.docs = PaperCorpus([])
        self.transformation = None
        return

    def __iter__(self):
        # Apply transformation to corpus if it exists
        if self.transformation:
            docs = self.transformation[self.docs]
        else:
            docs = self.docs
        if type(self.docs) is PaperCorpus:
            # Need to convert to a vector representation if still in plain text
            for doc in self.docs.get_texts():
                yield self.dictionary.doc2bow(doc)
        else:
            for doc in docs:
                yield doc

    def save(self, file):
        # TODO: Investigate saving to another file format, more memory efficient?
        corpus = [vector for vector in self]
        MmCorpus.serialize(file, corpus)
        Dictionary.save(self.dictionary, file+".dict")

    def load(self, dictionary, corpus):
        if isfile(dictionary) and isfile(corpus):
            self.dictionary = Dictionary.load(dictionary)
            self.docs = MmCorpus(corpus)
            return True
        return False

    def transform_corpus(self, transformation):
        """
            Function to transform one corpus representation into another
            transformation: Transformation to be applied to the corpus
            returns: Corpus object with transformation applied
        """
        # Todo: Further investigate applying transformations to transformations - currently apply current before creating new one
        if self.transformation:
            docs = self.transformation[self.docs]
        else:
            docs = self.docs
        transformed_model = transformation(docs)
        new_corpus = Corpus()
        new_corpus.dictionary = copy.copy(self.dictionary)
        new_corpus.docs = copy.copy(docs)
        new_corpus.transformation = transformed_model
        return new_corpus

class PaperCorpus(TextCorpus):
    # Wrap plain text document streaming - allows us to apply transformations to it
    def get_texts(self):
        for doc in self.input:
            handle = open(doc, "r")
            yield handle.read().lower().split()

def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]):
        corpus = Corpus(sys.argv[1])
        load_corpus = Corpus()
        # TODO: Write proper tests
        print "Testing Plain Text Corpus"
        for vector in corpus:
            print vector
        corpus.save(sys.argv[2])
        print "Testing Load Corpus empty"
        for vector in load_corpus:
            print vector
        print "Testing Load Corpus after MMload"
        load_corpus.load(sys.argv[2]+".dict", sys.argv[2])
        for vector in load_corpus:
            print vector
        print "Testing Plain Text Transformation Corpus"
        transformed_corpus = corpus.transform_corpus(models.TfidfModel)
        for vector in transformed_corpus:
            # TODO: Output currently equals input, investigate this.
            print vector
        print "Testing Load Transformation MMCorpus"
        transformed_corpus = load_corpus.transform_corpus(models.TfidfModel)
        for vector in transformed_corpus:
            print vector
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()
