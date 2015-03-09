#! /usr/bin/env python

#
# Author: Chang, Chuan Yi
#

import nltk
from nltk.tree import *
import sys

# Getting arguments
writeFileName = sys.argv[1]

# load pcfg file
pcfg = nltk.data.load('trained.pcfg')
prison_num = 1
			
# Run algorithm
def PCYK(words):
	global prison_num
	# Get num_words
	num_words = len(words)
	# Base Case
	for i in xrange(1,num_words+1):
		appeared = False
		#for each production RA -> RB RC
		for rule_index in pcfg.productions():
			rhs_list = list(rule_index.rhs())
			if (len(rhs_list)==1) and str(rhs_list[0])==str(words[i-1]):
				appeared = True
				# X[i,i,A] = P(A -> w(i)): words[i](terminal) -> non-terminal -> number
				table[i][1].append(str(prison_num))
				prob[str(prison_num)] = float(rule_index.prob())
				graph[str(prison_num)] = [-1]
				translate[str(prison_num)] = str(rule_index.lhs())
				string_translate[str(prison_num)] = str(words[i-1])
				prison_num = prison_num + 1
		if not(appeared):
			print words[i-1],
	# Recursive Case
	for length in xrange(2,num_words+1): # Window length
		for start in xrange(1,num_words-length+2): # Start point
			for partition in xrange(1,length): # partition within window
				# For each production RA -> RB RC
				for i in pcfg.productions():
					rhs_list = list(i.rhs())
					lhs = i.lhs()
					if (len(rhs_list)==2):  
						for left in table[start][partition]:
							if (str(translate[str(left)])==str(rhs_list[0])):
								for right in table[start+partition][length-partition]:
									if (str(translate[str(right)])==str(rhs_list[1])):
										table[start][length].append(str(prison_num))
										prob[str(prison_num)] = (float(i.prob()) * prob[str(left)] * prob[str(right)])
										graph[str(prison_num)] = [str(left),str(right)]
										translate[str(prison_num)] = str(lhs)
										prison_num = prison_num + 1

# Build Tree
def buildTree(num):	
	if str(num) in translate:
		if str(num) in string_translate:
			return Tree(str(translate[str(num)]),[str(string_translate[str(num)])])
		elif len(list(graph[str(num)]))>1:
			left_tree = Tree(translate[str(graph[str(num)][0])],buildTree(str(graph[str(num)][0])))
			right_tree = Tree(translate[str(graph[str(num)][1])],buildTree(str(graph[str(num)][1])))
			return Tree(str(translate[str(num)]),[left_tree,right_tree])
		else:
			return Tree(translate[str(graph[str(num)][0])],buildTree(str(graph[str(num)][0])))

# Find Max.
def FindMax(num):
	if str(num) in translate:
		if str(num) in string_translate:
			return prob[str(num)]
		elif len(list(graph[str(num)]))>1:
			return prob[str(num)] * FindMax(str(graph[str(num)][0])) * FindMax(str(graph[str(num)][1]))
		else:
			return prob[str(num)] * FindMax(str(graph[str(num)][0]))

# Convert apostrophe
def ConvertBack():
	for key in translate:
		if '2' in translate[key]:
			translate[key] = translate[key].replace('2',"'")

# Get word list, Open file to write
write_file = open(writeFileName,'w')
lines = []
file = open('ents.test',"r")

# All lines
for line in file:	
	# NUM -> [ NUM_1, NUM_2 ] or [ "terminal" ]
	graph = {}
	translate = {}
	string_translate = {}
	prob = {}
	prison_num = 1
	words = [x for x in nltk.word_tokenize(line)]
	num_words = len(words)
	# table threat - 'true' = 1
	table = [[[] for endIndex in range(num_words+1)] for startIndex in range(num_words+1)]
	# Run
	PCYK(words)
	ConvertBack()
	# Find Max.
	product = tree_index = index = 0
	for root in table[1][num_words]:
		if product < FindMax(root):
			tree_index = index
			product = FindMax(root)
		index += 1
	# Print tree
	if product!=0:
		tree = buildTree(str(table[1][num_words][int(tree_index)]))
		if tree != None:
			write_file.write(tree._pprint_flat(nodesep='',parens="()",quotes=False)) 
	write_file.write('\n') # Print a line

# Close
write_file.close()



