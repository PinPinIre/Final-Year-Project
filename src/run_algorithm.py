import argparse
import datetime
from os import makedirs
from os.path import isdir, exists
from project import corpus, knn_corpus, lda_corpus, word2vec_corpus

algorithms = {"lda": lda_corpus.LDACorpus,
              "knn": knn_corpus.KNNCorpus,
              "w2v": word2vec_corpus.W2VCorpus}

output_loc = "/corpus_out"
dictionary_loc = output_loc + "/%dcorpus.dict"
corpus_loc = output_loc + "/%dcorpus.mm"
log_file = output_loc + "/runtimes.log"
sup_file_loc = output_loc + "/%d.%s"


def run_algo(directory, ints, algorithm):
    # Build corpus from largest int and directory (Check valid directory)
    max_corpus = max(ints)
    if not exists(output_loc):
        makedirs(output_loc)
    log = open(log_file, 'a+')
    base_corpus_file = corpus_loc % max_corpus
    start_time = datetime.datetime.now()

    # Build corpus of size max_corpus and save to be reused
    base_corpus = corpus.Corpus(directory=directory, max_docs=max_corpus)
    base_corpus.save(dictionary_loc % max_corpus, base_corpus_file)
    end_time = datetime.datetime.now()
    base_corpus_build_time = end_time - start_time
    log.write(("base_corpus_build_time %d:\t" % max_corpus) + str(base_corpus_build_time))

    # For each int in the param list then apply the corpus algorithm using a sliced corpus
    for size in ints:
        if size is max_corpus: continue
        test_corpus = algorithms[algorithm](dictionary=dictionary_loc, corpus=base_corpus_file, max_docs=size)

        # Save any mm, index files, etc to a directory so they can be used again.
        dict_loc = dictionary_loc % size
        corp_loc = corpus_loc % size
        sup_loc = sup_file_loc % (size, algorithm)
        test_corpus.save(dictionary_file=dict_loc, corpus_file=corp_loc, sup_file=sup_loc)  # TODO: Modify save so it is general accross all algorithms.

        # Log temporal time
        log.write(("%s %d train time:\t" % (algorithm, size)) + test_corpus.get_train_time())
    log.close()


def main():
    parser = argparse.ArgumentParser(description='Build bow corpus on the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    parser.add_argument('algorithm', help='algoritm to apply to the corpus', choices=algorithms)
    args = parser.parse_args()
    if isdir(args.directory):
        run_algo(args.directory, args.integers, args.algorithm)
    else:
        print "Directory argument should be a valid directory"


if __name__ == "__main__": main()