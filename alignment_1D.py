'''
    File name: align_1D.py
    Date created: Nov 28, 2020

    Objective:
    Align RNA-seq expression data obtained from TCGA to 1-D image

    command: python3 align_1D.py \
             -o="/mnt/HDD8TB/RNA_seq/" \
             -F="/mnt/HDD8TB/RNA_seq/FPKM_calc/expression_data/*/*FPKM.txt.gz" \
             -X=1375 \
             -Y=1
             
'''

import argparse
import numpy as np
from glob import glob
import os
import sys
import cv2
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--basename')
    parser.add_argument('-F', '--datapath')
    parser.add_argument('-X', '--x_size')
    parser.add_argument('-Y', '--y_size')

    opts = parser.parse_args()

    try:
        datapath = opts.datapath
    except IndexError:
        parser.error('Missing data argument')
    files = glob(datapath)  
    files = sorted(files)

    for i in range(0, 4):
        # get data file
        for dataNb in range(len(files)):
            filename = files[dataNb]
            opts.basenamePNG = os.path.splitext(os.path.basename(filename))[0]
            tmp = pd.read_csv(filename,delimiter="\t", header=None)
            tmp.columns = ['name','value']
            tmp = tmp.set_index('name')
            tmp = tmp.sort_index()
            dataFile = np.append(np.array(tmp.loc[:,'value']), np.array([32.0]), axis=0)
            tmp = np.log2(dataFile + 1) / 16 - 0.5
            img = np.array([tmp[x] for x in df_template]).reshape(int(opts.x_size), int(opts.y_size))
            if not os.path.exists(opts.basename):
                os.makedirs(opts.basename)
            filename = os.path.join('rand_' + str(i) + '_' + opts.basenamePNG + ".npy")
            print(dataNb, filename, ' / ', len(files))
            np.save(os.path.join(opts.basename, filename), img)