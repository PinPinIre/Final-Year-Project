import argparse
import datetime
from os import listdir
from os.path import exists, join
from project import corpus, knn_corpus, lda_corpus, word2vec_corpus
from gensim.corpora import Dictionary

algorithms = {"lda": lda_corpus.LDACorpus,
              "knn": knn_corpus.KNNCorpus}

dictionary_loc = "%scorpus.dict"
corpus_loc = "%scorpus.mm"
sup_file_loc = "%d.%s"

file_logs = "%sfiles.log"
log_file = "sim_runtimes.log"
index_loc = "%d%s.simindex"
query_dict = "query.dict"
query_corp = "query.mm"


def load_queries(query_dir, corp_dict, algorithm):
    '''
    Loads in all of the files in the query directory, converts them to bow and
    returns an array of document vectors.
    '''
    return_vectors = list()
    corp_dict = Dictionary.load(corp_dict)
    valid_files = [join(query_dir, file) for file in listdir(query_dir) if corpus.Corpus._is_corpus_file(query_dir, file)]
    query_corpus = corpus.PaperCorpus(valid_files)
    return_vectors = list()
    for doc in query_corpus.get_texts():
        return_vectors.append(corp_dict.doc2bow(doc))
    return return_vectors


def parse_lda_results(result_vector, directory, size):
    result = ""
    file_list = join(directory, file_logs % size)
    with open(file_list) as file:
        files = file.readlines()
    for index, sim in result_vector:
        result = result + ("%f\t%s\n" % (sim, files[index].strip()))
    return result


def run_sim(ints, algorithm, query_files, directory):
    if not exists(directory):
        print "Output directory for %s must exist already. Run run_algorithm.py first." % algorithm
        return
    log = open(join(directory, log_file), 'a+')
    for size in ints:
        corpus_dict = join(directory, dictionary_loc % size)
        queries = load_queries(query_files, corpus_dict, algorithm)
        corp = join(directory, corpus_loc % size)
        sup_file = join(directory, sup_file_loc % (size, algorithm))
        file_log = join(directory, file_logs % size)
        test_corpus = algorithms[algorithm].load(dictionary_file=corpus_dict, corpus_file=corp, sup_file=sup_file)

        start_time = datetime.datetime.now()
        for i, query in enumerate(queries):
            most_sim = test_corpus.run_query(query, index_loc % (size, algorithm), 10)
            if algorithm == "lda":
                print parse_lda_results(most_sim, directory, size)
            # TODO: Log the similarities to a file for inspection
        end_time = datetime.datetime.now()

        query_time = end_time - start_time
        log.write("%s %d query time:\t" % (algorithm, size) + str(query_time) + "\n")
    log.close()


def main():
    parser = argparse.ArgumentParser(description='Run queries on bow corpus generated from the arxiv corpus.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='size values for the corpus')
    parser.add_argument('query', help='directory for the query files')
    parser.add_argument('directory', help='directory for pre processed model files')
    parser.add_argument('algorithm', help='algorithm to apply to the corpus', choices=algorithms)
    args = parser.parse_args()
    run_sim(args.integers, args.algorithm, args.query, args.directory)


if __name__ == "__main__":
    main()
