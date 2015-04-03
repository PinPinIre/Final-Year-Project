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
        return map(CorpusWordCloud.parse_topics, topics)

    def draw_topics(self, path, no_topics=10, num_words=30):
        topics = self.get_topics(num_words=num_words)
        for id_t, topic in enumerate(topics):
            CorpusWordCloud.draw_topic(topic, id_t, path)

    @staticmethod
    def parse_topics(string):
        word_topics = {}
        words = unicode.split(string, " + ")
        for word in words:
            word_freq = unicode.split(word, "*")
            if len(word_freq) is 2:
                word_topics[word_freq[1]] = float(word_freq[0])
        return word_topics

    @staticmethod
    def draw_topic(topic, t_id, outputdir):
        wordcloud = WordCloud(width=500, height=500, font_path="/System/Library/Fonts/Monaco.dfont", background_color="black")
        elements = wordcloud.fit_words(topic.items())
        wordcloud.to_file(outputdir + str(t_id) + ".png")

    @classmethod
    def load(cls, dictionary, corpus, lda_file):
        return cls(LDACorpus.load(dictionary_file=dictionary, corpus_file=corpus, sup_file=lda_file))


def main():
    if len(sys.argv) is 5:
        dictionary = sys.argv[1]
        corpus = sys.argv[2]
        sup = sys.argv[3]
        out = sys.argv[4]
        wc = CorpusWordCloud.load(dictionary, corpus, sup)
        wc.draw_topics(out, num_words=40)
        print "Success!"
    else:
        print sys.argv

if __name__ == "__main__":
    main()
