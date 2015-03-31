import dateutil.parser
import time
import argparse
import matplotlib.pyplot as plt
from os.path import isdir, join
from operator import add
from datetime import datetime
from gensim import corpora, models, similarities


minute = 60
hour = 3600
cdict = "%scorpus.dict"
ccorpus = "%scorpus.mm"
corpus_model = "%s.%s"


def gen_graph(figure, x, y, subtitle, xlabel, ylabel, scale):
    figure.suptitle(subtitle, fontsize=14, fontweight='bold')
    ax = figure.add_subplot(111)
    figure.subplots_adjust(top=0.85)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yscale(scale)
    ax.plot(x, y, linestyle='--', marker='o')


def load_data(directory, sizes, algorithm):
    dict_file = join(directory, cdict)
    corp_file = join(directory, ccorpus)
    model_file = join(directory, corpus_model)

    dictionaries = [corpora.Dictionary.load(dict_file % size) for size in sizes]
    corpi = [corpora.MmCorpus(corp_file % size) for size in sizes]
    corpus_models = [models.ldamodel.LdaModel.load(model_file % (size, algorithm)) for size in sizes]
    dict_sizes = [len(x) for x in dictionaries]
    return dict_sizes, corpus_models, corpi, dictionaries


def read_logfile(path):
    train_times = list()
    build_times = list()
    with open(path) as log_file:
        for i, line in enumerate(log_file):
            bt_time = line.strip().split("\t")[-1]
            hours, mins, seconds = bt_time.split(":")
            total = (hour * int(hours)) + (minute * int(mins)) + float(seconds)
            if (i % 2) == 0:
                train_times.append(total)
            else:
                build_times.append(total)
    total_times = map(add, train_times, build_times)
    return total_times, train_times, build_times


def graph_results(directory, sizes, algorithm):
    corp_dict_size = plt.figure()
    corp_time = plt.figure()
    corp_build = plt.figure()
    total_time = plt.figure()
    total_times, train_times, build_times = read_logfile(join(directory, "runtimes.log"))
    dict_sizes, corpus_models, corpi, dictionaries = load_data(directory, sizes, algorithm)

    gen_graph(corp_dict_size, sizes, dict_sizes, 'Corpus size and dictionary features', "corpus size", "dictionary size", 'log')
    gen_graph(corp_time, sizes, train_times, 'Corpus size and train time', "corpus size", "training time", 'log')
    gen_graph(corp_build, sizes, build_times, 'Corpus size and build time', "corpus size", "build time", 'log')
    gen_graph(total_time, sizes, total_times, 'Corpus size and total time', "corpus size", "total time", 'log')

    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Graph result from run_algorithm.py')
    parser.add_argument('sizes', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    parser.add_argument('algorithm', help='algorithm to apply to the corpus')
    args = parser.parse_args()
    if isdir(args.directory):
        graph_results(args.directory, args.sizes, args.algorithm)
    else:
        print "Directory argument should be a valid directory"


if __name__ == "__main__":
    main()
