import os
import copy
import pickle
import numpy as np
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
from tdidt import plot_tree
import sys
import pdb

def lang(node,listing,listlist,tree1):
	i=1
	
	if node['name'] == 'LEAF':
		y=len(listing)
		templist=copy.copy(listing)
		listlist.append(list(listing))
		
		#templist.reverse()
		z=0
		for x in range(0,y):
			element=templist.pop()
			if element is "yes" or element is "no":
				if element is "yes":
					bigsmall=" < "
				else:
					bigsmall=" > "
			else:
				if z!=y-1:
					print(element["name"]+bigsmall+str(element["decision_value"])+" AND ",end="")
				else:
					print(element["name"]+bigsmall+str(element["decision_value"]),end="")
			z=z+1
		if node["value"][0]<node["value"][1]:
			#print(listing[0]["name"]+" > "+str(listing[0]["decision_value"])+" AND "+listing[1]["name"]+" > "+str(listing[1]["decision_value"])+" AND "+listing[2]["name"]+" > "+str(listing[2]["decision_value"])+" -> no" )
			#print(output_string[6:])
			print(" -> yes" )
		else:

			print(" -> no" )
	else:
		listing.append(node)
	for children in node['children']:
		if i==1:
			list1=copy.copy(listing)
			list1.append("yes")
			lang(children,list1,listlist,tree1)
		else:
			list2=copy.copy(listing)
			list2.append("no")
			lang(children,list2,listlist,tree1)
		i=i+1

def process_scripts(args):
	mode =args.mode
	tree_file = args.pickle_file_name
	tree = pickle.load(open(tree_file,'rb'))
	tree1 = copy.deepcopy(tree)
	listing=[]
	listlist=[]

	lang(tree1,listing,listlist,tree1)

def main():
	parser = ArgumentParser('prune_tree',
							formatter_class=ArgumentDefaultsHelpFormatter,
								conflict_handler='resolve')
	parser.add_argument('--pickle_file_name', 
                      help='Pickle file for tree')

	args = parser.parse_args()
	process_scripts(args)


if __name__ == '__main__':
	sys.exit(main()) 