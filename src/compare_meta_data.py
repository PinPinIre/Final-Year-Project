import argparse
import json
import re
from os.path import join

file_regex = re.compile("(^[a-z\-]*)")


results_log = "query_results.json"


def extract_arXiv_topic(filename):
    return_topic = ""
    matches = file_regex.match(filename).groups()
    if len(matches) > 0:
        return_topic = matches[0]
    return return_topic


def gen_match_results(query_file, directory):
    match_results = dict()
    with open(query_file) as f:
        json_data = f.read()
    json_file = json.loads(json_data)

    for corpus_name, data in json_file.iteritems():
        match_results[corpus_name] = dict()
        for query, results in data["queries"].iteritems():
            match_results[corpus_name][query] = dict()
            for result in results.itervalues():
                topic = extract_arXiv_topic(result["file"])
                if topic in match_results[corpus_name][query]:
                    match_results[corpus_name][query][topic] += 1
                else:
                    match_results[corpus_name][query][topic] = 1
    json.dump(match_results, open(join(directory, "meta_results.json"), 'w'))


def main():
    parser = argparse.ArgumentParser(description='script to compare similarities generated by run sim')
    parser.add_argument('file', help='input json file')
    parser.add_argument('directory', help='output directory for json.')
    args = parser.parse_args()
    gen_match_results(args.file, args.directory)


if __name__ == "__main__":
    main()