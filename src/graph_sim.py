import dateutil.parser
import time
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from os.path import isdir, join
from datetime import datetime

minute = 60
hour = 3600
corpus_model = "%s.%s"
sizes = [10000, 20000, 30000, 40000, 50000]
knn_sizes = sizes[:3]


def plt_3(figure, d1, d3, subtitle, xlabel, ylabel, scale):
    x1, y1 = d1
    x3, y3 = d3
    figure.suptitle(subtitle, fontsize=14, fontweight='bold')
    ax = figure.add_subplot(111)
    figure.subplots_adjust(top=0.80)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yscale(scale)
    lda_patch = mpatches.Patch(color='red', label='LDA')
    w2v_patch = mpatches.Patch(color='green', label='W2V')

    plt.legend(handles=[lda_patch, w2v_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

    ax.plot(x1, y1, 'r--', x3, y3, 'gs', linestyle='--', marker='o')


def read_logfile(path):
    times = list()
    with open(path) as log_file:
        for i, line in enumerate(log_file):
            bt_time = line.strip().split("\t")[-1]
            hours, mins, seconds = bt_time.split(":")
            total = (hour * int(hours)) + (minute * int(mins)) + float(seconds)
            times.append(total)
    return times


def graph_multiple(directory):
    figure = plt.figure()
    dir1 = join(directory, "lda.corpus_out")
    dir2 = join(directory, "knn.corpus_out")
    dir3 = join(directory, "w2v.corpus_out")
    times1 = read_logfile(join(dir1, "sim_runtimes.log"))
    times2 = read_logfile(join(dir2, "sim_runtimes.log"))
    times3 = read_logfile(join(dir3, "sim_runtimes.log"))
    plt_3(figure, (sizes, times1), (sizes, times3), 'Corpus size and query time', "number of documents", "query time seconds", 'linear')
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Graph result from run_algorithm.py')
    parser.add_argument('directory', help='directory for the arxiv txt files')
    args = parser.parse_args()
    graph_multiple(args.directory)


if __name__ == "__main__":
    main()
