import argparse
import datetime
from os import makedirs, getcwd
from shutil import move
from os.path import isdir, exists, join
from project import corpus, knn_corpus, lda_corpus, word2vec_corpus

algorithms = {"lda": lda_corpus.LDACorpus,
              "knn": knn_corpus.KNNCorpus,
              "w2v": word2vec_corpus.W2VCorpus}

base_dir = getcwd()
output_loc = base_dir + "/%s.corpus_out"
dictionary_loc = output_loc + "/%scorpus.dict"
corpus_loc = output_loc + "/%scorpus.mm"
sup_file_loc = output_loc + "/%d.%s"

file_logs = output_loc + "/%sfiles.log"
log_file = output_loc + "/runtimes.log"


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


def run_algo(directory, ints, algorithm, move_dir=None):
    # Build corpus from largest int and directory (Check valid directory)
    max_corpus = max(ints)
    output_dir = output_loc % algorithm
    if not exists(output_dir):
        makedirs(output_dir)
    log = open(log_file % algorithm, 'a+')
    distributions = get_file_distributions(directory)

    # For each int in the param list then apply the corpus algorithm using a sliced corpus
    for size in ints:
        new_directory = directory
        corpus_file = corpus_loc % (algorithm, size)
        corp_dict = dictionary_loc % (algorithm, size)
        sup_loc = sup_file_loc % (algorithm, size, algorithm)
        file_log = file_logs % (algorithm, size)
        start_time = datetime.datetime.now()

        if algorithm != "w2v":
            # Build corpus of size max_corpus and save to be reused
            current_corpus = corpus.Corpus(directory=directory, max_docs=size, distributions=distributions)
            current_corpus.save(dictionary_file=corp_dict, corpus_file=corpus_file, sup_file=file_log)
            new_directory = None
        end_time = datetime.datetime.now()

        current_corpus_build_time = end_time - start_time
        log.write("%s_corpus_build_time:\t%d\t%s\n" % (algorithm, size, current_corpus_build_time))
        log.flush()

        test_corpus = algorithms[algorithm](directory=new_directory, dictionary=corp_dict, corpus=corpus_file, max_docs=size, distributions=distributions)
        if algorithm != "w2v":
            test_corpus.save(sup_file=sup_loc)
        else:
            test_corpus.save(sup_file=sup_loc, dictionary_file=file_log)
        # Log temporal time
        log.write("%s_train_time:\t%d\t%s\n" % (algorithm, size, test_corpus.get_train_time()))
        log.flush()
        if move_dir:
            # It was noticed that KNN could generate a large index file, this can move to an external drive without affecting times
            move(corpus_file, move_dir)
            move(corp_dict, move_dir)
            move(sup_loc, move_dir)
            move(file_log, move_dir)
    log.close()


def main():
    parser = argparse.ArgumentParser(description='Build bow corpus on the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    parser.add_argument('algorithm', help='algorithm to apply to the corpus', choices=algorithms)
    parser.add_argument('--movedir', help='optional directory to move outputed files to', default=None)
    args = parser.parse_args()
    if isdir(args.directory):
        run_algo(args.directory, args.integers, args.algorithm, args.movedir)
    else:
        print "Directory argument should be a valid directory"


if __name__ == "__main__":
    main()
