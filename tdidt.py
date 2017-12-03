import numpy as np
import copy
import random
import pickle
import graphviz as gv
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
import sys
import string

def read_data(filename):

	file = [line.strip().split(',') for line in open(filename,'r')]
	feature_names = file[0][:-1]

	data = [[float(el) for el in row[:-1]] for row in file[1:]]
	class_label = [float(row[-1]) for row in file[1:]]

	return data, class_label, feature_names

def calc_entropy(freq):
	p = [i/float(sum(freq)) for i in list(freq)]
	entropy = 0.0
	for p_i in p:
		if p_i!=0:
			entropy += p_i * np.log2(1/p_i)
	return entropy 


def calc_info_gain(attribute, class_label):

	unique_class = list(set(class_label))
	unique_attribute = list(set(attribute))

	freq_matrix = np.zeros((len(unique_attribute), len(unique_class)))
	for attr, label in zip(attribute, class_label):
		freq_matrix[unique_attribute.index(attr), unique_class.index(label)] += 1

	#Compute H(S)
	h_s = calc_entropy(freq_matrix.sum(axis=0))
	#Conditional Entropy H(S/A)
	h_s_a = 0.0
	for i in range(freq_matrix.shape[0]):
		h_s_a += sum(freq_matrix[i,:])/float(len(attribute))*calc_entropy(freq_matrix[i,:])

	gain = h_s - h_s_a
	return gain

def best_split(attribute, label):

	#Sort according to current attribute
	#sorted_attribute, sorted_label = zip(*sorted(zip(attribute, label)))
	#sorted_attribute = list(sorted_attribute)
	#sorted_label = list(sorted_label)
	data = sorted([ (attribute[i],label[i]) for i in range(len(attribute)) ], key = lambda l: l[0])

	sorted_attribute = []
	sorted_label = []
	for tup in data:
		sorted_attribute.append(tup[0])
		sorted_label.append(tup[1])

	split_candidates = []
	#Find break 'c'
	split_label = sorted_label[0]
	for c in range(1,len(sorted_attribute)):
		if sorted_label[c] != split_label:
			discrete_attribute = [0]*c + [1]*(len(sorted_attribute)-c)
			split_candidates.append((c, calc_info_gain(discrete_attribute, sorted_label)))
		split_label = sorted_label[c]

	#Find the split with the maximum information gain
	best_split = max(split_candidates,key=lambda item:item[1])
	#Computing the mean of attribute at break
	if best_split[0]>0:
		avg_attribute = (float(sorted_attribute[best_split[0]-1]) + float(sorted_attribute[best_split[0]]))/2
	else:
		avg_attribute  = sorted_attribute[best_split[0]]

	#Return the attribute value (average of 2 example in case of break) and its information gain
	return avg_attribute, best_split[1]

def best_attribute(data, class_label):
	attribute_info_gain = []
	for idx, attribute in enumerate(np.array(data).T.tolist()):
		attr_value, info_g = best_split(attribute, class_label)
		attribute_info_gain.append([attr_value, info_g, idx])
	# Choose which attribute is best using information gain
	best_attr = max(attribute_info_gain,key=lambda gain:gain[1])
	
	return best_attr

def data_split(data, class_label, best_attribute):
	#Divide the data based on this attribute
	data_left = []
	data_right = []
	label_left = []
	label_right = []
	for i in range(len(data)):
		#reduced_data = copy.copy(data[i])
		#reduced_data.remove(reduced_data[best_attribute[2]])				
		if data[i][best_attribute[2]] < best_attribute[0]:
			#left node
			data_left.append(data[i])
			label_left.append(class_label[i])
		else:
			#right node
			data_right.append(data[i])
			label_right.append(class_label[i])
		#reduced_attribute_list = copy.copy(attribute_list)
		#reduced_attribute_list.remove(reduced_attribute_list[best_attribute[2]])
	return data_left, label_left, data_right, label_right

def make_tree(data, class_label, depth, attribute_list, tree):

	nm_datapoints = len(data)

	if nm_datapoints==0 or (depth>=max_depth) or class_label.count(0) == nm_datapoints or class_label.count(1) == nm_datapoints:
		# Have reached an empty branch or only 1 class present or reached maximum depth		
		# Base Case of Recursion
		tree['name'] = 'LEAF'
		tree['children'] = []
		tree['samples'] = len(data)
		tree['value'] =[class_label.count(0),class_label.count(1)]
		tree['label'] = max(set(class_label), key=class_label.count)
	else:
		best_attr = best_attribute(data, class_label)
		tree['decision_value'] = best_attr[0]
		tree['gain'] = best_attr[1]
		tree['name'] = attribute_list[best_attr[2]]
		tree['feature_id'] = best_attr[2]
		tree['samples'] = len(data)
		tree['children'] = []
		tree['value'] = [class_label.count(0),class_label.count(1)]
		

		data_left, label_left, data_right, label_right = data_split(data, class_label, best_attr)
		#TDIDT for each part
		tree['children'].append({})
		make_tree(data_left, label_left, depth+1, attribute_list, tree['children'][-1])
		tree['children'].append({})
		make_tree(data_right, label_right, depth+1, attribute_list, tree['children'][-1])
			
def plot_tree(filename, tree):
	#Save Dot file for tree
	tree_dot = gv.Digraph(format='svg',engine='dot')
	traverse_tree(tree, 'ROOT', tree_dot)
	f = open(filename,'w+')
	f.write(tree_dot.source)
	f.close()			

def traverse_tree(node, parent_name, tree_dot):
	if node['name'] == 'LEAF':
		tree_dot.attr('node', shape='box')
		name = parent_name + str(random.choice(string.ascii_lowercase + string.digits))
		tree_dot.node(name, ''' samples = %(samples)d \n value = %(value)s''' % {'samples': node['samples'],'value':node['value']})
		tree_dot.edge(parent_name, name)
	else:
		tree_dot.attr('node', shape='box')
		name = node['name']+'_'+str(node['samples'])
		tree_dot.node(name = name, label = '''%(property_name)s => %(decision_value)s \n gain = %(gain)s \n samples = %(samples)d \n value = %(value)s''' % {'property_name': node['name'],'decision_value':str(node['decision_value']),'gain':str(node['gain']),'samples':node['samples'],'value':node['value']})

		if parent_name != 'ROOT':
			tree_dot.edge(parent_name, name)

	for children in node['children']:
		traverse_tree(children, name, tree_dot)

def classify(tree, datapoint):

	tree_instance = tree
	while True:
		if tree_instance['name'] == 'LEAF':
			return tree_instance['label']

		elif datapoint[tree_instance['feature_id']]<tree_instance['decision_value']:	
			tree_instance = tree_instance['children'][0]
			continue
		else:
			tree_instance = tree_instance['children'][1]

def classifyAll(tree, data):
	results = []
	for i in range(len(data)):
		results.append(classify(tree,data[i]))
	return results

def calc_accuracy(predicted_label, target_label):
	correct = 0
	for pr, tg in zip(predicted_label, target_label):
		if pr == tg:
			correct += 1
	accuracy = float(correct)/len(predicted_label)*100
	return accuracy	

def process_scripts(args):

	global feature_names
	global max_depth
	global tree
	filename = args.data_file
	max_depth = args.max_depth
	mode = args.mode
	pkl_file = args.pickle_file_name

	if mode=='train':
		output_file = args.dot_file_name
		tree = {}
		data, class_label, feature_names = read_data(filename)
		#Save the tree	
		print('Training Decision Tree')
		make_tree(data, class_label, 0, feature_names, tree)
		pickle.dump(tree, open(pkl_file,'wb'))
		plot_tree(output_file, tree) 

	elif mode=='test':
		data, class_label, feature_names = read_data(filename)
		tree = pickle.load(open(pkl_file,'rb'))
		print('Testing Decision Tree')
		predicted_label = classifyAll(tree, data)
		accuracy = calc_accuracy(predicted_label, class_label)
		print('Accuracy {:0.20}'.format(accuracy))
	else:
		print('Undefined mode')

		
def main():
  parser = ArgumentParser('tdidt',
                          formatter_class=ArgumentDefaultsHelpFormatter,
                          conflict_handler='resolve')

  parser.add_argument('--data_file', nargs='?', required=True,
                      help='Filename of training or test data')

  parser.add_argument('--max_depth', default=3, type=int,
                      help='Maximum depth of Tree')

  parser.add_argument('--mode', default='train', type=str,
                      help='train or test')

  parser.add_argument('--dot_file_name', 
                      help='If training mode name of dot file to contain tree')

  parser.add_argument('--pickle_file_name', 
                      help='Pickle file for tree')

  args = parser.parse_args()

  process_scripts(args)

if __name__ == '__main__':
	sys.exit(main()) 