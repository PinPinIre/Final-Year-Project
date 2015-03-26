import sys
import datetime
from os.path import isdir, isfile
from corpus import Corpus, PaperCorpus
from gensim import models


# TODO: Investigate the similarity query
class W2VCorpus(object):

    def __init__(self, directory=None, w2v_model=None, max_docs=None, **kwargs):
        docs = Corpus.get_docs(directory, distributions, max_docs)
        self.docs = PaperCorpus(docs)
        start_time = datetime.datetime.now()
        if not w2v_model:
            # Todo: Tweak the default parameter
            self.model = models.Doc2Vec(self._gen_docs(self.docs), size=100, window=5, min_count=5, workers=4)
        else:
            self.model = models.Doc2Vec.load(w2v_model)
        end_time = datetime.datetime.now()
        self.train_time = end_time - start_time
        return

    def similarity(self, word):
        if self.model:
            return self.model.most_similar(word)
        else:
            # Todo: Raise exception?
            return None

    def save(self, dictionary_file="w2v_corpus.dict", corpus_file="corpus.mm", sup_file="vector.w2vs"):
        if self.model:
            self.model.save(sup_file)

    @classmethod
    def load(cls, dictionary_file=None, corpus_file=None, sup_file=None):
        return cls(dictionary=dictionary_file, corpus=corpus_file, w2v_model=sup_file)

    @staticmethod
    def _gen_docs(docs):
        docs = docs.get_texts()
        for doc_id, doc in enumerate(docs):
            yield models.doc2vec.LabeledSentence(words=doc, labels=['DOC_%s' % doc_id])

    def run_query(self, query, index_location, best_matches):
        return self.similarity(query)


def main():
    w2v = "w2vcorpus.w2v"
    if len(sys.argv) is 4 and isdir(sys.argv[1]):
        if not isfile(w2v):
            corpus = W2VCorpus(directory=sys.argv[1])
            corpus.save(dictionary_file=sys.argv[2], corpus_file=sys.argv[3], sup_file=w2v)
        else:
            corpus = W2VCorpus.load(dictionary_file=sys.argv[2], corpus_file=sys.argv[3], sup_file=w2v)
        time = corpus.get_train_time()
        print "W2V Train Time:\t" + str(time)
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__":
    main()
