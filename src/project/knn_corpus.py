import sys
import datetime
from os.path import isdir, isfile
from corpus import Corpus
from gensim.matutils import sparse2full
from gensim import models
from annoy import AnnoyIndex
#TODO: Currently using Annoy as was straight forward to set up, investigate FLANN

class KNNCorpus(Corpus):
    no_trees = 10 # TODO: Tweak this Annoy param

    def __init__(self, dictionary=None, corpus=None, index_file=None):
        Corpus.__init__(self, dictionary=dictionary, corpus=corpus)
        # Set up for KNN
        features = len(self.dictionary)
        self.index = AnnoyIndex(features)
        start_time = datetime.datetime.now()
        if not index_file:
            self.transform_corpus(models.TfidfModel)
            for i, vector in enumerate(self):
                dense_vector = sparse2full(vector, features).tolist()
                self.index.add_item(i, dense_vector)
            self.index.build(self.no_trees)
        else:
            self.index.load(index_file)
        end_time = datetime.datetime.now()
        self.train_time = end_time - start_time
        return

    def find_nn(self, doc_no, neighbours):
        return self.index.get_nns_by_item(doc_no, neighbours)

    def save(self, index):
        self.index.save(index)

    @classmethod
    def load(cls, dictionary, corpus, index_file):
        return cls(dictionary=dictionary, corpus=corpus, index_file=index_file)


def main():
    knn_file = "KNN.index"
    if len(sys.argv) > 2 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        if not isfile(knn_file):
            corpus = KNNCorpus(sys.argv[2], sys.argv[3])
            corpus.save(knn_file)
        corpus = KNNCorpus.load(sys.argv[2], sys.argv[3], knn_file)
        print corpus.find_nn(0, 10)
        time = corpus.get_train_time()
        print "KNN Train Time:\t" + str(time)
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()