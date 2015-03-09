#! /usr/bin/env python

#
# Author: Chang, Chuan Yi
#

import nltk
import sys
import string
import math
from scipy.stats.stats import pearsonr

deps = sys.argv[1] # 
weights = sys.argv[2] 
simi = sys.argv[3]
outputFileName = sys.argv[4] # 
# Write File
write_file = open(outputFileName,'w')
# Dictionaries
rel = {}
word_rel = {}
rel_feature = {}
all_vectors = {}
freq = {}
pearson_vectorX = []
pearson_vectorY = []

# Get all targets
simi_file = open(simi,"r")
all_of_targets = {}
for line in simi_file:
	# Make dict for top ten
	temp = line.split(',')
	pearson_vectorX.append(float(temp[2]))
	all_of_targets[temp[0]] = all_of_targets[temp[1]] = ''
simi_file.close()

# Open deps file & Get components for LIN's association
file = open(deps,"r")
for line in file:
	elements = line.split('\t')
	# If target word is found in similarity file
	if elements[0] in all_of_targets:
		# Add all lines to dict.
		if elements[0] not in all_vectors:
			all_vectors[elements[0]] = [elements]
		else:
			all_vectors[elements[0]].append(elements)
		# count(r)
		if elements[1] not in rel:
			rel[elements[1]] = 1
		else:
			rel[elements[1]] += 1
		# Get count(w', r)
		if (elements[0]+elements[1]) not in word_rel:
			word_rel[(elements[0]+elements[1])] = 1
		else:
			word_rel[(elements[0]+elements[1])] += 1
		# Get count(r, w')
		if (elements[1]+elements[2]) not in rel_feature:
			rel_feature[(elements[1]+elements[2])] = 1
		else:
			rel_feature[(elements[1]+elements[2])] += 1
		# Get frequency counts
		if weights in 'FREQ':
			if (elements[0]+elements[2]) not in freq:
				freq[(elements[0]+elements[2])] = 1
			else:
				freq[(elements[0]+elements[2])] += 1
file.close()

# log2( ( count(w, r, w') * sum of count(r) across all w ) / ( count(w', r) * sum of count(r, w') across all w ) )
# Get all targets
simi_file = open(simi,"r")
duplicate = {}
for line in simi_file:
	# Make dict for top ten
	temp = line.split(',')
	if weights in 'FREQ': # FREQ
		if (temp[0]+temp[1]) in freq:
			pearson_vectorY.append(freq[(temp[0]+temp[1])])
		else:
			pearson_vectorY.append(0)
	else: # Lin
		# If target word exists
		if temp[0] in all_vectors:
			selected = False
			# Calculate for all lines
			for elements in all_vectors[temp[0]]:
				computed_similarity = 0
				if elements[2] in temp[1] and (temp[0]+elements[2]) not in duplicate and not(selected):
					duplicate[(temp[0]+elements[2])] = ''
					if weights in 'FREQ':
						computed_similarity = float(freq[(elements[0]+elements[2])])
					else:
						computed_similarity = float(math.log( float(elements[3]) * float(rel[elements[1]])/float(word_rel[(elements[0]+elements[1])])/float(rel_feature[(elements[1]+elements[2])]) )/math.log(2))
					pearson_vectorY.append(computed_similarity)
					selected = True			
			if not(selected):
				pearson_vectorY.append(0)
		else:
			pearson_vectorY.append(0)

# Print similarity comparison
for index in range(len(pearson_vectorX)):
	write_file.write(str(pearson_vectorX[index])+':'+str(pearson_vectorY[index])+'\n')
# Pearson 
write_file.write('Pearson Correlation: ' + str(pearsonr(pearson_vectorX,pearson_vectorY)[0]))

# Close files
simi_file.close()
write_file.close()










