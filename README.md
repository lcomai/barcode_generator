# barcode_generator for Nanopore PCR
A program that generates barcodes for sequencing adapters. It runs in Python 3.x. Tested with 3.7.
This version, 3.4, is for Nanopore PCR adapters. If you select, for example, 48 adapters it will 
print to a file a list of 24 forward and 24 reverse adapters. 

## Adapter sequences
5'-[barcode]-TTTCTGTTGGTGCTGATATTGC

5'-[barcode]-ACTTGCCTGTCGCTCTATCTTC

## Arguments
* table_excluded_barcodes = one barcode per line table, for example, if the first barcode is 'aggt', the line
should be "['a','g','g','t']". default is none. Enter "none" if the second arg is given. 
* length = nucleotide number in barcode 
* number = how many barcodes def:48
* distance = Hamming distance def:2
* min_GC = minimum GC% def:0
* max_GC = maximum GC% def:100
* attempts = how many cycles shall the computer attempt def:100,000
* hf = homopolymer filter. Uses the provided number n to filter n+ homopolymers. def:4

I run this program from BBEdit (or TextWrangler) in a Mac. In this case, I find it convenient to enter the arguments
by modifying the script itself (try-except lines), saving it, then running it. If you invoke it from a terminal or console, the usage is shown below.  

usage: mycomp$ barcode_generator_3.4.py table_excluded_barcodes length number distance min_GC max_GC attempts hf

