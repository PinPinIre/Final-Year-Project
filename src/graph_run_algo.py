import dateutil.parser
import time
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from os.path import isdir, join
from operator import add
from datetime import datetime
from gensim import corpora, models, similarities


minute = 60
hour = 3600
cdict = "%scorpus.dict"
ccorpus = "%scorpus.mm"
corpus_model = "%s.%s"
sizes = [1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
knn_sizes = sizes[:7]


def gen_graph(figure, x, y, subtitle, xlabel, ylabel, scale):
    figure.suptitle(subtitle, fontsize=14, fontweight='bold')
    ax = figure.add_subplot(111)
    figure.subplots_adjust(top=0.85)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yscale(scale)
    ax.plot(x, y, linestyle='--', marker='o')


def plt_2(figure, d1, d2, subtitle, xlabel, ylabel, scale):
    x1, y1 = d1
    x2, y2 = d2
    figure.suptitle(subtitle, fontsize=14, fontweight='bold')
    ax = figure.add_subplot(111)
    figure.subplots_adjust(top=0.80)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yscale(scale)
    lda_patch = mpatches.Patch(color='red', label='LDA')
    knn_patch = mpatches.Patch(color='blue', label='kNN')

    plt.legend(handles=[lda_patch, knn_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

    ax.plot(x1, y1, 'r--', x2, y2, 'bs', linestyle='--', marker='o')


def plt_3(figure, d1, d2, d3, subtitle, xlabel, ylabel, scale):
    x1, y1 = d1
    x2, y2 = d2
    x3, y3 = d3
    print "%s %s" % (len(x1), len(y1))
    print "%s %s" % (len(x2), len(y2))
    print "%s %s" % (len(x3), len(y3))
    figure.suptitle(subtitle, fontsize=14, fontweight='bold')
    ax = figure.add_subplot(111)
    figure.subplots_adjust(top=0.80)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yscale(scale)
    lda_patch = mpatches.Patch(color='red', label='LDA')
    knn_patch = mpatches.Patch(color='blue', label='kNN')
    w2v_patch = mpatches.Patch(color='green', label='W2V')

    plt.legend(handles=[lda_patch, knn_patch, w2v_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

    ax.plot(x1, y1, 'r--', x2, y2, 'bs', x3, y3, 'gs', linestyle='--', marker='o')


def load_data(directory, sizes, algorithm):
    dict_file = join(directory, cdict)
    corp_file = join(directory, ccorpus)
    # model_file = join(directory, corpus_model)

    dictionaries = [corpora.Dictionary.load(dict_file % size) for size in sizes]
    corpi = [corpora.MmCorpus(corp_file % size) for size in sizes]
    # corpus_models = [models.ldamodel.LdaModel.load(model_file % (size, algorithm)) for size in sizes]
    dict_sizes = [len(x) for x in dictionaries]
    return dict_sizes, corpi


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
    # directory = join(directory, algorithm)
    corp_dict_size = plt.figure()
    corp_time = plt.figure()
    corp_build = plt.figure()
    total_time = plt.figure()
    total_times, train_times, build_times = read_logfile(join(directory, "runtimes.log"))
    dict_sizes, corpi = load_data(directory, sizes, algorithm)

    gen_graph(corp_dict_size, sizes, dict_sizes, 'Corpus size and dictionary features', "corpus size", "dictionary size", 'linear')
    gen_graph(corp_time, sizes, train_times, 'Corpus size and train time', "number of documents", "training time seconds", 'log')
    gen_graph(corp_build, sizes, build_times, 'Corpus size and build time', "number of documents", "build time seconds", 'log')
    gen_graph(total_time, sizes, total_times, 'Corpus size and total time', "number of documents", "total time seconds", 'log')
    plt.show()


def graph_multiple(directory, sizes):
    figure = plt.figure()
    dir1 = join(directory, "lda.corpus_out")
    dir2 = join(directory, "knn.corpus_out")
    dir3 = join(directory, "w2v.corpus_out")
    total_times1, train_times1, build_times1 = read_logfile(join(dir1, "runtimes.log"))
    total_times2, train_times2, build_times2 = read_logfile(join(dir2, "runtimes.log"))
    total_times3, train_times3, build_times3 = read_logfile(join(dir3, "runtimes.log"))
    #dict_sizes1, corpi1 = load_data(dir1, sizes, "lda")
    #dict_sizes2, corpi2 = load_data(dir2, knn_sizes, "knn")
    #dict_sizes3, corpi3 = load_data(dir3, sizes, "w2v")
    # Slicing is a temporary hack until I read the sizes from the log file rather than the command line
    # plt_2(figure, (sizes, total_times1[:len(sizes)]), (sizes, total_times2[:len(sizes)]), 'Corpus size and total time', "corpus size", "total time", 'linear')
    plt_3(figure, (sizes, total_times1), (knn_sizes, total_times2), (sizes, total_times3), 'Corpus size and train time', "number of documents", "train time seconds", 'linear')
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Graph result from run_algorithm.py')
    parser.add_argument('sizes', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    parser.add_argument('algorithm', help='algorithm to apply to the corpus')
    args = parser.parse_args()
    if args.algorithm != "multiple" and isdir(args.directory):
        graph_results(args.directory, args.sizes, args.algorithm)
    else:
        graph_multiple(args.directory, args.sizes)


if __name__ == "__main__":
    main()
