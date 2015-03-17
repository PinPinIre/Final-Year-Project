import sys
import datetime
from os.path import isdir, isfile
from gensim import models
from corpus import Corpus
from gensim.similarities import Similarity


class LDACorpus(Corpus):

    def __init__(self, dictionary=None, corpus=None, lda_corpus=None, no_topics=100, update=1, chunksize=10000, passes=1, max_docs=None, **kwargs):
        Corpus.__init__(self, dictionary=dictionary, corpus=corpus)
        self.clip_corpus(max_docs)
        self.no_topics = no_topics
        self.update = update
        self.chunksize = chunksize
        self.passes = passes
        self.dict_loc = dictionary
        self.vec_loc = corpus
        start_time = datetime.datetime.now()
        if not lda_corpus:
            self.transform_corpus(models.TfidfModel)
            self.model = self.train_model()
        else:
            self.model = models.ldamodel.LdaModel.load(lda_corpus)
        end_time = datetime.datetime.now()
        self.train_time = end_time - start_time

    def print_topics(self, num_words=10):
        if self.model: return self.model.print_topics(100, num_words=num_words)

    def train_model(self):
        return models.ldamodel.LdaModel(corpus=self, id2word=self.dictionary, num_topics=self.no_topics, iterations=500)

    def save(self, dictionary_file=None, corpus_file=None, sup_file="topics.lda"):
        Corpus.save(self, dictionary_file, corpus_file)
        self.model.save(sup_file)

    @classmethod
    def load(cls, dictionary_file=None, corpus_file=None, sup_file=None):
        return cls(dictionary=dictionary_file, corpus=corpus_file, lda_corpus=sup_file)

    def _build_sim_index(self, index_dir="corpusindex", num_features=None):
        if not num_features: num_features = self.no_topics
        self.sim_index = Similarity(index_dir, self, num_features=num_features)


def main():
    if len(sys.argv) is 5 and isdir(sys.argv[1]) and isfile(sys.argv[2]) and isfile(sys.argv[3]):
        if isfile(sys.argv[4]):
            # Load model if file exists
            corpus = LDACorpus.load(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            # Otherwise build LDA model
            corpus = LDACorpus(dictionary=sys.argv[2], corpus=sys.argv[3], no_topics=100)
            corpus.save(sup_file="LDA.lda")
        time = corpus.get_train_time()
        print "LDA Train Time:\t" + str(time)
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()