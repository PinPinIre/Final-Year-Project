import sys
from wordcloud import WordCloud
from os.path import isdir, isfile
from corpus import Corpus
from lda_corpus import LDACorpus


class CorpusWordCloud(object):

    def __init__(self, lda_corpus):
        self.corpus = lda_corpus

    def save(self, dictionary, file, lda_file):
        self.corpus.save(dictionary, file, lda_file)

    def get_topics(self, num_words=20):
        topics = self.corpus.print_topics(num_words=num_words)
        return map(WordCloud.parse_topics, topics)

    def draw_topics(self, no_topics=10, num_words=20):
        topics = self.get_topics(num_words=num_words)
        for id, topic in enumerate(topics):
            WordCloud.draw_topic(topic, id)

    @staticmethod
    def parse_topics(string):
        word_topics = {}
        words = unicode.split(string, " + ")
        for word in words:
            word_freq = unicode.split(word, "*")
            if len(word_freq) is 2:
                word_topics[word_freq[1]] = word_freq[0]
        return word_topics

    @staticmethod
    def draw_topic(topic, id):
        wordcloud = WordCloud()
        elements = wordcloud.fit_words(topic.items(), width=120, height=120)
        wordcloud.draw(elements, "gs_topic_%d.png" % (id), width=120, height=120)

    @classmethod
    def load(cls, dictionary, corpus, lda_file):
        return cls(LDACorpus.load(dictionary, corpus, lda_file))


def main():
    if len(sys.argv) > 2 and isdir(sys.argv[1]):
        if not isfile("LDA.mm"):
            if not isfile(sys.argv[2]) and not isfile(sys.argv[3]):
                corpus = Corpus(sys.argv[1])
                corpus.save(sys.argv[2], sys.argv[3])
            corpus = LDACorpus(sys.argv[2], sys.argv[3], no_topics=25)
            wc = CorpusWordCloud(corpus)
            wc.save(sys.argv[2], sys.argv[3], "LDA.mm")
        else:
            wc = CorpusWordCloud.load(sys.argv[2], sys.argv[3], "LDA.mm")
        wc.draw_topics()
    else:
        print "Corpus requires directory as an argument."

if __name__ == "__main__": main()