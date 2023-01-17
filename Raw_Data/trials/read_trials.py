import pandas as pd
import numpy as np
from os import listdir

from Raw_Data.utils.utils import number_to_string
import Raw_Data.configurations as cfg
import pathes


def path_resolver(subject_num):
    path = pathes.raw_data_path + cfg.participant_dir_name + \
        number_to_string(subject_num) + f'/{cfg.experiment_name}/'
    inner_dir = [f for f in listdir(path) if f.startswith('Sub')][0]
    path += inner_dir + '/UsedPlan/'

    suffix = [f for f in listdir(path) if f.lower().startswith(cfg.trials_file_name_prefix)]
        
    path = path + '/' + suffix[0]
    
    return path




def filter_trials_file_question(df):
    # take only real trials rows
    # filter by question
    df = df[df[cfg.trial_question_col_name] == cfg.relevant_question_trials]
    
    
    # take only id and relevant columns
    df = df[[cfg.trial_index] + cfg.trial_relevant_cols]
    
    return df
    
def label_trials_file_one_column(df, col_id, tranfrom_dic=cfg.trial_labels_dic):
    df.iloc[:,col_id].replace(tranfrom_dic, inplace=True)
    return df

def label_trials_file(df, col_id, tranfrom_dic=cfg.trial_labels_dic):
    trial_cfg = df.iloc[:,col_id: col_id + len(cfg.trial_relevant_cols)]
    trial_cfg  = [tuple(x.to_list()) for _, x in trial_cfg.iterrows()]
    trial_labels = [tranfrom_dic[x] for x in trial_cfg]
    df.iloc[:, col_id] = trial_labels 
    df = df.iloc[:, [0, col_id]]

    trial_col_name = df.columns[col_id]
    df.rename(columns={trial_col_name:cfg.trial_condition_col_name}, inplace=True)

    return df


def read_trials(subject_num):
    # resolve path of trials file
    path = path_resolver(subject_num)
    
    # read trials data
    data = pd.read_csv(path)
    
    # filter trials data
    data = filter_trials_file_question(data)
    
    # label trials in organize manner (by dictionary)
    data = label_trials_file(data, col_id=1)
    
    # reset index
    data.reset_index(inplace=True, drop=True)

    return data