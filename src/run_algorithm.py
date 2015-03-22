import argparse
import datetime
from os import makedirs, getcwd
from os.path import isdir, exists, join
from project import corpus, knn_corpus, lda_corpus, word2vec_corpus

algorithms = {"lda": lda_corpus.LDACorpus,
              "knn": knn_corpus.KNNCorpus,
              "w2v": word2vec_corpus.W2VCorpus}

base_dir = getcwd()
output_loc = base_dir + "/%s.corpus_out"
dictionary_loc = output_loc + "/%scorpus.dict"
corpus_loc = output_loc + "/%scorpus.mm"
log_file = output_loc + "/runtimes.log"
sup_file_loc = output_loc + "/%d.%s"


def get_file_distributions(directory):
    distributions = dict()
    total = 0
    log = join(directory, "paperstats.log")
    with open(log) as file:
        for line in file:
            name, count = line.split("\t")
            distributions[name] = float(count)
            total = total + float(count)
    distributions["total"] = total
    return distributions


def run_algo(directory, ints, algorithm):
    # Build corpus from largest int and directory (Check valid directory)
    max_corpus = max(ints)
    output_dir = output_loc % algorithm
    if not exists(output_dir):
        makedirs(output_dir)
    log = open(log_file % algorithm, 'a+')
    base_corpus_file = corpus_loc % (algorithm, "base_")
    max_dict = dictionary_loc % (algorithm, "base_")
    distributions = get_file_distributions(directory)
    start_time = datetime.datetime.now()
    if algorithm != "w2v":
        # Build corpus of size max_corpus and save to be reused
        base_corpus = corpus.Corpus(directory=directory, max_docs=max_corpus, distributions=distributions)
        base_corpus.save(max_dict, base_corpus_file)
        directory = None
    end_time = datetime.datetime.now()
    base_corpus_build_time = end_time - start_time
    log.write(("base_corpus_build_time %d:\t" % max_corpus) + str(base_corpus_build_time) + "\n")

    # For each int in the param list then apply the corpus algorithm using a sliced corpus
    for size in ints:
        test_corpus = algorithms[algorithm](directory=directory, dictionary=max_dict, corpus=base_corpus_file, max_docs=size)

        # Save any mm, index files, etc to a directory so they can be used again.
        dict_loc = dictionary_loc % (algorithm, size)
        corp_loc = corpus_loc % (algorithm, size)
        sup_loc = sup_file_loc % (algorithm, size, algorithm)
        test_corpus.save(dictionary_file=dict_loc, corpus_file=corp_loc, sup_file=sup_loc)

        # Log temporal time
        log.write("%s %d train time:\t" % (algorithm, size) + str(test_corpus.get_train_time()) + "\n")
    log.close()


def main():
    parser = argparse.ArgumentParser(description='Build bow corpus on the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    parser.add_argument('algorithm', help='algorithm to apply to the corpus', choices=algorithms)
    args = parser.parse_args()
    if isdir(args.directory):
        run_algo(args.directory, args.integers, args.algorithm)
    else:
        print "Directory argument should be a valid directory"


if __name__ == "__main__":
    main()