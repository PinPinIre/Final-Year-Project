import argparse
from project import corpus, knn_corpus, lda_corpus, word2vec_corpus

algorithms = {"lda": lda_corpus.LDACorpus,
              "knn": knn_corpus.KNNCorpus,
              "w2v": word2vec_corpus.W2VCorpus}

def main():
    parser = argparse.ArgumentParser(description='Build bow corpus on the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    parser.add_argument('algorithm', help='algoritm to apply to the corpus', choices=algorithms)
    args = parser.parse_args()
    # Build corpus from largest int and directory (Check valid directory)
    # For each int in the param list then apply the corpus algorithm using a sliced corpus
    # Save any mm, index files, etc to a directory so they can be used again.
    # Log temporal time


if __name__ == "__main__": main()