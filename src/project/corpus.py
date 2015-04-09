import sys
import codecs
from os import listdir
from os.path import isdir, isfile, join, splitext
from random import sample
from math import ceil
from nltk.corpus import stopwords
from gensim.interfaces import TransformationABC
from gensim.corpora import Dictionary, MmCorpus, TextCorpus
from gensim.utils import ClippedCorpus

ignore_words = stopwords.words("english")


class Corpus(object):
    """Wrapper class around Corpus streaming"""

    def __init__(self, directory=None, dictionary=None, distributions=None, corpus=None, max_docs=None):
        if directory:
            docs = self.get_docs(directory, distributions, max_docs)
            if not dictionary:
                """ Construct dictionary without having all texts in memory, based off the example in the Gensim docs"""
                dictionary = Dictionary(filter_common(codecs.open(doc, encoding='utf-8').read().lower().split()) for doc in docs)
                once_words = [id for id, freq in dictionary.dfs.iteritems() if freq is 1]
                dictionary.filter_tokens(once_words)     # Exclude if appears once
                dictionary.compactify()                  # Remove gaps in ids left by removing words
                dictionary.filter_extremes(no_below=20, no_above=0.75, keep_n=None)  # Filter if in less than 20 docs and if in more than 75%
                self.dictionary = dictionary
            else:
                self.dictionary = Dictionary.load(dictionary)
            self.docs = PaperCorpus(docs)
        elif dictionary and corpus:
            self.dictionary = Dictionary.load(dictionary)
            self.docs = MmCorpus(corpus)
        else:
            self.dictionary = Dictionary([])
            self.docs = PaperCorpus([])
        self.transformation = IdentityTransformation()
        self.train_time = None
        self.sim_index = None
        return

    def __iter__(self):
        # Apply transformation to corpus if it exists
        self.docs = self.transformation[self.docs]
        if type(self.docs) is PaperCorpus:
            # Need to convert to a vector representation if still in plain text
            for doc in self.docs.get_texts():
                yield self.dictionary.doc2bow(doc)
        else:
            docs = self.transformation[self.docs]
            for doc in docs:
                yield doc

    def save(self, dictionary_file="corpus.dict", corpus_file="corpus.mm", sup_file=None):
        if dictionary_file:
            Dictionary.save(self.dictionary, dictionary_file)
        if corpus_file:
            MmCorpus.serialize(corpus_file, self)
        if sup_file and type(self.docs) is PaperCorpus:
            self.docs.save(sup_file)

    @classmethod
    def load(cls, dictionary_file=None, corpus_file=None, sup_file=None):
        if isfile(dictionary_file) and isfile(corpus_file):
            return cls(dictionary=dictionary_file, corpus=corpus_file)
        return False

    def __len__(self):
        return len(self.docs)

    def transform_corpus(self, transformation):
        """
        Function to transform one corpus representation into another. Applying Transformations can be can be costly
        as they are done on the fly. Save to disk first if access will be frequent

        :param transformation: Transformation to be applied to the corpus
        :return:
        """
        self.docs = self.transformation[self.docs]
        transformed_model = transformation(self.docs)
        self.transformation = transformed_model
        return

    def clip_corpus(self, max_docs=None):
        """
        Function to clip a copus to a max size, if max_doc is none then the the corpus remains it's current size

        :param max_docs:
        :return:
        """
        self.docs = ClippedCorpus(self.docs, max_docs)

    def get_train_time(self):
        return self.train_time

    def _build_sim_index(self, index_dir=None, num_features=None):
        pass

    @staticmethod
    def _is_corpus_file(directory, doc):
        return isfile(join(directory, doc)) and splitext(doc)[-1] == ".txt"

    @staticmethod
    def get_docs(directory, distributions=None, max_docs=None):
        if distributions:
            if max_docs and distributions and max_docs <= distributions["total"]:
                max_dis = max_docs / distributions["total"]
            else:
                max_dis = 1
            docs = list()
            for name in distributions:
                if name is "total":
                    continue
                current_dir = join(directory, name)
                temp = [join(current_dir, doc) for doc in listdir(current_dir) if Corpus._is_corpus_file(current_dir, doc)]
                select_amount = int(ceil(len(temp) * max_dis))
                docs.extend(sample(temp, select_amount))
        else:
            docs = [join(directory, doc) for doc in listdir(directory) if Corpus._is_corpus_file(directory, doc)]
        return docs


class PaperCorpus(TextCorpus):
    # Wrap plain text document streaming - allows us to apply transformations to it
    def get_texts(self):
        for doc in self.input:
            handle = codecs.open(doc, encoding='utf-8')
            yield filter_common(handle.read().lower().split())

    def save(self, sup_file):
        file_log = open(sup_file, 'a+')
        for doc in self.input:
            file_log.write("%s\n" % doc)
        file_log.close()


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
    words = [word for word in word_list if len(word) > 1]
    return words


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        load_corpus = Corpus()
        corpus = Corpus(directory=sys.argv[1])
        # TODO: Write proper tests
        # corpus.transform_corpus(models.TfidfModel)
        corpus.save(dictionary_file=sys.argv[2], corpus_file=sys.argv[3])
        load_corpus.load(dictionary_file=sys.argv[2], corpus_file=sys.argv[3])
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__":
    main()
