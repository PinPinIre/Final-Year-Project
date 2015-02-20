import sys
import copy
import codecs
from os import listdir
from os.path import isdir, isfile, join, splitext
from nltk.corpus import stopwords
from gensim import models, utils
from gensim.interfaces import TransformationABC
from gensim.corpora import Dictionary, MmCorpus, TextCorpus

ignore_words = stopwords.words("english")


class Corpus(object):
    """Wrapper class around Corpus streaming"""

    def __init__(self, dir=None):
        if dir:
            docs = [join(dir, doc) for doc in listdir(dir) if isfile(join(dir, doc)) and splitext(doc)[-1] == ".txt"]
            """ Construct dictionary without having all texts in memory, based off the example in the Gensim docs"""
            dictionary = Dictionary(filter_common(codecs.open(doc, encoding='utf-8').read().lower().split()) for doc in docs)
            once_words = [id for id, freq in dictionary.dfs.iteritems() if freq is 1]
            dictionary.filter_tokens(once_words)    # Exclude if appears once
            dictionary.compactify()                 # Remove gaps in ids left by removing words
            self.dictionary = dictionary
            self.docs = PaperCorpus(docs)
        else:
            self.dictionary = Dictionary([])
            self.docs = PaperCorpus([])
        self.transformation = IdentityTransformation()
        return

    def __iter__(self):
        # Apply transformation to corpus if it exists
        docs = self.transformation[self.docs]
        if type(self.docs) is PaperCorpus:
            # Need to convert to a vector representation if still in plain text
            for doc in self.docs.get_texts():
                yield self.dictionary.doc2bow(doc)
        else:
            for doc in docs:
                yield doc

    def save(self, dictionary, file):
        # TODO: Investigate saving to another file format, more memory efficient?
        corpus = [vector for vector in self]
        Dictionary.save(self.dictionary, dictionary)
        MmCorpus.serialize(file, corpus)

    def load(self, dictionary, corpus):
        if isfile(dictionary) and isfile(corpus):
            self.dictionary = Dictionary.load(dictionary)
            self.docs = MmCorpus(corpus)
            return True
        return False

    def __len__(self):
        return len(self.docs)

    def transform_corpus(self, transformation):
        """
            Function to transform one corpus representation into another. Applying Transformations can be can be costly
            as they are done on the fly. Save to disk first if access will be frequent

            transformation: Transformation to be applied to the corpus
            returns: Corpus object with transformation applied
        """
        docs = self.transformation[self.docs]
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
            handle = codecs.open(doc, encoding='utf-8')
            yield handle.read().lower().split()


class IdentityTransformation(TransformationABC):
    # Identity transformation which returns the input corpus
    def __getitem__(self, vec):
        return vec


def corpus_equal(corpus1, corpus2):
    if len(corpus1) == len(corpus2):
        for doc1, doc2 in zip(corpus1, corpus2):
            if doc1 != doc2:
                return False
    return True


def filter_common(word_list):
    words = [word for word in word_list if len(word) > 1 and word not in ignore_words]
    return words


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        load_corpus = Corpus()
        corpus = Corpus(sys.argv[1])
        # TODO: Write proper tests

        # Tests if applying a transformation to a non-saved corpus results in a new representation
        tfid_corpus = corpus.transform_corpus(models.TfidfModel)
        # TODO: Fails possibly caused by the corpus not being in a vector representation? Investigate!
        if corpus_equal(corpus, tfid_corpus):
            print "tfid corpus is equal to corpus that hasn't been saved"
        else:
            print "tfid corpus is not equal to corpus that hasn't been saved"

        corpus.save(sys.argv[2], sys.argv[3])
        load_corpus.load(sys.argv[2], sys.argv[3])
        tfid_corpus_load = load_corpus.transform_corpus(models.TfidfModel)

        # Tests if applying a transformation to a saved corpus results in a new representation
        print "Test 2"
        if corpus_equal(load_corpus, tfid_corpus_load):
            print "tfid corpus is equal to corpus that has been saved"
        else:
            print "tfid corpus is not equal to corpus that has been saved"
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()
