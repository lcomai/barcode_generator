#!/Users/lucacomai/anaconda3/bin/python3.7

'''BARCODE GENERATOR
	BY Luca Comai
	(gc code by Tyson Howell)
	Feb 2020'''

print('\n\nBARCODE GENERATOR by LC\n\t--***---\nPlant Biology and Genome Center\n\tUC Davis\n')
print ('''This program generates barcodes
of a desired length, distance, and GC content
The primer sequences are for Nanopore. The 
output is ....... \n''')

# usage: mycomp$ barcode_generator_3.3.py table_excluded_barcodes length number distance min_GC max_GC attempts hf
# table_excluded_barcodes = one barcode per line table
# length = nucleotide number in barcode def:none, enter "none" if second arg is given
# number = how many barcodes def:48
# distance = Hamming distance def:2
# min_GC = minimum GC% def:0
# max_GC = maximum GC% def:100
# attempts = how many cycles shall the computer attempt def:100,000
# hf = homopolymer filter. Uses the provided number to filter n+ homopolymers. def:4
import sys
import time
import re
from datetime import date
#import pdb

start_time = time.process_time()
today = date.today().isoformat()
#___________________________________________________Definition of the input

try:
	pre_barcode = sys.argv[1]
except IndexError:
	#pre_barcode = 'pre_barcodes.txt'
	pre_barcode = 'none'
try:
	length = int(sys.argv[2])
except IndexError:
	length = 15
try:
	number = int(sys.argv[3])
except IndexError:
	number = 24
try:
	diffs = int(sys.argv[4])
except IndexError:
	diffs = 10
try:
	mingc = float(sys.argv[5])/100
except IndexError:
	mingc = 0
try:
	maxgc = float(sys.argv[6])/100
except IndexError:
	maxgc = 200
try:
	attempts = int(sys.argv[7])
except IndexError:
	attempts = 100000 
try:
	# hf is homopolymer filter
	hf = int(sys.argv[8])
except IndexError:
	# discard barcodes that have a string of hf or more identical nucs
	hf = 4  


		
#___________________________________________________process
				

# make list of the four bases
l1 = ['a', 'c', 'g', 't']

pre_barcode_list = []
# for comparison later, make list in upper case
pre_upper_bc = []
barcode_list = []

# set regex match
# convert homopolymer number to string
hfs = str(hf) 
pat = re.compile('a{'+hfs+',}|c{'+hfs+',}|g{'+hfs+',}|t{'+hfs+',}')

# open file of preexisting barcodes
if pre_barcode == 'none':
	barcode_list = []
else:
	pre_barcode_op = open(pre_barcode, 'r')
	for line in pre_barcode_op:
		bc_list = [i.lower() for i in line.rstrip()]
		pre_barcode_list.append(bc_list)
	pre_barcode_op.close()
	    
	    

# initialize the first barcode
first_barcode = []

# prime the tested list, for future counting
tested = []

# function to determine GC content
def gc_cont (bar_code):
	gc = 0.0
	for base in range(length):
		if bar_code[base] == 'c' or bar_code[base] == 'g':
			gc += 1
		else:
			gc += 0
	cont = gc / length
	return cont

# import random module
import random

# make the first barcode
# add first barcode to barcode list. This is needed for the
# first comparison of "compare_barcode" function

barcode_list += pre_barcode_list

# print barcode_list

while barcode_list == []:
	for i in range(length):
		first_barcode.append(random.choice(l1))
	if gc_cont(first_barcode) <= maxgc and gc_cont(first_barcode) >= mingc:
		barcode_list.append(first_barcode)
	else:
		first_barcode = []  

# the barcode "cradle": a place where each barcode will sit
barcode = []

#___________________________________________________define functions

# function makes the barcode
def make_barcode(length, barcode):
	# empties the barcode cradle
	for i in range(length):
		barcode.append(random.choice(l1))
	return barcode
	
# barcode is tested vs the previously generated barcodes
def compare_barcode(length, barcode_l, barcode_out, tested):
	count = 0
	# run barcode creator
	barcode_maker = []
	barcode = make_barcode(length, barcode_maker)
	# keep track of it
	tested.append(barcode)
	# testing of barcode
	if barcode not in barcode_l:
		count_list = []
		# compare to barcodes in list
		for bc in barcode_l:
			# matches to existing barcodes
			# are scored as points
			count = 0
			for pos in range(length):
				if barcode[pos] == bc[pos]:
					count += 1
				else:
					count += 0
			# for each barcode a list of scores is made
			count_list.append(count)
		# if the barcode has enough unique bases
		# and the proper GC content, it is added
		# to the list of good barcodes
		if max(count_list) > length-diffs:
			count_list = []
		# apply homopolymer filter
		# join items in barcode list to make regex searchable string
		elif pat.search(''.join(barcode)):
			count_list = []
			print('excluded: '+''.join(barcode))
		elif gc_cont(barcode) <= maxgc and gc_cont(barcode) >= mingc:
			barcode_l.append(barcode)
			barcode_out.append(barcode)
			count_list = []
		else:
			count_list = []
	else:
		pass
			   
#___________________________________________________run functions
	
# initialize count

count_list = []
barcode_out = []

# program stalls if too many attempts are allowed
# and few barcodes remain to be discovered
# this loop keeps the attempts within the range allowed
while len(tested) < attempts:
	if len(barcode_out) < number:
		compare_barcode(length, barcode_list, barcode_out, tested)
	else:
		break

barcode_list.sort()
barcode_out.sort()

all_bc = barcode_out + pre_barcode_list
all_bc.sort()

##print "\n\nRESULTS\n\nall barcodes and GC content:"
##
##for i in barcode_list:
##	print i, int(gc_cont(i)*100), '%'

print("\n\nRESULTS\n\ngood new barcodes and previous set and GC content:")    
for i in all_bc:
	print(i, int(gc_cont(i)*100), '%')

print("\n\nRESULTS\n\ngood new barcodes only and GC content:")    
for i in barcode_out:
	print(i, int(gc_cont(i)*100), '%')

print('\nnumber of tested barcodes:')

print(len(tested))

print('\nnumber of good barcodes:')

print(len(barcode_out))

#count base composition in each of the barcode position
from collections import defaultdict

print('\nbase compositions by position')

for pos in range(length):
	list_l = [i[pos] for i in barcode_out]
	base_count = defaultdict(int)
	for base in list_l:
		base_count[base] += 1
	print(base_count.keys(), base_count.values())

#___________________________________________________manipulate barcodes and print results

# make a file for the barcoded oligonucleotide sequence
# open file 
barfile = open('barcode_'+today+'.txt', 'w')
sdiffs = str(diffs)
slength = str(length)
#pdb.set_trace()
barfile.write('These are the barcodes of length '+slength+' with a distance of '+sdiffs+' bases\n')

#___________________________________________________Illumina oligonucleotide sequence
# not in this generator. See others
#__________________________________Nanopore oligonucleotide 
# note: these are not complementary
primerF = 'TTTCTGTTGGTGCTGATATTGC' 
primerR = 'ACTTGCCTGTCGCTCTATCTTC'
# barcode is attached to 5'	
# define adapter names
name_rootF = '>adF_'
name_rootR = '>adR_'

#____________________________________________________________
# initialize a holder name for the complement of barcode
#comp_barcode = ''
# define function to derive complement of any seq
# has been imported, output is a "comp_barcode"

# def reverse_comp(seq):
# 	comp_table = str.maketrans('actg','tgac')
# 	global comp_barcode
# 	comp_barcode = seq[::-1].translate(comp_table)
#____________________________________________________________
# divide barcode stash into two. Use floor division operator '//'
# to account for cases of uneven number of barcodes in the stash
# print the first half with primer F    
for i in barcode_out[:len(barcode_out)//2]:
	j = ''.join(i)
	barfile.write(f'{name_rootF}{j[:7]}\n{j}{primerF}\n')
# print the second half with primer R
for i in barcode_out[len(barcode_out)//2:]:
	j = ''.join(i)
	barfile.write(f'{name_rootR}{j[:7]}\n{j}{primerR}\n')
print('''\nA file called barcode.txt has been generated.
It contains the adapter sequences with each
barcode in lower case\n\n''')

# close file or it does not get updated
barfile.close()


print('Finished')

end_time = time.process_time()
time_tot = end_time - start_time

print(' ...by the way, it took me ', time_tot, ' seconds')


#___________________________________________________log
# version 3.3:
# convert to Python 3+
# add homopolymer filter
# add date stamp to output file

# version 3.0
# removed raw input for command line argvs
# takes as argv 1 a table of pre-existing barcodes 
# that should not be used
# added a time counter

# version 2.9
# removed all global statements from functions
# add set picker

# version 2.8:
# rephrase raw input queries
# default barcodes to test to 10,000
# clean up shell results

# changes from 2.7:
# rephrase raw input queries
# default barcodes to test to 10,000
# clean up shell results






