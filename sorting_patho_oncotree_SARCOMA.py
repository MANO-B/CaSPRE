'''
    File name: sorting.py
    Date created: Aug 22, 2019

    Objective:
    Sort RNA-seq expression png image with TCGA metadata

    command: python3 sorting.py \
             -f="/mnt/IKEGAMI/R/expression_profile/files.json" \
             -C="/mnt/IKEGAMI/R/expression_profile/clinical.tsv" \
             -s="/mnt/IKEGAMI/R/expression_profile/png_anal" \
             -F="/mnt/IKEGAMI/R/expression_profile/png_rand/*.FPKM.txt.npy"
'''

import argparse
import numpy as np
from glob import glob
import os
import sys
import cv2
import json
import random
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files')
    parser.add_argument('-C', '--clinical')
    parser.add_argument('-s', '--sorted_TCGA')
    parser.add_argument('-p', '--sorted_patho')
    parser.add_argument('-F', '--datapath')
    opts = parser.parse_args()

    # get data file
    files = glob(opts.datapath)
    df_clin = pd.read_table(opts.clinical, header=0, index_col=0)
    f = open(opts.files, 'r')
    jdata = json.load(f)
    cnt = 0
    TCGA = 1
    if not os.path.exists(opts.sorted_TCGA):
        TCGA = 0
    for fileName in files:
        imgRootName = os.path.basename(fileName).replace(".FPKM.txt.npy", "")[-36:]
        ID = -1
        for TotImg in range(len(jdata)):
            if jdata[TotImg]['file_name'].startswith(imgRootName):
                case = jdata[TotImg]['cases'][0]['case_id']
                ID = TotImg
                break
 
        if ID == -1:
            print("File name not found in json file.")
            continue
        cnt += 1
        print("***** ", fileName, cnt)

        project = df_clin.loc[case].loc["project_id"]
        # gender = df_clin.loc[case].loc["gender"]
        # vital = df_clin.loc[case].loc["vital_status"]
        origin = df_clin.loc[case].loc["tissue_or_organ_of_origin"]
        # prior = df_clin.loc[case].loc["prior_malignancy"]
        patho = df_clin.loc[case].loc["primary_diagnosis"]
        # stage = df_clin.loc[case].loc["tumor_stage"]
        # ann_stage = df_clin.loc[case].loc["ann_arbor_clinical_stage"]

        # vital = vital.replace(" ", "_")
        origin = origin.replace(" ", "_")
        origin = origin.replace(",_NOS", "")
        # prior = prior.replace(" ", "_")
        # stage = str(stage)
        # stage = stage.replace(" ", "")
        # stage = stage.replace("stage", "")
        # stage = stage.replace('a','')
        # stage = stage.replace('b','')
        # ann_stage = ann_stage.replace(" ", "")
        # ann_stage = ann_stage.replace("stage", "")
        # ann_stage = ann_stage.replace('a','')
        # ann_stage = ann_stage.replace('b','')
        
        
        # pathology classification based on OncoTree
        
        # exclude: Acute Leukemias of Ambiguous Lineage, because of its ambiguous disease entity
        # exclude: Undifferentiated pleomorphic sarcoma, called a diagnosis of exclusion

        patho = project + '_' + patho
        patho = patho.replace(" ", "_")
        patho = patho.replace(",_NOS", "")
        
        patho = patho.replace("BEATAML1.0-COHORT_Acute_monoblastic_and_monocytic_leukemia", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia,_CBF-beta", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia_with_inv(3)(q21q26.2)_or_t(3;3)(q21;q26.2);_RPN1-EVI1", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia_with_mutated_CEBPA", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Mixed_phenotype_acute_leukemia,_T", "other")
        patho = patho.replace("BEATAML1.0-COHORT_Mixed_phenotype_acute_leukemia,_B", "other")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia_with_mutated_NPM1", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia_with_myelodysplasia-related_changes", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia_with_t(8;21)(q22;q22);_RUNX1-RUNX1T1", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia_with_t(9;11)(p22;q23);_MLLT3-MLL", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Myeloid_sarcoma", "other")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myelomonocytic_leukemia", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_promyelocytic_leukaemia,_PML-RAR-alpha", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_erythroid_leukaemia", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Myeloid_leukemia_associated_with_Down_Syndrome", "Acute Myeloid Leukemia")
        patho = patho.replace("BEATAML1.0-COHORT_Acute_myeloid_leukemia", "Acute Myeloid Leukemia")
        patho = patho.replace("CGCI-BLGSP_--", "other")
        patho = patho.replace("CGCI-BLGSP_Burkitt-like_lymphoma", "other")
        patho = patho.replace("CGCI-BLGSP_Burkitt_lymphoma", "Burkitt_lymphoma")
        patho = patho.replace("CPTAC-3_Adenocarcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("CPTAC-3_Endometrioid_adenocarcinoma", "Uterine Endometrial Carcinoma")
        patho = patho.replace("CPTAC-3_Renal_cell_carcinoma", "Kidney_Renal Clear Cell Carcinoma")
        patho = patho.replace("CTSP-DLBCL1_Diffuse_large_B-cell_lymphoma", "Diffuse Large B-Cell Lymphoma")
        patho = patho.replace("HCMI-CMDC_Adenocarcinoma", origin + " Adenocarcinoma")
        patho = patho.replace("HCMI-CMDC_Glioblastoma", "Brain_Glioblastoma")
        patho = patho.replace("MMRF-COMMPASS_--", "other")
        patho = patho.replace("MMRF-COMMPASS_Multiple_myeloma", "Multiple_Myeloma")
        patho = patho.replace("NCICCR-DLBCL_Diffuse_large_B-cell_lymphoma", "Diffuse Large B-Cell Lymphoma")        
        patho = patho.replace("TARGET-ALL-P1_Mixed_phenotype_acute_leukemia,_T/myeloid", "other")
        patho = patho.replace("TARGET-ALL-P1_T_lymphoblastic_leukemia/lymphoma", "T-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P1_Precursor_B-cell_lymphoblastic_leukemia", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P1_Mixed_phenotype_acute_leukemia,_B/myeloid", "other")
        patho = patho.replace("TARGET-ALL-P1_Mixed_phenotype_acute_leukemia_with_t(v;11q23);_MLL_rearranged", "other")
        patho = patho.replace("TARGET-ALL-P1_Undifferentiated_leukaemia", "other")
        patho = patho.replace("TARGET-ALL-P1_Mixed_phenotype_acute_leukemia_with_t(9;22)(q34;q11.2);_BCR-ABL1", "other")
        patho = patho.replace("TARGET-ALL-P1_Leukemia", "other")
        patho = patho.replace("TARGET-ALL-P1_B_lymphoblastic_leukemia/lymphoma", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P1_Juvenile_myelomonocytic_leukemia", "other")
        patho = patho.replace("TARGET-ALL-P1_--", "other")
        patho = patho.replace("TARGET-ALL-P2_Mixed_phenotype_acute_leukemia,_T/myeloid", "other")
        patho = patho.replace("TARGET-ALL-P2_T_lymphoblastic_leukemia/lymphoma", "T-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P2_Precursor_B-cell_lymphoblastic_leukemia", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P2_Mixed_phenotype_acute_leukemia,_B/myeloid", "other")
        patho = patho.replace("TARGET-ALL-P2_Mixed_phenotype_acute_leukemia_with_t(v;11q23);_MLL_rearranged", "other")
        patho = patho.replace("TARGET-ALL-P2_Undifferentiated_leukaemia", "other")
        patho = patho.replace("TARGET-ALL-P2_Mixed_phenotype_acute_leukemia_with_t(9;22)(q34;q11.2);_BCR-ABL1", "other")
        patho = patho.replace("TARGET-ALL-P2_Leukemia", "other")
        patho = patho.replace("TARGET-ALL-P2_B_lymphoblastic_leukemia/lymphoma", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P2_Juvenile_myelomonocytic_leukemia", "other")
        patho = patho.replace("TARGET-ALL-P3_Mixed_phenotype_acute_leukemia,_T/myeloid", "other")
        patho = patho.replace("TARGET-ALL-P3_T_lymphoblastic_leukemia/lymphoma", "T-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P3_Precursor_B-cell_lymphoblastic_leukemia", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P3_Mixed_phenotype_acute_leukemia,_B/myeloid", "other")
        patho = patho.replace("TARGET-ALL-P3_Mixed_phenotype_acute_leukemia_with_t(v;11q23);_MLL_rearranged", "other")
        patho = patho.replace("TARGET-ALL-P3_Undifferentiated_leukaemia", "other")
        patho = patho.replace("TARGET-ALL-P3_Mixed_phenotype_acute_leukemia_with_t(9;22)(q34;q11.2);_BCR-ABL1", "other")
        patho = patho.replace("TARGET-ALL-P3_Leukemia", "other")
        patho = patho.replace("TARGET-ALL-P3_B_lymphoblastic_leukemia/lymphoma", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P3_Juvenile_myelomonocytic_leukemia", "other")
        patho = patho.replace("TARGET-ALL-P3_Not_Reported", "other")
        patho = patho.replace("TARGET-ALL-P3_Mixed_phenotype_acute_leukemia_with_t(9;22)(q34;q11.2);_BCR-ABL1", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P3_Mixed_phenotype_acute_leukemia_with_t(v;11q23);_MLL_rearranged", "B-Lymphoblastic Leukemia-Lymphoma")
        patho = patho.replace("TARGET-ALL-P3_Acute_myeloid_leukemia", "Acute_Myeloid_Leukemia")
        patho = patho.replace("TARGET-AML_Acute_myeloid_leukemia", "Acute Myeloid Leukemia")
        patho = patho.replace("TARGET-CCSK_Clear_cell_sarcoma_of_kidney", "Kidney_Clear Cell Sarcoma of Kidney")
        patho = patho.replace("TARGET-NBL_Neuroblastoma", "Neuroblastoma-Ganglioneuroblastoma")
        patho = patho.replace("TARGET-NBL_Ganglioneuroblastoma", "Neuroblastoma-Ganglioneuroblastoma")
        patho = patho.replace("TARGET-OS_Osteosarcoma", "Bone_Osteosarcoma")
        patho = patho.replace("TARGET-RT_Malignant_rhabdoid_tumor", "Rhabdoid Cancer")
        patho = patho.replace("TARGET-WT_Wilms_tumor", "Wilms Tumor")
        patho = patho.replace("TCGA-ACC_Adrenal_cortical_carcinoma", "Adrenocortical Carcinoma")
        patho = patho.replace("TCGA-BLCA_Carcinoma", "other")
        patho = patho.replace("TCGA-BLCA_Papillary_adenocarcinoma", "other")
        patho = patho.replace("TCGA-BLCA_Papillary_transitional_cell_carcinoma", "Bladder Urothelial Carcinoma")
        patho = patho.replace("TCGA-BLCA_Squamous_cell_carcinoma", "other")
        patho = patho.replace("TCGA-BLCA_Transitional_cell_carcinoma", "Bladder Urothelial Carcinoma")        
        patho = patho.replace("TCGA-BRCA_--", "other")
        patho = patho.replace("TCGA-BRCA_Adenoid_cystic_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Apocrine_adenocarcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Basal_cell_carcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Carcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Cribriform_carcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Infiltrating_duct_and_lobular_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Infiltrating_duct_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Infiltrating_duct_mixed_with_other_types_of_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Infiltrating_lobular_mixed_with_other_types_of_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Intraductal_micropapillary_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Intraductal_papillary_adenocarcinoma_with_invasion", "Breast_Invasive Breast Carcinoma")        
        patho = patho.replace("TCGA-BRCA_Large_cell_neuroendocrine_carcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Lobular_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Medullary_carcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Metaplastic_carcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Mucinous_adenocarcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Paget_disease_and_infiltrating_duct_carcinoma_of_breast", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Papillary_carcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-BRCA_Phyllodes_tumor", "other")
        patho = patho.replace("TCGA-BRCA_Pleomorphic_carcinoma", "other")
        patho = patho.replace("TCGA-BRCA_Secretory_carcinoma_of_breast", "other")
        patho = patho.replace("TCGA-BRCA_Tubular_adenocarcinoma", "Breast_Invasive Breast Carcinoma")
        patho = patho.replace("TCGA-CESC_Adenocarcinoma", "other")
        patho = patho.replace("TCGA-CESC_Adenosquamous_carcinoma", "other")
        patho = patho.replace("TCGA-CESC_Basaloid_squamous_cell_carcinoma", "Cervical Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-CESC_Endometrioid_adenocarcinoma", "Cervical Adenocarcinoma")
        patho = patho.replace("TCGA-CESC_Mucinous_adenocarcinoma", "Cervical Adenocarcinoma")
        patho = patho.replace("TCGA-CESC_Papillary_squamous_cell_carcinoma", "Cervical Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-CESC_Squamous_cell_carcinoma", "Cervical Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-CHOL_Cholangiocarcinoma", "Cholangiocarcinoma")
        patho = patho.replace("TCGA-COAD_--", "other")
        patho = patho.replace("TCGA-COAD_Adenocarcinoma", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-COAD_Adenosquamous_carcinoma", "other")        
        patho = patho.replace("TCGA-COAD_Carcinoma", "other")
        patho = patho.replace("TCGA-COAD_Mucinous_adenocarcinoma", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-COAD_Papillary_adenocarcinoma", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-DLBC_Diffuse_large_B-cell_lymphoma", "Diffuse Large B-Cell Lymphoma")
        patho = patho.replace("TCGA-DLBC_Malignant_lymphoma,_large_B-cell,_diffuse", "Diffuse Large B-Cell Lymphoma")
        patho = patho.replace("TCGA-ESCA_Adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-ESCA_Basaloid_squamous_cell_carcinoma", origin + " Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-ESCA_Mucinous_adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-ESCA_Squamous_cell_carcinoma", origin + " Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-ESCA_Tubular_adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-GBM_--", "other")
        patho = patho.replace("TCGA-GBM_Glioblastoma", "Brain_Glioblastoma")        
        patho = patho.replace("TCGA-HNSC_Basaloid_squamous_cell_carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-HNSC_Squamous_cell_carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-KICH_Renal_cell_carcinoma", "Kidney_Chromophobe Renal Cell Carcinoma")
        patho = patho.replace("TCGA-KIRC_Clear_cell_adenocarcinoma", "Kidney_Renal Clear Cell Carcinoma")
        patho = patho.replace("TCGA-KIRC_Renal_cell_carcinoma", "other")
        patho = patho.replace("TCGA-KIRP_Papillary_adenocarcinoma", "Kidney_Papillary Renal Cell Carcinoma")
        patho = patho.replace("TCGA-LAML_Acute_myeloid_leukemia", "Acute Myeloid Leukemia")
        patho = patho.replace("TCGA-LGG_--", "other")
        patho = patho.replace("TCGA-LGG_Astrocytoma", "Brain_Oligodendroglioma-Astrocytoma")
        patho = patho.replace("TCGA-LGG_Mixed_glioma", "Brain_Oligodendroglioma-Astrocytoma")
        patho = patho.replace("TCGA-LGG_Oligodendroglioma", "Brain_Oligodendroglioma-Astrocytoma")
        patho = patho.replace("TCGA-LIHC_Clear_cell_adenocarcinoma", "other")        
        patho = patho.replace("TCGA-LIHC_Combined_hepatocellular_carcinoma_and_cholangiocarcinoma", "other")
        patho = patho.replace("TCGA-LIHC_Hepatocellular_carcinoma", "Hepatocellular Carcinoma")
        patho = patho.replace("TCGA-LUAD_Acinar_cell_carcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("TCGA-LUAD_Adenocarcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("TCGA-LUAD_Bronchio-alveolar_carcinoma,_mucinous", "other")
        patho = patho.replace("TCGA-LUAD_Bronchiolo-alveolar_adenocarcinoma", "other")
        patho = patho.replace("TCGA-LUAD_Bronchiolo-alveolar_carcinoma,_non-mucinous", "other")
        patho = patho.replace("TCGA-LUAD_Clear_cell_adenocarcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("TCGA-LUAD_Micropapillary_carcinoma", "Lung Adenocarcinoma")        
        patho = patho.replace("TCGA-LUAD_Mucinous_adenocarcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("TCGA-LUAD_Papillary_adenocarcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("TCGA-LUAD_Signet_ring_cell_carcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("TCGA-LUAD_Solid_carcinoma", "Lung Adenocarcinoma")
        patho = patho.replace("TCGA-LUSC_Basaloid_squamous_cell_carcinoma", "Lung Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-LUSC_Papillary_squamous_cell_carcinoma", "Lung Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-LUSC_Squamous_cell_carcinoma,_keratinizing", "Lung Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-LUSC_Squamous_cell_carcinoma,_large_cell,_nonkeratinizing", "Lung Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-LUSC_Squamous_cell_carcinoma,_small_cell,_nonkeratinizing", "Lung Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-LUSC_Squamous_cell_carcinoma", "Lung Squamous Cell Carcinoma")
        patho = patho.replace("TCGA-MESO_Epithelioid_mesothelioma,_malignant", "Pleural Mesothelioma")        
        patho = patho.replace("TCGA-MESO_Fibrous_mesothelioma,_malignant", "Pleural Mesothelioma")
        patho = patho.replace("TCGA-MESO_Mesothelioma,_biphasic,_malignant", "Pleural Mesothelioma")
        patho = patho.replace("TCGA-MESO_Mesothelioma,_malignant", "Pleural Mesothelioma")
        patho = patho.replace("TCGA-OV_Papillary_serous_cystadenocarcinoma", "Ovary_Serous Ovarian Cancer")
        patho = patho.replace("TCGA-OV_Serous_cystadenocarcinoma", "Ovary_Serous Ovarian Cancer")
        patho = patho.replace("TCGA-PAAD_Adenocarcinoma_with_mixed_subtypes", "Pancreatic Adenocarcinoma")
        patho = patho.replace("TCGA-PAAD_Adenocarcinoma", "Pancreatic Adenocarcinoma")
        patho = patho.replace("TCGA-PAAD_Carcinoma,_undifferentiated", "other")
        patho = patho.replace("TCGA-PAAD_Infiltrating_duct_carcinoma", "Pancreatic Adenocarcinoma")
        patho = patho.replace("TCGA-PAAD_Mucinous_adenocarcinoma", "Pancreatic Adenocarcinoma")
        patho = patho.replace("TCGA-PAAD_Neuroendocrine_carcinoma", "other")        
        patho = patho.replace("TCGA-PCPG_Extra-adrenal_paraganglioma,_malignant", "Pheochromocytoma-Paraganglioma")
        patho = patho.replace("TCGA-PCPG_Extra-adrenal_paraganglioma", "Pheochromocytoma-Paraganglioma")
        patho = patho.replace("TCGA-PCPG_Paraganglioma,_malignant", "Pheochromocytoma-Paraganglioma")
        patho = patho.replace("TCGA-PCPG_Paraganglioma", "Pheochromocytoma-Paraganglioma")
        patho = patho.replace("TCGA-PCPG_Pheochromocytoma,_malignant", "Pheochromocytoma-Paraganglioma")
        patho = patho.replace("TCGA-PCPG_Pheochromocytoma", "Pheochromocytoma-Paraganglioma")
        patho = patho.replace("TCGA-PRAD_Adenocarcinoma_with_mixed_subtypes", "Prostate Adenocarcinoma")
        patho = patho.replace("TCGA-PRAD_Adenocarcinoma", "Prostate Adenocarcinoma")
        patho = patho.replace("TCGA-PRAD_Infiltrating_duct_carcinoma", "Prostate Adenocarcinoma")
        patho = patho.replace("TCGA-PRAD_Mucinous_adenocarcinoma", "Prostate Adenocarcinoma")
        patho = patho.replace("TCGA-READ_--", "other")
        patho = patho.replace("TCGA-READ_Adenocarcinoma_in_tubolovillous_adenoma", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-READ_Adenocarcinoma_with_mixed_subtypes", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-READ_Adenocarcinoma", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-READ_Mucinous_adenocarcinoma", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-READ_Tubular_adenocarcinoma", "Colorectal Adenocarcinoma")
        patho = patho.replace("TCGA-SARC_Abdominal_fibromatosis", "other")
        patho = patho.replace("TCGA-SARC_Aggressive_fibromatosis", "other")
        patho = patho.replace("TCGA-SARC_Dedifferentiated_liposarcoma", "STS_Dedifferentiated liposarcoma")
        patho = patho.replace("TCGA-SARC_Fibromyxosarcoma", "STS_Myxofibrosarcoma")
        patho = patho.replace("TCGA-SARC_Giant_cell_sarcoma", "other")
        patho = patho.replace("TCGA-SARC_Leiomyosarcoma", "STS_Leiomyosarcoma")
        patho = patho.replace("TCGA-SARC_Liposarcoma,_well_differentiated", "other")
        patho = patho.replace("TCGA-SARC_Malignant_fibrous_histiocytoma", "other")
        patho = patho.replace("TCGA-SARC_Malignant_peripheral_nerve_sheath_tumor", "other")
        patho = patho.replace("TCGA-SARC_Myxoid_leiomyosarcoma", "STS_Leiomyosarcoma")
        patho = patho.replace("TCGA-SARC_Pleomorphic_liposarcoma", "other")
        patho = patho.replace("TCGA-SARC_Synovial_sarcoma,_biphasic", "STS_Synovial Sarcoma")
        patho = patho.replace("TCGA-SARC_Synovial_sarcoma,_spindle_cell", "STS_Synovial Sarcoma")
        patho = patho.replace("TCGA-SARC_Synovial_sarcoma", "STS_Synovial Sarcoma")
        patho = patho.replace("TCGA-SARC_Undifferentiated_sarcoma", "other")
        patho = patho.replace("TCGA-SKCM_Acral_lentiginous_melanoma,_malignant", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Desmoplastic_melanoma,_malignant", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Amelanotic_melanoma", "Cutaneous Melanoma")        
        patho = patho.replace("TCGA-SKCM_Epithelioid_cell_melanoma", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Lentigo_maligna_melanoma", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Malignant_melanoma", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Mixed_epithelioid_and_spindle_cell_melanoma", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Nodular_melanoma", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Spindle_cell_melanoma", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-SKCM_Superficial_spreading_melanoma", "Cutaneous Melanoma")
        patho = patho.replace("TCGA-STAD_Adenocarcinoma_with_mixed_subtypes", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-STAD_Adenocarcinoma,_intestinal_type", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-STAD_Adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-STAD_Carcinoma,_diffuse_type", "Esophagogastric Adenocarcinoma")        
        patho = patho.replace("TCGA-STAD_Mucinous_adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-STAD_Papillary_adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-STAD_Signet_ring_cell_carcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-STAD_Tubular_adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("TCGA-TGCT_--", "other")
        patho = patho.replace("TCGA-TGCT_Embryonal_carcinoma", "GCT_Non-Seminomatous Germ Cell Tumor")
        patho = patho.replace("TCGA-TGCT_Mixed_germ_cell_tumor", "GCT_Non-Seminomatous Germ Cell Tumor")
        patho = patho.replace("TCGA-TGCT_Seminoma", "GCT_Seminoma")
        patho = patho.replace("TCGA-TGCT_Teratocarcinoma", "GCT_Non-Seminomatous Germ Cell Tumor")
        patho = patho.replace("TCGA-TGCT_Teratoma,_benign", "GCT_Non-Seminomatous Germ Cell Tumor")
        patho = patho.replace("TCGA-TGCT_Teratoma,_malignant", "GCT_Non-Seminomatous Germ Cell Tumor")
        patho = patho.replace("TCGA-TGCT_Yolk_sac_tumor", "GCT_Non-Seminomatous Germ Cell Tumor")
        patho = patho.replace("TCGA-THCA_Carcinoma", "other")
        patho = patho.replace("TCGA-THCA_Follicular_carcinoma,_minimally_invasive", "other")
        patho = patho.replace("TCGA-THCA_Follicular_adenocarcinoma", "other")
        patho = patho.replace("TCGA-THCA_Nonencapsulated_sclerosing_carcinoma", "other")
        patho = patho.replace("TCGA-THCA_Oxyphilic_adenocarcinoma", "other")
        patho = patho.replace("TCGA-THCA_Papillary_carcinoma,_columnar_cell", "Papillary Thyroid Cancer")        
        patho = patho.replace("TCGA-THCA_Papillary_carcinoma,_follicular_variant", "Papillary Thyroid Cancer")
        patho = patho.replace("TCGA-THCA_Papillary_adenocarcinoma", "Papillary Thyroid Cancer")
        patho = patho.replace("TCGA-THYM_Thymic_carcinoma", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_AB,_malignant", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_AB", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_A,_malignant", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_A", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_B1,_malignant", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_B1", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_B2,_malignant", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_B2", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-THYM_Thymoma,_type_B3,_malignant", "Thymic Epithelial Tumor")
        patho = patho.replace("TCGA-UCEC_Adenocarcinoma", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCEC_Carcinoma,_undifferentiated", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCEC_Clear_cell_adenocarcinoma", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCEC_Endometrioid_adenocarcinoma,_secretory_variant", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCEC_Endometrioid_adenocarcinoma", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCEC_Not_Reported", "other")
        patho = patho.replace("TCGA-UCEC_Papillary_serous_cystadenocarcinoma", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCEC_Serous_cystadenocarcinoma", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCEC_Serous_surface_papillary_carcinoma", "Uterine Endometrial Carcinoma")
        patho = patho.replace("TCGA-UCS_Carcinosarcoma", "Uterine Carcinosarcoma")
        patho = patho.replace("TCGA-UCS_Mesodermal_mixed_tumor", "Uterine Carcinosarcoma")
        patho = patho.replace("TCGA-UCS_Mullerian_mixed_tumor", "Uterine Carcinosarcoma")
        patho = patho.replace("TCGA-UVM_Epithelioid_cell_melanoma", "Uveal Melanoma")
        patho = patho.replace("TCGA-UVM_Malignant_melanoma", "Uveal Melanoma")
        patho = patho.replace("TCGA-UVM_Mixed_epithelioid_and_spindle_cell_melanoma", "Uveal Melanoma")
        patho = patho.replace("TCGA-UVM_Spindle_cell_melanoma,_type_B", "Uveal Melanoma")
        patho = patho.replace("TCGA-UVM_Spindle_cell_melanoma", "Uveal Melanoma")
        
        patho = patho.replace("Esophagus", "Esophageal")
        patho = patho.replace("Rectum", "Rectal")
        patho = patho.replace("Rectosigmoid junction", "Rectal")
        patho = patho.replace("Stomach Squamous Cell Carcinoma", "other")
        patho = patho.replace("Unknown primary site Mucinous adenocarcinoma", "other")

        patho = patho.replace(" ", "_")

        patho = patho.replace(",_anaplastic", "")
        patho = patho.replace("Head_and_Neck_Squamous_Cell_Carcinoma,_keratinizing", "Head_and_Neck_Squamous_Cell_Carcinoma")
        patho = patho.replace("Head_and_Neck_Squamous_Cell_Carcinoma,_large_cell,_nonkeratinizing", "Head_and_Neck_Squamous_Cell_Carcinoma")
        patho = patho.replace("Head_and_Neck_Squamous_Cell_Carcinoma,_spindle_cell", "Head_and_Neck_Squamous_Cell_Carcinoma")
        patho = patho.replace(",_malignant", "")
        patho = patho.replace("Cardia_Squamous_Cell_Carcinoma", "other")
        patho = patho.replace("Cardia_Adenocarcinoma", "other")
        patho = patho.replace("Cecum_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Cervical_Squamous_Cell_Carcinoma,_keratinizing", "Cervical_Squamous_Cell_Carcinoma")
        patho = patho.replace("Cervical_Squamous_Cell_Carcinoma,_large_cell,_nonkeratinizing", "Cervical_Squamous_Cell_Carcinoma")
        patho = patho.replace(",_endocervical_type", "")

        patho = patho.replace("Rectal_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Colon_Adenocarcinoma", "Colorectal_Adenocarcinoma")

        patho = patho.replace("Acute_Myeloid_Leukemia,_minimal_differentiation", "Acute_Myeloid_Leukemia")
        patho = patho.replace("Acute_Myeloid_Leukemia_with_maturation", "Acute_Myeloid_Leukemia")
        patho = patho.replace("Acute_Myeloid_Leukemia_without_maturation", "Acute_Myeloid_Leukemia")

        patho = patho.replace("Colorectal_Adenocarcinoma_with_mixed_subtypes", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Colorectal_Adenocarcinoma_with_neuroendocrine_differentiation", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Descending_colon_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Esophageal_Squamous_Cell_Carcinoma,_keratinizing", "Esophageal_Squamous_Cell_Carcinoma")
        patho = patho.replace("Floor_of_mouth_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Floor_of_mouth_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Gum_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Gum_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Hard_palate_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Head_and_Neck_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Hepatic_flexure_of_colon_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Hepatocellular_Carcinoma,_clear_cell_type", "Hepatocellular Carcinoma")
        patho = patho.replace("Hepatocellular_Carcinoma,_fibrolamellar", "Hepatocellular Carcinoma")
        patho = patho.replace("Hepatocellular_Carcinoma,_spindle_cell_variant", "Hepatocellular Carcinoma")
        patho = patho.replace("Hypopharynx_Squamous_Cell_Carcinoma,_large_cell,_nonkeratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Hypopharynx_Squamous_Cell_Carcinoma,_large_cell,_nonkeratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Chromophobe_Renal_Cell_Carcinoma,_chromophobe_type", "Chromophobe_Renal_Cell_Carcinoma")
        patho = patho.replace("Larynx_Squamous_Cell_Carcinoma,_large_cell,_nonkeratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Lip_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Lip_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Lower_gum_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Lower_third_of_esophagus_Squamous_Cell_Carcinoma,_keratinizing", "Esophageal Squamous Cell Carcinoma")
        patho = patho.replace("Lower_third_of_esophagus_Adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("Lower_third_of_esophagus_Squamous_Cell_Carcinoma", "Esophageal Squamous Cell Carcinoma")
        patho = patho.replace("Lung_Adenocarcinoma_with_mixed_subtypes", "Lung_Adenocarcinoma")
        patho = patho.replace("Mandible_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Middle_third_of_esophagus_Squamous_Cell_Carcinoma", "Esophageal Squamous Cell Carcinoma")
        patho = patho.replace("Middle_third_of_esophagus_Adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("Mouth_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Mouth_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Mucinous_Adenocarcinoma_of_the_Colon_and_Rectal", "Colorectal Adenocarcinoma")
        patho = patho.replace("Burkitt_lymphoma_(Includes_all_variants)", "Burkitt_lymphoma")
        patho = patho.replace("Oropharynx_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Oropharynx_Squamous_Cell_Carcinoma,_spindle_cell", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Overlapping_lesion_of_lip,_oral_cavity_and_pharynx_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Palate_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Pharynx_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Phyllodes_Tumor_of_the_Breast,_malignant", "other")
        patho = patho.replace("Posterior_wall_of_oropharynx_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Rectosigmoid_junction_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Renal_Non-Clear_Cell_Carcinoma,_chromophobe_type", "Renal_Non-Clear_Cell_Carcinoma")
        patho = patho.replace("Retromolar_area_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Sigmoid_colon_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Splenic_flexure_of_colon_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Supraglottis_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Thoracic_esophagus_Adenocarcinoma", "Esophagogastric Adenocarcinoma")
        patho = patho.replace("Tongue_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Tongue_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Tonsil_Squamous_Cell_Carcinoma,_keratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Tonsil_Squamous_Cell_Carcinoma,_large_cell,_nonkeratinizing", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Tonsil_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Transverse_colon_Adenocarcinoma", "Colorectal_Adenocarcinoma")
        patho = patho.replace("Unknown_primary_site_Adenocarcinoma", "other")
        patho = patho.replace("Upper_Gum_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Upper_third_of_esophagus_Squamous_Cell_Carcinoma", "Esophageal Squamous Cell Carcinoma")
        patho = patho.replace("Ventral_surface_of_tongue_Squamous_Cell_Carcinoma", "Head and Neck Squamous Cell Carcinoma")
        patho = patho.replace("Connective,_subcutaneous_and_other_soft_tissues_of_abdomen_Adenocarcinoma", "other")

        patho = patho.replace("Acute_Myeloid_Leukemia", "Myeloid_Acute_Myeloid_Leukemia")
        patho = patho.replace("Thymic_Epithelial_Tumor", "Thymus_Thymic_Epithelial_Tumor")
        patho = patho.replace("Burkitt_lymphoma", "Lymphoid_Burkitt_lymphoma")
        patho = patho.replace("B-Lymphoblastic_Leukemia-Lymphoma", "Lymphoid_B-Lymphoblastic_Leukemia-Lymphoma")
        patho = patho.replace("Diffuse_Large_B-Cell_Lymphoma", "Lymphoid_Diffuse_Large_B-Cell_Lymphoma")
        patho = patho.replace("Multiple_Myeloma", "Lymphoid_Multiple_Myeloma")
        patho = patho.replace("Papillary_Thyroid_Cancer", "Thyroid_Papillary_Cancer")
        patho = patho.replace("T-Lymphoblastic_Leukemia-Lymphoma", "Lymphoid_T-Lymphoblastic_Leukemia-Lymphoma")

        patho = patho.replace("TCGA-SARC_Dedifferentiated_liposarcoma", "STS_Dedifferentiated liposarcoma")
        patho = patho.replace("TCGA-SARC_Fibromyxosarcoma", "STS_Myxofibrosarcoma")
        patho = patho.replace("TCGA-SARC_Giant_cell_sarcoma", "other")
        patho = patho.replace("TCGA-SARC_Leiomyosarcoma", "STS_Leiomyosarcoma")
        patho = patho.replace("TCGA-SARC_Liposarcoma,_well_differentiated", "other")
        patho = patho.replace("TCGA-SARC_Malignant_fibrous_histiocytoma", "other")
        patho = patho.replace("TCGA-SARC_Malignant_peripheral_nerve_sheath_tumor", "other")
        patho = patho.replace("TCGA-SARC_Myxoid_leiomyosarcoma", "STS_Leiomyosarcoma")
        patho = patho.replace("TCGA-SARC_Pleomorphic_liposarcoma", "other")
        patho = patho.replace("TCGA-SARC_Synovial_sarcoma,_biphasic", "STS_Synovial Sarcoma")

        patho = patho.replace(" ", "_")
        SubDir = opts.sorted_patho + '/' + patho
        Other = opts.sorted_patho + '/other'

        if patho == "STS_Dedifferentiated_liposarcoma" or patho == "STS_Myxofibrosarcoma" or patho == "STS_Leiomyosarcoma" or patho == "STS_Synovial_Sarcoma":
            if not os.path.exists(SubDir):
                os.makedirs(SubDir)
            NewImageDir = os.path.join(SubDir, ("{}_{}.npy".format(os.path.basename(fileName).replace(".FPKM.txt.npy", ""), project)))
            os.symlink(fileName, NewImageDir)
        else:
            if not os.path.exists(Other):
                os.makedirs(Other)
            NewImageDir = os.path.join(Other, ("{}_{}.npy".format(os.path.basename(fileName).replace(".FPKM.txt.npy", ""), project)))
            os.symlink(fileName, NewImageDir)

        
        if project.startswith("TCGA"):
            if(TCGA == 1):
                SubDir = opts.sorted_TCGA + '/' + project
                if not os.path.exists(SubDir):
                    os.makedirs(SubDir)
                NewImageDir = os.path.join(SubDir, ("{}_{}.npy".format(os.path.basename(fileName).replace(".FPKM.txt.npy", ""), project)))
                os.symlink(fileName, NewImageDir)
