from functools import reduce

import pandas as pd
import numpy as np
import os

from Raw_Data.utils.utils import number_to_string
import Raw_Data.configurations as cfg
import pathes


def path_resolver(subject_num):
    path = pathes.raw_data_path + cfg.participant_dir_name + \
           number_to_string(subject_num) + f'/{cfg.experiment_name}/'
    inner_dir = [f for f in os.listdir(path) if f.startswith('Sub')][0]
    path += inner_dir + '/'
    filename = [x for x in os.listdir(path) if x.lower().startswith(cfg.answers_file_name)][0]
    path += filename
    return path


def filter_answer_file_question(df):
    # take only real trials rows
    # filter by question
    df = df[df[cfg.answer_question_col_name].isin(cfg.relevant_questions_answers)]

    # take only id and relevant columns
    df = df[[cfg.answers_index] + cfg.answer_relevant_cols]

    return df


def label_answer_file_one_columns(df, col_id, transform_dic=cfg.trial_labels_dic):
    df.iloc[:, col_id].replace(transform_dic, inplace=True)
    return df


def aggregate_answers(df):
    answers_df_list = []

    for i, relevant_question in enumerate(cfg.relevant_questions_answers):
        one_question_df = df[df[cfg.answer_question_col_name] == relevant_question]
        one_question_df.rename(columns={cfg.answer_col_name: cfg.relevant_questions_answers_names[i]}, inplace=True)
        one_question_df.drop(cfg.answer_question_col_name, axis=1, inplace=True)
        answers_df_list.append(one_question_df)

    aggregated_answers_df = reduce(lambda left, right: pd.merge(left, right, on=cfg.answers_index,
                                                                how='inner'), answers_df_list)

    return aggregated_answers_df


def read_answers(subject_num):
    # resolve path of trials file
    path = path_resolver(subject_num)

    # read trials data
    data = pd.read_csv(path)

    # filter trials data
    data = filter_answer_file_question(data)

    if len(cfg.relevant_questions_answers) > 1:
        data = aggregate_answers(data)

    # reset index
    data.reset_index(inplace=True, drop=True)

    # no need for labeling in the moment 
    # data = label_trials_file_one_columns(data, col_id=1)

    return data
