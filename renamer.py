#!/usr/bin/python3

import argparse, re

#Arguments from commandline
parser = argparse.ArgumentParser()
parser.add_argument("mapping")
parser.add_argument("infile")
parser.add_argument("outfile")
parser.add_argument('--bs', default=0, help='1 = tree with bootstrap values')

#parsing args
args = parser.parse_args()

#Reading tips from tree
with open(args.infile) as f:
	tree = f.readline().strip()
	
with open(args.mapping, mode='r', encoding='utf-8-sig') as f: 
	for line in f:
		line = line.strip()
		LINE = line.split(",")
		searchterm = LINE[0]
		print("this is LINE[0] ",LINE[0]," and this is LINE[1] ", LINE[1])
		if args.bs == 0:
			tree = re.sub(rf'\({searchterm},','('+LINE[1]+',',tree)
			tree = re.sub(rf',{searchterm}\)',','+LINE[1]+')',tree)
		else: 
			tree = re.sub(rf'\({searchterm}:','('+LINE[1]+':',tree)
			tree = re.sub(rf',{searchterm}:',','+LINE[1]+':',tree)

with open(args.outfile, "w") as f:
	print(tree,file=f)

