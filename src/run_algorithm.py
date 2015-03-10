import argparse
import datetime
from os import makedirs
from os.path import isdir, exists
from project import corpus, knn_corpus, lda_corpus, word2vec_corpus

algorithms = {"lda": lda_corpus.LDACorpus,
              "knn": knn_corpus.KNNCorpus,
              "w2v": word2vec_corpus.W2VCorpus}

output_loc = "/corpus_out"
dictionary_loc = output_loc + "/corpus.dict"
corpus_loc = output_loc + "/%dcorpus.mm"
log_file = output_loc + "/runtimes.log"


def run_algo(directory, ints, algorithm):
    # Build corpus from largest int and directory (Check valid directory)
    if isdir(directory):
        max_corpus = max(ints)
        if not exists(output_loc):
            makedirs(output_loc)
        log = open(log_file, 'a+')
        base_corpus_file = corpus_loc % max_corpus
        start_time = datetime.datetime.now()
        # Build corpus of size max_corpus
        base_corpus = corpus.Corpus(directory=directory)
        base_corpus.save(dictionary_loc, base_corpus_file)
        end_time = datetime.datetime.now()
        base_corpus_build_time = end_time - start_time
        log.write(("base_corpus_build_time %d:\t" % max_corpus) + str(base_corpus_build_time))
        for size in ints:
            # For each int in the param list then apply the corpus algorithm using a sliced corpus
            test_corpus = algorithms[algorithm](dictionary=dictionary_loc, corpus=base_corpus_file, max_docs=size)
            # Save any mm, index files, etc to a directory so they can be used again.
            # test_corpus.save() TODO: Modify save so it is general accross all algorithms.
            # Log temporal time
            log.write(("%s %d train time:\t" % (algorithm, size)) + test_corpus.get_train_time())


def main():
    parser = argparse.ArgumentParser(description='Build bow corpus on the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    parser.add_argument('algorithm', help='algoritm to apply to the corpus', choices=algorithms)
    args = parser.parse_args()
    run_algo(args.directory, args.integers, args.algorithm)
    else:
        print "Directory argument should be a valid directory"


if __name__ == "__main__": main()