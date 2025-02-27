#!/bin/bash

#Activating trimal_env
source /home/owrisberg/miniconda3/etc/profile.d/conda.sh
conda activate trimal_env

#Getting the gene name as a commandline argument with the flag -g
while getopts g: flag
do
    case "${flag}" in
        g) gene=${OPTARG};;
    esac
done

    #Copying data into working folder
    cd /home/owrisberg/Coryphoideae/work_flow/06_alignment
    cp "${gene}_aligned.fasta" "../07_optrimal/${gene}_aligned_mafft.fasta"

    #Going to folder with data
    cd /home/owrisberg/Coryphoideae/work_flow/07_optrimal

    # replace n's with gaps in alignmenets - this will otherwise trip up TrimAl
    for f in ${gene}_aligned_mafft.fasta; do (sed -i'.old' -e 's/n/-/g' $f); done

    # change back "exo" to "exon"
    for f in ${gene}_aligned_mafft.fasta; do (sed -i'.old' -e 's/exo-/exon/g' $f); done

    for f in ${gene}_aligned_mafft.fasta; do (sed -i'.old' -e 's/HEY883-/HEY883n/g' $f); done

    # create summary tables for all thresholds specified
    while read cutoff_trim
    do
			# Checking if a directory exists for the cutoff_trim
            if [[ -d "/home/owrisberg/Coryphoideae/work_flow/07_optrimal/${cutoff_trim}" ]]
			then
     			echo "${cutoff_trim} folder exists."
			else
				mkdir $cutoff_trim
			fi 

			#trimming the aligned sequences of a gene with the given cutoff_trim
            for alignment in "${gene}_aligned_mafft.fasta"
            do
              echo This is the alignment: ${alignment}
              trimal -in ${alignment} -out ${cutoff_trim}/${alignment} -htmlout ${cutoff_trim}/${alignment/.fasta}.html -gt ${cutoff_trim}

                    #check if alignment was trimmed to extinction by trimAl
                    if grep ' 0 bp' ${cutoff_trim}/${alignment}
                    then
                        rm -f ${cutoff_trim}/${alignment}
                    fi
            done

    done < cutoff_trim.txt

