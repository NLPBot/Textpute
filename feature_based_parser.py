#! /usr/bin/env python

#
# Ling 571: HW 5  
# Instructor: Gina-Anne Levow
# Author: Chang, Chuan Yi
#

import nltk
import sys
from nltk.tree import *
from nltk import load_parser
nltk.download('punkt')   

# Getting arguments
grammarFileName = sys.argv[1] 
inputFileName = sys.argv[2]
outputFileName = sys.argv[3]  

# Open grammar file and create a parser
filepath = "file:" + grammarFileName
my_parser = load_parser(filepath,trace=2)

# To get the tokenizer
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

# Open file to write
write_file = open(outputFileName,'w')

# A vector of lines
lines = [] 
sentence_list = []

# A function that grab lines from file and store lines as vectors of strings
def getLines():
        file = open(inputFileName,"r")
        for line in file:       
                # Add sentence to list
                sentence_list.append(line)
                # Appending to lines vector
                lines.append(nltk.word_tokenize(line))

# A function that parse the vector of lines and output grammar to file
def parse():
        num_lines = len(lines)
        counter = 1

        for line in lines:
                printed = False
                for tree in my_parser.nbest_parse(line):
                        if not(printed):
                                write_file.write(str(tree._pprint_flat(nodesep='',parens="()",quotes=False)))
                        printed = True
                if counter!=num_lines:
                        write_file.write('\n')
                counter += 1

# Calling the functions above
getLines()
parse()

# Close output file
write_file.close()




