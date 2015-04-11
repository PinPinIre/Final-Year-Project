import sys
import datetime
from os.path import isdir, isfile
from corpus import Corpus, PaperCorpus
from gensim import models


# TODO: Investigate the similarity query
class W2VCorpus(object):

    def __init__(self, directory=None, w2v_model=None, list_files=None, max_docs=None, distributions=None, **kwargs):
        if list_files:
            with open(list_files) as f:
                docs = [line.strip() for line in f]
        elif directory and distributions:
            docs = Corpus.get_docs(directory, distributions, max_docs)

        start_time = datetime.datetime.now()
        if not w2v_model:

            self.docs = PaperCorpus(docs)
            # Todo: Tweak the default parameter
            self.model = models.Doc2Vec(self._gen_docs(self.docs), min_count=20, workers=4)
        else:
            self.model = models.Doc2Vec.load(w2v_model)
        end_time = datetime.datetime.now()

        self.train_time = end_time - start_time
        return

    def similarity(self, word, items):
        if not self.model:
            self.model = models.Doc2Vec(self._gen_docs(self.docs), min_count=20, workers=4)
        return self.model.most_similar(word, topn=items)

    def save(self, dictionary_file="w2v_corpus.dict", corpus_file="corpus.mm", sup_file="vector.w2vs"):
        if self.model:
            self.model.save(sup_file)

    @classmethod
    def load(cls, sup_file=None, list_files=None):
        return cls(w2v_model=sup_file, list_files=list_files)

    @staticmethod
    def _gen_docs(docs):
        docs = docs.get_texts()
        for doc_id, doc in enumerate(docs):
            yield models.doc2vec.LabeledSentence(words=doc, labels=['DOC_%s' % doc_id])

    def get_train_time(self):
        return self.train_time

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
