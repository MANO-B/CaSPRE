'''
    File name: count_to_FPKM.py
    Date created: Oct 6, 2019

    Objective:
    To transform RNA-seq expression raw count into FPKM style

    command: python3 convert_npz.py
'''
from glob import glob
import os
import sys
import pandas as pd
import numpy as np
import pathlib

if __name__ == '__main__':
    data_dir = "/mnt/HDD8TB/RNA_seq/FPKM_calc/select_patho_309"
    result_dir = data_dir + "_result"
    batch_rand = 32
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    if not os.path.exists(result_dir + "/npy/"):
        os.mkdir(result_dir + "/npy/")

    for bat in range(0, batch_rand):
        # loading training data
        path = data_dir + '/*/rand_' + str(bat) + "_*.npy"
        files = glob(path)
        files.sort()
        trainImg = []
        trainLabel = []
        j = 1
        num = len(files)

        # making a classification list
        if bat == 0:
            for img in files:
                print("\r" + str(bat) + ", " + str(j) + "/" + str(num) , end="")
                label = pathlib.Path(img).parent.name
                trainImg.append(np.expand_dims(np.load(img), axis=0))
                trainLabel.append(label)
                j += 1
            image_list = np.asarray(trainImg)
            trainLabel = pd.DataFrame(trainLabel)

            # saving a file
            np.savez_compressed(result_dir + "/npy/image_" + str(bat) + ".npz", image_list)
            trainLabel.to_csv(result_dir + "/npy/label.tsv", index=False, sep='\t')

        else:
            for img in files:
                print("\r" + str(bat) + ", " + str(j) + "/" + str(num) , end="")
                trainImg.append(np.expand_dims(np.load(img), axis=0))
                j += 1

            image_list = np.asarray(trainImg)
            np.savez_compressed(result_dir + "/npy/image_" + str(bat) + ".npz", image_list)
