# TDIDT Algorithm for Decision-Tree
Developed in Python
Code can be run from command line
Python Libraries
numpy, copy, random, pickle, graphviz, argparse, sys, string.

All scripts should be in the same folder.  Tree is populated with samples of positive and negative class while training. For pruning tree should already exist in a pickle file in same folder.

## Running the Algorithm:

See 'python tdidt.py --help' for further options
'''
arguments:
-h, --help	show the help message
--data_file : File name. Depends on mode. If mode is ‘train’ then training file name else test file name 
--max_depth : Maximum depth for tree growth.
--mode : String can take one of two values: ‘train’ or ‘test’, ‘train’ mode is for training decision tree and test mode is for evaluating trained tree on test data.
--dot_file_name: Name of file to store dot format of decision tree.
'''
## Train the model
'''
python tdidt.py --data_file gene_expression_training.csv --max_depth 3 --mode train --dot_file_name tree.dot --pickle_file_name tree.pickle
'''
## To generate png file from dot
'''
dot -Tpng tree.dot -o tree.png
'''
## Test the Model
'''
python tdidt.py --data_file gene_expression_test.csv --mode test
'''
## Prunning Decision Tree
'''
Arguements
--mode : String to specify pruning mode: ‘heuristic’ or ‘pessimistic’.
--dot_file_name: If training mode name of file to store dot format of decision tree.
--pickle_file_name: Pickle file for tree
'''

(A) Heuristic Pruning Steps
1. First train the tree on training set.
2. Prune the tree on validation set (this implementation uses training).
3. Test the tree on test set.

(B) Pessimistic Pruning Steps
1. First train the tree on training set.
2. Prune the tree on training set.
3. Test the tree on test set.

## Prune the Model
'''
python prune_tree.py --mode heuristic --dot_file_name prune_heuristic.dot --pickle_file_input tree.pickle --pickle_file_output heuristic_prune_tree.pickle
'''

## Dependencies
1. Python 3.0+
2. Graphviz