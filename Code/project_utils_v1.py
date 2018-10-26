"""
CS109a, Fall 2017
Utility functions for the final project.
"""
import pandas as pd
import numpy as np

def get_data():
    adnimerge = pd.read_csv("./data/ADNIMERGE.csv")
    adnimerge = adnimerge[['RID', 'DX_bl', 'DX', 'Month']]
    # Removing baseline diagnosis = AD
    adnimerge = adnimerge[adnimerge.DX_bl != 'AD']
    p = adnimerge[['RID', 'Month', 'DX']]
    #Remove entries with NaN
    p = p.dropna(axis=0, how='any')
    #Find the Max diagnosis for each subject
    p1 = p.groupby("RID")['Month'].max()
    q = pd.DataFrame({'RID': p1.index, 'Month': p1})
    k = pd.read_csv("./data/ADNIMERGE.csv")
    k = k[['RID', 'Month', 'DX']]
    k = k.dropna(axis=0, how='any')
    k = k.drop_duplicates()
    #Get the final diagnosis
    df = pd.merge(q, k, how='inner', on=['RID', 'Month'])
    del df['Month']
    #Making a copy of the dataset
    x1 = df.copy()

    #Adding adnimerge data
    # Includes baseline scores of brain scans, various NP tests - MMSE, FAQ, ADAS, Gender, Marital status, race, APOE4
    adnimerge = pd.read_csv("./data/ADNIMERGE.csv")
    adnimerge = adnimerge[adnimerge.VISCODE == 'bl']
    c = adnimerge.columns.tolist()
    # Removing fields that are not baseline measurements
    q = ['PTID', 'VISCODE', 'SITE', 'COLPROT', 'ORIGPROT', 'EXAMDATE_bl', 'PTETHCAT', 'FDG', 'PIB', 'AV45', 'CDRSB',
         'ADAS11', 'ADAS13','MMSE', 'RAVLT_immediate', 'RAVLT_learning', 'RAVLT_forgetting', 'RAVLT_perc_forgetting', 'FAQ', 'MOCA',
         'EcogPtMem', 'EcogPtLang', 'EcogPtVisspat', 'EcogPtPlan', 'EcogPtOrgan', 'EcogPtDivatt', 'EcogPtTotal', 'EcogSPMem',
         'EcogSPLang', 'EcogSPVisspat', 'EcogSPPlan', 'EcogSPOrgan', 'EcogSPDivatt', 'EcogSPTotal', 'FLDSTRENG', 'FSVERSION',
         'Ventricles', 'Hippocampus', 'WholeBrain', 'Entorhinal', 'Fusiform', 'MidTemp', 'ICV', 'DX', 'update_stamp', 'Month_bl',
         'Month', 'M', 'Years_bl', 'EXAMDATE', 'DX_bl', 'FLDSTRENG_bl', 'FSVERSION_bl',
         # This has very high missingness
         'PIB_bl',
         # Turns out these are measured for few subjects
         'EcogPtMem_bl', 'EcogSPPlan_bl', 'EcogPtPlan_bl', 'EcogPtDivatt_bl', 'MOCA_bl', 'EcogPtVisspat_bl',
         'EcogSPMem_bl', 'EcogSPVisspat_bl', 'EcogSPOrgan_bl', 'EcogPtTotal_bl', 'EcogSPLang_bl', 'AV45_bl', 'EcogSPTotal_bl',
         'EcogPtOrgan_bl','EcogSPDivatt_bl', 'EcogPtOrgan_bl', 'EcogSPDivatt_bl', 'EcogPtLang_bl', 'FDG_bl', 'PIB_bl'
         ]

    p = list(set(c) - set(q))
    adnimerge = adnimerge[p]
    x1 = pd.merge(x1, adnimerge, how='inner', on=['RID'])

    # Intergrating UWNPSYCHSUM - composite scores from UPENN
    mem = pd.read_csv("./data/UWNPSYCHSUM_10_27_17.csv")
    mem = mem[mem.VISCODE == "bl"]
    mem = mem[['RID', 'ADNI_MEM', 'ADNI_EF']]
    mem.columns = ['RID', 'ADNI_MEM_bl', 'ADNI_EF_bl']
    x1 = pd.merge(x1, mem, how='left', on='RID')

    # Integratuing select columns from medical history
    a1 = pd.read_csv("./data/MEDHIST.csv")
    a1 = a1[a1.VISCODE == 'sc']
    # Gives medical history of issues related to neurological, phyciatry, cardiovascular, hepatic, dematological, muscular, endothelial, gastro-intestinal,
    #hematological, renal, allergies, alcoholic, smoking, cancer or any past surgeries
    v = ['RID', 'MHPSYCH', 'MH2NEURL', 'MH3HEAD', 'MH4CARD', 'MH5RESP', 'MH6HEPAT', 'MH7DERM', 'MH8MUSCL', 'MH9ENDO',
         'MH10GAST','MH11HEMA', 'MH12RENA', 'MH13ALLE', 'MH14ALCH', 'MH15DRUG', 'MH16SMOK', 'MH17MALI', 'MH18SURG', 'MH19OTHR']
    a1 = a1[v]
    x1 = pd.merge(x1, a1, how='left', on='RID')

    # Integrating history of stroke, hypertension. Stroke may be a confounder for Dementia
    # Intergrating NP tests scores such as modified Hachinski, Geriatric scale score
    a1 = pd.read_csv("./data/MODHACH.csv")
    a1 = a1[a1.VISCODE == 'sc']
    v = ['RID', 'HMHYPERT', 'HMSTROKE', 'HMSCORE']
    a1 = a1[v]
    x1 = pd.merge(x1, a1, how='left', on='RID')

    # GDSCALE score - depression scores
    a1 = pd.read_csv("./data/GDSCALE.csv")
    a1 = a1[a1.VISCODE == 'sc']
    v = ['RID', 'GDTOTAL']
    a1 = a1[v]
    x1 = pd.merge(x1, a1, how='left', on='RID')

    # Calculating the number of missing values per subject
    k = x1.isnull().sum(axis=1).tolist()
    x1['missing'] = np.array(k) / len(x1.columns.tolist())

    # Using subjects that have all entries. Played arounf with 0.08 cutoff, but some brain scans missing for some subjects
    x2 = x1[x1.missing < 0.0001]

    # Converting
    # MCI and CN to No-AD (0) and Dementia to AD (1)

    x2['grp'] = np.where(x2.DX == "Dementia", 1, 0)

    #Interval variables
    cont = ['RAVLT_perc_forgetting_bl', 'Ventricles_bl', 'RAVLT_learning_bl', 'MMSE_bl', 'RAVLT_immediate_bl',
            'PTEDUCAT', 'MidTemp_bl', 'ADAS11_bl', 'FAQ_bl', 'ADAS13_bl', 'AGE', 'RAVLT_forgetting_bl', 'ICV', 'Entorhinal_bl',
            'WholeBrain_bl', 'Fusiform_bl', 'CDRSB_bl', 'ADNI_MEM_bl', 'ADNI_EF_bl', 'HMSCORE', 'GDTOTAL']
    #categorical variables
    cat = ['PTGENDER', 'PTMARRY', 'PTRACCAT']

    #Creatinf dummy variables
    df = pd.get_dummies(x2, prefix=cat, columns=cat, drop_first=True)

    del df['DX']
    del df['RID']
    del df['missing']

    #Splitting into training and test sets
    np.random.seed(9001)
    msk = np.random.rand(len(df)) < 0.80
    tr = df[msk]
    ts = df[~msk]
    x = df.columns.tolist()
    x.remove('grp')
    X_train = tr[x]
    X_test = ts[x]
    y_train = tr['grp']
    y_test = ts['grp']
    return X_train, y_train, X_test, y_test



#X_train, y_train, X_test, y_test = project_utils_v2.get_data()
#X_train.head()



