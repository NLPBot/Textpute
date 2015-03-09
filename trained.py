#! /usr/bin/env python

#
# Author: Chang, Chuan Yi
#

from nltk import *
from nltk.tree import *
import sys

# Getting arguments
expand = sys.argv[1]

NTCounts = {}
graph = {}

def traverse(t):
	try:
	    t.label()
	except AttributeError:
	    return
	else:
	    if t.height() == 2:   #child nodes  
			if t.label() not in graph:
				graph[t.label()] = [[1,str(t.leaves()[0])]]
			else:
				notused = True
				for production in graph[t.label()]:
					if production[1]==str(t.leaves()[0]):
						production[0] += 1
						notused = False
				if notused:
					graph[t.label()].append([1,str(t.leaves()[0])])
			return
	    parent = t.label()
	    left = right = ''
	    left_child = right_child = None
	    for child in t:
	    	if left == '':
	    		left_child = child
	    		left = child.label()
	    	else:
	    		right_child = child
	    		right = child.label()
		if left!='' and right!='':
			if parent not in graph:
				graph[parent] = [[1,str(left),str(right)]]
			else:
				notused = True
				for production in graph[parent]:
					if str(production[1])==str(left) and str(production[2])==str(right):
						production[0] += 1
						notused = False
				if notused:
					graph[parent].append([1,str(left),str(right)])
			traverse(left_child)
			traverse(right_child)

# Expand coverage 
def RuleExpander():
	graph['VBG'].append([1,'Traveling'])
	graph['VBG'].append([1,'Arriving'])
	NTCounts['VBG'] += 2
	graph['VBP'].append([1,'accept'])
	NTCounts['VBP'] += 1
	graph['VB'].append([1,'Traveling'])
	graph['VB'].append([1,'Arriving'])
	graph['VB'].append([1,'accept'])
	NTCounts['VB'] += 3
	graph['NN'].append([1,'flyer'])
	NTCounts['NN'] += 1
	graph['NNS'].append([1,'tickets'])
	NTCounts['NNS'] += 1
	graph['NN'].append([1,'tickets'])
	graph['NN'].append([1,'flyer'])
	NTCounts['NN'] += 2
	graph['NP_NNP'].append([1,'Westchester'])
	NTCounts['NP_NNP'] += 1
	graph['NNP'].append([1,'H'])
	NTCounts['NNP'] += 1
	graph['IN'].append([1,'either'])
	graph['IN'].append([1,'during'])
	NTCounts['IN'] += 2
	graph['JJ'].append([1,'frequent'])
	NTCounts['JJ'] += 1

# All lines
file = open('parses.train',"r")
for line in file:
	traverse(ParentedTree.fromstring(line))
	words = line.split()
	for word in words:
		if ')' not in word:
			word = word + ' '
			newword = word[word.find('(')+1:word.find(' ')]
			if newword not in NTCounts:
				NTCounts[newword] = 1
			else:
				NTCounts[newword] += 1

# 1 is true
if expand:
	# Expand coverage
	RuleExpander()

# Probability
write_file = open('trained.pcfg','w')
for key in graph:
	for production in graph[key]:
		#if len(production)<3:
		production.append(float(production[0])/float(NTCounts[key]))
		lhs = key
		if "'" in key:
			lhs = lhs.replace("'",'2')
		if len(production)>3:
			first = production[1]
			second = production[2]
			if "'" in production[1]:
				first = first.replace("'",'2')
			if "'" in production[2]:
				second = second.replace("'",'2')
			write_file.write(lhs+' -> '+first+' '+second+' ['+str(production[3])+']\n')
		else:
			first = production[1]	
			write_file.write(lhs+' -> "'+first+'" ['+str(production[2])+']\n')
# Close
write_file.close()







