Final Year Project
=====

My final year project for the Computer Science course in Trinity College Dublin.

The project is assessing the performance of 3 machine learning algorithms for topic-modelling and text clustering.

The algorithms being investigated are:
* LDA (latent Dirichlet allocation)
* KNN (K-Nearest Neighbours)
* Word2Vec

To preprocess the the pdf files run the "src/scripts/process_pdfs.sh" script on the the corpus to convert to plain text. The "src/scripts/sort_corpus.sh" script can then be used to sort the files into directories based on their arXiv topics and genrate a log file of their distributions.

Run the "src/run_algorithm.py" python script to generate the models. Run the src/run_similarity.py python script to query the models.
