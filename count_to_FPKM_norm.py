'''
    File name: count_to_FPKM.py
    Date created: Oct 6, 2019

    Objective:
    To transform RNA-seq expression raw count into FPKM style

    command: python3 count_to_FPKM.py \
             -c="/mnt/HDD8TB/RNA_seq/raw_count/*" \
             -i="/mnt/HDD8TB/RNA_seq/gencode.gene.info.v22.tsv" \
             -o="/mnt/HDD8TB/RNA_seq/FPKM_calc/FPKM"

python3 count_to_FPKM_norm.py \
             -c="/mnt/HDD8TB/RNA_seq/TOP_count/*" \
             -i="/mnt/HDD8TB/RNA_seq/gencode.gene.info.v22.tsv" \
             -o="/mnt/HDD8TB/RNA_seq/TOP_FPKM"

python3 count_to_FPKM_norm.py \
             -c="/mnt/HDD8TB/RNA_seq/TOP_normal_count/*" \
             -i="/mnt/HDD8TB/RNA_seq/gencode.gene.info.v22.tsv" \
             -o="/mnt/HDD8TB/RNA_seq/TOP_normal_FPKM"

python3 count_to_FPKM_norm.py \
             -c="/mnt/HDD8TB/RNA_seq/RNA_count/*" \
             -i="/mnt/HDD8TB/RNA_seq/gencode.gene.info.v22.tsv" \
             -o="/mnt/HDD8TB/RNA_seq/RNA_normal_FPKM"



'''

import argparse
from glob import glob
import os
import sys
import pandas as pd
import numpy as np

def normalize_per_million_reads(df):
    # RPM/FPM = reads per million  fragments per million
    sum_count = df[df["gene_type"] == "protein_coding"]["count"].sum()
    return 10**6 * df["count"] / sum_count

def normalize_per_kilobase(df, gene_length):
    # FPKM = fragments per kilobase of exon per million reads mapped
    df_tmp = (df.T * 10**3 / gene_length).T 
    return df_tmp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--countfile')
    parser.add_argument('-i', '--info')
    parser.add_argument('-o', '--outputpath')
    opts = parser.parse_args()
    datapath = opts.countfile
    if not os.path.exists(opts.outputpath):
        os.makedirs(opts.outputpath)

    files = glob(datapath)  
    files = sorted(files)

    info = pd.read_csv(opts.info, header=0, sep='\t')
    info = info.sort_values('gene_id').reset_index()


    for dataNb in range(len(files)):
        filename = files[dataNb]
        opts.basename = os.path.splitext(os.path.basename(filename))[0]
        df = pd.read_csv(filename, header=None, sep='\t').drop(range(60483,60488))
        df.columns = ['gene_id','count']
        df = df.sort_values('gene_id')
        df["gene_type"] = info["gene_type"]
        df["exon_length"] = info["exon_length"]

        # RPM/FPM = reads per million  fragments per million
        df_count_fpm = normalize_per_million_reads(df)

        # FPKM = fragments per kilobase of exon per million reads mapped
        gene_length = df["exon_length"]
        df_count_fpkm = normalize_per_kilobase(df_count_fpm, gene_length)
        #print(df_count_fpkm.head())
        print(dataNb+1, ' / ', len(files))

        # for TOP version 5
        # normalized by 10 house-keeping genes
        df_count_fpkm.to_csv(opts.outputpath + "/" + opts.basename + ".FPKM.txt", sep='\t',index_label=False, header=False)

    
