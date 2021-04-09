# Coryphoideae targeted capture bioinformatics work-flow

Inherited by Oscar Wrisberg ([Oscar.wrisberg@bio.au.dk](mailto:Oscar.wrisberg@bio.au.dk)), 11th January 2021

* * *
## -1\. Work to do
- [x] Ensure Coverage script works
	- [x] Is the output satisfactory - *trimmed.fasta seems to be empty: This was caused by me not running intronerate and as such not producing the necesarry file for the coverage script. 
	- [ ] How is it used in Blacklisting
- [ ] Blacklisting
	- [ ] Understand how Blacklisting commands work
	- [ ] Hardcode species or genes for blacklisting
- [ ] Alignments
- [ ] 
* * *

## 0\. Workspace

All raw sequences are found on the Ecoinf drive:  
`/home/au543206/Ecoinf/C_Write/_Proj/@PEB/lab/sequence_data`  

Copy of raw sequences on GenomeDK are found at:  
`/home/owrisberg/Coryphoideae/sequence_data/Coryphoideae`

GitHub project repo clone on GenomeDK:  
`/home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree`

GitHub HybPiper repo clone on GenomeDKr:  
`/home/owrisberg/Coryphoideae/github_code/HybPiper`

Directory containing target file on GenomeDK:  
`/home/owrisberg/Coryphoideae/target_sequence`

**Required file structure**  
In order to run this pipeline you need a directory with the following folders, this can be quickly produced by running `infrastructure.sh` within the desired directory 

- `0_secapr`
    - `0_data`
    - `1_trimmed`
- `1_data`
- `2_trimmed`
- `3_hybpiper`
- `4_seqs`
- `5_coverage`
- `6_blacklisting`
- `7_alignment`
- `8_mapping`
- `9_optrimal`
- `10_manual-editing`
- `11_tree_building`

## 0\. Downloading and renaming data

Transfer the first set of sequence files from storage device to `1_data`.  
These files need renaming among other things. Within `1_data` run  
`rm *.xml *.csv Undtermined*`  
`gunzip *.gz`  
`cp /home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/names_1_data_1_rename_seqs.csv .`

**Rename files**  
You can test if this script is printing the correct things before running it by including an echo between do mv, like so `do echo mv`

`cat names_1_data_1_rename_seqs.csv | while IFS=, read orig new; do mv "$orig" "$new"; done`  
The above line introduces hidden characters ($'  
). To remove these run the following.

`rm names_1_data_1_rename_seqs.csv`  
`for f in *; do echo mv "$f" "$(sed 's/[^0-9A-Za-z_.]/_/g' <<< "$f")"; done`  
`rename -n 's/(.*).{1}/$1/' *`

The last line removes an underscore, which was introduced when hidden characters were removed (for changes to take effect remove the -n flag).

Transfer the remaining sequences to `1_data`. They will already have been renamed. (This is probably the files from Angela as these already have names following the formula of xxxx_R1.fastq)

Remove files which are of inferior quality  
run `bash /home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/names.sh`

* * *

## 1\. Before commencing analysis

SECAPR quality check is run on the raw data in `1_data`.  
In order to invoke `secapr` first activate the environment  
`conda activate secapr_env`  
Then run SECAPR from within the directory  
`secapr quality_check --input . --output .`  
Move the secapr files to `0_secapr/0_data`

A list of the fastq files is created for the directory `1_data` by running the following script from within it  
`ls *R1.fastq > namelist_temp.txt; sed 's/.........$//' namelist_temp.txt > namelist.txt; rm namelist_temp.txt`  
The second command removes the last 9 characters. This list is needed for running Trimmomatics on all the names in the list.

* * *

## 2\. Trimming

From within the `2_trimmed` directory run trimmomatics on the sequences in `1_data`

First, Activate the trimmomatic environment by writing `conda activate trimmomatic_env`

Then run: `bash /home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/trimmomatic_genomedk_sh.sh`

**OBS** remember to check if the TruSeq3-PE-2.fa file is uploaded to the folder located at `/home/owrisberg/miniconda3/pkgs/trimmomatic-0.39-1/adapters/`

All trimmed files are found in `2_trimmed` along with the stderr output in the file `stderr_trim_loop_output.txt`

SECAPR quality check is now run on the trimmed data in the directory `2_trimmed` but first, for comparability with the raw SECAPR quality check, paired and unpaired reads are combined for each sample. Within `2_trimmed` run:`bash /home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/comb_postrim_secapr.sh`

This script should be run from within `2_trimmed` and results in the creation of a subdirectory `secapr_postrim` that contains the combined files.

Now activate the Secapr environment by running `conda activate secapr_env`and run SECAPR from within `secapr_postrim`  
`secapr quality_check --input . --output .`

Transfer the FastQC files to `fastqc/secapr_2_trimmed` and delete `secapr_postrim` with all the combined files to save storage.

* * *

## 3\. Assembly (HybPiper)

### Combine unpaired reads into a single file for each sample

Run the following script within `2_trimmed`  
`/home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/comb_u_trim_reads.sh`  
This merges `####_1U.fastq` and `####_2U.fastq` into `####_UN.fastq`

### Generate namelist

A list of the fastq files within the directory `2_trimmed` is created in the directory `3_hybpiper` by running the following script from within `2_trimmed`  
`ls *1P.fastq > namelist_temp.txt; sed 's/.........$//' namelist_temp.txt > ../3_hybpiper/namelist.txt; rm namelist_temp.txt`  
The second command removes the last 9 characters. This list is needed for running hybpiper on all the listed names.  
If all trimmed data are to go into hybpiper the namelist within `1_data` can alternatively be copied to `3_hybpiper` and reused.

### Execute HybPiper

From within `3_hybpiper` run  
`bash /home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/hybpiper_gdk.sh`

### Get assembly stats

From within `3_hybpiper` run  
`python /home/owrisberg/Coryphoideae/github_code/HybPiper/get_seq_lengths.py /home/owrisberg/Coryphoideae/target_sequence/PhyloPalms_loci_renamed_794-176_HEYcorrected.fasta namelist.txt dna > seq_lengths.txt`  
and  
`python ~/Coryphoideae/github_code/HybPiper/hybpiper_stats.py seq_lengths.txt namelist.txt > stats.txt`  
The file `seq_lengths.txt` can be used to make a heatmap in R by running the script `gene_recovery_heatmap_ggplot.R`

### Paralogs

From within `3_hybpiper` run  
`bash ~/Coryphoideae/github_code/coryphoideae_species_tree/paralog2.sh`  
The output from this program is saved in the file `paralog.txt`. This file lists putatively paralogous genes. In order to have the name of every gene only listed once only run the following  
`sort paralog.txt | uniq | sed 's/^.......................//' > gene_paralogs.txt`

### Intronerate
In order to generate the super contigs we need to run intronerate.
Run the `intronerate_batch.sh`
***Make sure to download the developmental version of intronerate from Github, as the standard one causes errors when run***

***

## 4\. Retrieve sequences (HybPiper) "Springes over i coverage scriptet"

From within `3_hybpiper` run  
`python ~/github/hybpiper/retrieve_sequences.py /data_vol/peter/target/sidonie_target_file/PhyloPalms_loci_renamed_794-176_HEYcorrected.fasta . dna > stats_seq_retr.txt`  
and  
`mv *.FNA ../4_seqs`  
The recovered, unaligned multi-FASTA files for each gene can now be found in `4_seqs`.  
Putatively paralogous genes are excluded  
`for f in $(cat ../3_hybpiper/gene_paralogs.txt); do rm "${f}.FNA"; done`  
The text file `stats_seq_retr.txt` which contains the stdout for the programme `retrieve_sequences.py` can be used for the crude exclusion of genes based on number of retrieved sequences

* * *
## 4\. Coverage trimming and Length filtering
Run the coverage program by running the `coverage_batch.sh`.

Ensure that "supercontig" is chosen in the coverage.py script. This is currently done by commenting two lines of code. 

The Coverage.py script does the following:
- Gather all contigs from each sample in one fasta file
- map paired and unpaired reads to that fasta using BWA mem
- Deduplicate reads using Picard
- Calculate depth using samtools
- Mask/strip any bases with coverage less than 2 
- Generate a new trimmed sample-level fasta.

Then, in `5_coverage`, run:

`ls *trimmed.fasta > filelist.txt`
`/home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/samples2genes.py > outstats.csv`

* * *
## 5\. Blacklisting


***
# From here on out, everything needs to be done together.

## 6\. Alignment

From within `4_seqs` run MAFFT on all genes  
`bash ~/github/coryphoideae_species_tree/mafft.sh`  
Aligned genes are found within `5_alignments`

Visualize single gene alignments with AliView. Launch the program with command: `aliview`  
Visualize multiple gene alignments with Geneious. Launch from Nautilus.

* * *
## 7\. mapping

* * *
## 8\. Gap trimming using Optrimal

From within `5_alignments` run  
`bash ~/github/coryphoideae_species_tree/trimal.sh`  
The trimmed alignments can now be found in `6_trimal`

* * *
## 9\. Manual editing
Manually edit sequences to ensure proper alignment. 
* * * 

## 10\. Tree building

Check that MSA format is compatible with RAxML-NG and convert to RAxML binary alignments (RBA). From within `6_trimal` run  
`for f in *; do raxml-ng --parse --msa $f --model GTR+G; done`  
If no problems reported run from within `6_trimal`  
`bash ~/github/coryphoideae_species_tree/raxml_ng.sh`  
Move all RAxML output to `7_raxml`

* * *
