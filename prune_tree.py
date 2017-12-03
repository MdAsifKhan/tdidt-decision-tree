
import copy
import pickle
import numpy as np
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
from tdidt import plot_tree
import sys

def prune_tree(node, thresh, parent=None):
	if node['name'] == 'LEAF':
		leaf_value = node['value']
		th1 = leaf_value[1]/float(np.sum(leaf_value))
		if th1<thresh:
			parent['name'] = 'LEAF'
			parent['children'] = []
			value = parent['value']
			parent['label'] = value.index(max(value))

	name = node['name']
	value = node['value']	
	for children in node['children']:
		thresh = value[1]/float(np.sum(value))
		prune_tree(children, thresh, node)

def pessimistic_error(value):
	z = 0.674
	n = np.sum(value)
	observed_error = min(value)/n
	pess_error = observed_error + np.power(z,2)/(2*n) + z*np.sqrt(observed_error/n -np.power(observed_error,2)/n+ np.power(z/(2*n),2))
	pess_error = pess_error/ (1+np.power(z,2)/n)
	return pess_error

def prune_tree_pessimistic(node, prune_error, parent=None):
	if node['name'] == 'LEAF':
		leaf_value = node['value']
		leaf_error = pessimistic_error(leaf_value)
		if leaf_error>prune_error:
			parent['name'] = 'LEAF'
			parent['children'] = []
			value = parent['value']
			parent['label'] = value.index(max(value))

	value = node['value']	
	for children in node['children']:
		prune_error = pessimistic_error(value)
		prune_tree_pessimistic(children, prune_error, node)

def process_scripts(args):

	mode =args.mode
	output_file = args.dot_file_name
	tree_file = args.pickle_file_input
	tree_file_output = args.pickle_file_output
	tree = pickle.load(open(tree_file,'rb'))
	tree1 = copy.deepcopy(tree)
	if mode =='heuristic':
		prune_tree(tree1, thresh = 0, parent=None)
		pickle.dump(tree1, open(tree_file_output,'wb'))		
		plot_tree(output_file, tree1)
	elif mode=='pessimistic':
		prune_tree_pessimistic(tree1, prune_error=1, parent=None)
		pickle.dump(tree1, open(tree_file_output,'wb'))		
		plot_tree(output_file, tree1)	
	else:
		print('Undefined Mode')


def main():
	parser = ArgumentParser('prune_tree',
							formatter_class=ArgumentDefaultsHelpFormatter,
								conflict_handler='resolve')

	parser.add_argument('--mode', default='heuristic', type=str,
                      help='heuristic or pessimistic')

	parser.add_argument('--dot_file_name', required=True, 
                      help='If training mode name of dot file to contain tree')

	parser.add_argument('--pickle_file_input', 
                      help='Pickle file for Input tree')

	parser.add_argument('--pickle_file_output', 
                      help='Pickle file for Pruned tree')	
	args = parser.parse_args()
	process_scripts(args)


if __name__ == '__main__':
	sys.exit(main()) 