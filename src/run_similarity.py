import argparse
import datetime
from os import getcwd
from os.path import isdir, exists
from project import corpus, knn_corpus, lda_corpus, word2vec_corpus

algorithms = {"lda": lda_corpus.LDACorpus,
              "knn": knn_corpus.KNNCorpus,
              "w2v": word2vec_corpus.W2VCorpus}

base_dir = getcwd()
output_loc = base_dir + "/%s.corpus_out"
dictionary_loc = output_loc + "/%scorpus.dict"
corpus_loc = output_loc + "/%scorpus.mm"
log_file = output_loc + "/Sim_runtimes.log"
sup_file_loc = output_loc + "/%d.%s"


def run_sim(ints, algorithm):
    output_dir = output_loc % algorithm
    if not exists(output_dir):
        print "Output directory for %s must exist already. Run run_algorithm.py first." % algorithm
        return
    log = open(log_file % algorithm, 'a+')
    for size in ints:
        corpus_dict = dictionary_loc % (algorithm, size)
        corpus = corpus_loc % (algorithm, size)
        sup_file = sup_file_loc % (algorithm, size, algorithm)
        test_corpus = algorithms[algorithm].load(dictionary_file=corpus_dict, corpus_file=corpus, sup_file=sup_file)
        # Run some queries on the corpus

        # Log temporal time
        # log.write("%s %d query time:\t" % (algorithm, size) + str(test_corpus.get_train_time()) + "\n")
    log.close()


def main():
    parser = argparse.ArgumentParser(description='Run queries on bow corpus generated from the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('algorithm', help='algorithm to apply to the corpus', choices=algorithms)
    args = parser.parse_args()
    run_sim(args.integers, args.algorithm)


if __name__ == "__main__":
    main()