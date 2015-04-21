import copy
import matplotlib.pyplot as plt
from gensim import corpora

infrequent_filter = [0, 1, 2, 4, 8, 16, 20, 24, 28, 32]
frequent_filter = [1.0, 0.90, 0.80, 0.70, 0.60, 0.55, 0.50, 0.45]
features_infrequent = list()
features_frequent = list()

base_dictionary = corpora.Dictionary.load("./lda.corpus_out/50000corpus.dict")


def print_np1(n, dictionary):
    print n
    words = [id for id, freq in dictionary.dfs.iteritems() if freq is n + 1]
    for i, word_id in enumerate(words):
        if i == 25: break
        print dictionary.get(word_id)


for feat_filter in infrequent_filter:
    current_dict = copy.deepcopy(base_dictionary)
    current_dict.filter_extremes(no_below=feat_filter, no_above=1.0, keep_n=None)
    features_infrequent.append(len(current_dict))
    print_np1(feat_filter, current_dict)
print "Infrequent"
print zip(infrequent_filter, features_infrequent)

for feat_filter in frequent_filter:
    current_dict = copy.deepcopy(base_dictionary)
    current_dict.filter_extremes(no_below=0, no_above=feat_filter, keep_n=None)
    features_frequent.append(len(current_dict))
print "Frequent"
print zip(frequent_filter, features_frequent)

infreq_figure = plt.figure()
infreq_figure.suptitle("Removal of Infrequent terms", fontsize=14, fontweight='bold')
ax = infreq_figure.add_subplot(111)
# infreq_figure.subplots_adjust(top=0.85)
ax.set_xlabel("Occurence")
ax.set_ylabel("Features")
ax.set_yscale("linear")
ax.plot(infrequent_filter, features_infrequent, linestyle='--', marker='o')

freq_figure = plt.figure()
freq_figure.suptitle("Removal of Frequent terms", fontsize=14, fontweight='bold')
bx = freq_figure.add_subplot(111)
# freq_figure.subplots_adjust(top=0.85)
bx.set_xlabel("In % documents")
bx.set_ylabel("Features")
bx.set_yscale("linear")
bx.plot(frequent_filter, features_frequent, linestyle='--', marker='o')
plt.show()
