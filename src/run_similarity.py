import argparse
import datetime
from os import getcwd
from os.path import exists
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
index_loc = output_loc + "/%d%s.simindex"
query_dict = output_loc + "/query.dict"
query_corp = output_loc + "query.mm"


def load_queries(query_dir, dictionary, algorithm):
    if algorithm != "w2v":
        query_corpus = corpus.Corpus(directory=query_dir, dictionary=dictionary)
    else:
        docs = corpus.Corpus.get_docs(query_dir)
        query_corpus = corpus.PaperCorpus(docs).get_texts()
    return query_corpus


def run_sim(ints, algorithm, query_files, corpus_dir):
    output_dir = output_loc % algorithm
    if not exists(output_dir):
        print "Output directory for %s must exist already. Run run_algorithm.py first." % algorithm
        return
    log = open(log_file % algorithm, 'a+')
    max_dict = dictionary_loc % (algorithm, "base_")
    queries = load_queries(query_files, max_dict, algorithm)
    for size in ints:
        corpus_dict = dictionary_loc % (algorithm, size)
        corp = corpus_loc % (algorithm, size)
        sup_file = sup_file_loc % (algorithm, size, algorithm)
        if algorithm != "w2v":
            test_corpus = algorithms[algorithm].load(dictionary_file=corpus_dict, corpus_file=corp, sup_file=sup_file)
        else:
            test_corpus = algorithms[algorithm](directory=corpus_dir, max_docs=size)

        start_time = datetime.datetime.now()
        for i, query in enumerate(queries):
            most_sim = test_corpus.run_query(query, index_loc % (algorithm, size, algorithm), 10)
            print most_sim
            # TODO: Log the similarities to a file for inspection
        end_time = datetime.datetime.now()

        query_time = end_time - start_time
        log.write("%s %d query time:\t" % (algorithm, size) + str(query_time) + "\n")
    log.close()


def main():
    parser = argparse.ArgumentParser(description='Run queries on bow corpus generated from the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('directory', help='directory for the query files')
    parser.add_argument('algorithm', help='algorithm to apply to the corpus', choices=algorithms)
    parser.add_argument('corp_directory', help='directory for the arxiv corpus files')
    args = parser.parse_args()
    run_sim(args.integers, args.algorithm, args.directory, args.corp_directory)


if __name__ == "__main__":
    main()