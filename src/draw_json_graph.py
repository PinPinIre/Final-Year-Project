import json
import networkx as nx
from networkx.readwrite import json_graph

with open("/query_results.json") as f:
    json_data = f.read()
x = json.loads(json_data)
doc_graphs = list()

for corpus_name, data in x.iteritems():
    for query, results in data["queries"].iteritems():
        new_graph = nx.Graph()
        new_graph.add_node(query)

        for result in results.itervalues():
            new_graph.add_node(result["file"])
            if "similarity" in results:
                sim = results["similarity"]
            else:
                print "no sim"
                sim = 1
            print sim
            new_graph.add_edge(query, result["file"], weight=sim)

        doc_graphs.append(new_graph)

for graph in doc_graphs:
    for n in graph:
        graph.node[n]['name'] = n
        similarity_graph_json = json_graph.node_link_data(graph)
        # Todo: Save json file
