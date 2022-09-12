#!/usr/bin/python3

import os, argparse, subprocess
import numpy as np
import pandas as pd
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument("--outdir")
parser.add_argument("--gene")
args = parser.parse_args()
outdir = args.outdir
gene = args.gene


# import recovery statistics
df = pd.read_csv("../03_hybpiper/seq_lengths.txt", sep="\t")
df = df.drop(0)


# for each aligned gene, identify the two samples with the highest recovery stats
#gene = fn.split("_")[1]
if gene in df.columns:
	df_red = df[['Species',gene]].sort_values(gene, ascending=False)
	df_red = df_red.reset_index()
	# first sample
	sp = df_red["Species"][0]
	exon1 = list(SeqIO.parse("/home/owrisberg/Coryphoideae/work_flow/03_hybpiper/"+sp+"/"+gene+"/"+sp+"/sequences/FNA/"+gene+".FNA", "fasta"))[0]
	exon1.id = "exon1"
	# second sample
	sp = df_red["Species"][1]
	exon2 = list(SeqIO.parse("/home/owrisberg/Coryphoideae/work_flow/03_hybpiper/"+sp+"/"+gene+"/"+sp+"/sequences/FNA/"+gene+".FNA", "fasta"))[0]
	exon2.id = "exon2"
	with open(gene+"_temp.fasta", "w") as output_handle:
		SeqIO.write([exon1, exon2], output_handle, "fasta")
	subprocess.call("mafft --add "+gene+"_temp.fasta "+gene+"_aligned.fasta > ../"+outdir+"/"+gene+"_aligned.fasta" ,shell=True)
	subprocess.call("rm "+gene+"_temp.fasta", shell=True)
else:
	print(gene+" not there!!!!")