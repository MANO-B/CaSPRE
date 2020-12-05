#!/bin/sh

HOME=/home/ueno/ln_run_fastq
WORK=/mnt/HDD/share/RNA_seq
TMP=/home/ikegami/work/FPKM
PROJECT=$1
SAMPLE=$2
THREAD=$3

sshpass -p ikegami ssh -o StrictHostKeyChecking=no ikegami@172.25.100.141 "find "${HOME}/${PROJECT}/${SAMPLE}/" -name "*R1*" -exec cat {} >> "${TMP}/${SAMPLE}_R1.fastq.gz" \;" & sshpass -p ikegami ssh -o StrictHostKeyChecking=no ikegami@172.25.100.142 "find "${HOME}/${PROJECT}/${SAMPLE}/" -name "*R2*" -exec cat {} >> "${TMP}/${SAMPLE}_R2.fastq.gz" \;" & wait
sshpass -p ikegami  scp -o StrictHostKeyChecking=no ikegami@172.25.100.141:${TMP}/${SAMPLE}_R1.fastq.gz ${WORK} & sshpass -p ikegami  scp -o StrictHostKeyChecking=no ikegami@172.25.100.142:${TMP}/${SAMPLE}_R2.fastq.gz ${WORK} & wait

sshpass -p ikegami ssh -o StrictHostKeyChecking=no ikegami@172.25.100.141 "rm  "${TMP}/${SAMPLE}_R1.fastq.gz""
sshpass -p ikegami ssh -o StrictHostKeyChecking=no ikegami@172.25.100.141 "rm  "${TMP}/${SAMPLE}_R2.fastq.gz""

${WORK}/STAR-2.7.1a/bin/Linux_x86_64_static/STAR \
--readFilesIn "${WORK}/${SAMPLE}_R1.fastq.gz" "${WORK}/${SAMPLE}_R2.fastq.gz" \
--alignIntronMax 500000 \
--alignIntronMin 20 \
--alignMatesGapMax 1000000 \
--alignSJDBoverhangMin 1 \
--alignSJoverhangMin 8 \
--alignSoftClipAtReferenceEnds Yes \
--genomeDir  "${WORK}/STAR_index" \
--genomeLoad NoSharedMemory \
--limitSjdbInsertNsj 1200000 \
--outFileNamePrefix "${SAMPLE}_" \
--outFilterMatchNminOverLread 0.33 \
--outFilterMismatchNmax 999 \
--outFilterMismatchNoverLmax 0.1 \
--outFilterMultimapNmax 20 \
--outFilterScoreMinOverLread 0.33 \
--outFilterType BySJout \
--outSAMattributes NH HI NM MD AS XS \
--outSAMtype BAM Unsorted \
--outSAMunmapped None \
--readFilesCommand zcat \
--runThreadN "${THREAD}" \
--twopassMode Basic

rm "${WORK}/${SAMPLE}_R1.fastq.gz"
rm "${WORK}/${SAMPLE}_R2.fastq.gz"

# HTSeq count  version 0.6.1p1

${WORK}/HTSeq-0.6.1p1/build/scripts-2.7/htseq-count \
-f bam \
-r name \
-s reverse \
-a 10 \
-t exon \
-i gene_id \
-m intersection-nonempty \
"${WORK}/${SAMPLE}_Aligned.out.bam" \
"${WORK}/gencode.v22.annotation.gtf" > "${WORK}/raw_count/${SAMPLE}.txt"

rm "${WORK}/${SAMPLE}_Aligned.out.bam"

