import pandas as pd
import numpy as np
from os import path, mkdir


def save_df_as_csv_conditional(df, file_path, index = False):
    '''
    Save df as a csv if the specified file_path/name does not already exist. Otherwise,
    ask the user whether to overwrite the existing file.
    '''

    file_exists = path.exists(file_path)

    if file_exists:
        confirmed = input(f"Type 'Y' to confirm that you want to overwrite '{file_path}': ")
        if confirmed == 'Y':
            print('CONFIRMED!\n')
            df.to_csv(file_path, index = index)
            print(f"Successfully wrote to {file_path}")
    else:
        df.to_csv(file_path, index = index)
        print(f"Successfully wrote to {file_path}")



def create_ordered_message_history():
    '''
    Create a dataframe where ...
    '''
    relative_data_dir = '../data'
    messages_df = pd.read_csv(f'{relative_data_dir}/messages.csv')
    deployment = 'COGSCI21-LIVINGDOC-ITER-FR-1'
    file_path = f'{relative_data_dir}/ordered_message_history.csv'

    full_hist = messages_df['deployment'] == deployment
    passed_count = messages_df['passed_count'] != -1

    ordered_message_history = messages_df[full_hist & passed_count].copy()
    ordered_message_history.game_number = pd.to_numeric(ordered_message_history.game_number)
    ordered_message_history.message = ordered_message_history.message.apply(lambda x: [x])
    ordered_message_history = ordered_message_history.sort_values(['deployment', 'chain', 'generation', 'exp_id', 'game_number', ])
    ordered_message_history = ordered_message_history.groupby(['deployment', 'chain','game_number','game_name'])[['message']].sum().reset_index()

    save_df_as_csv_conditional(ordered_message_history, file_path)

    return ordered_message_history



def create_ordered_message_history_by_sentence():
    '''
    Create a dataframe where each line represents a sentence from a particular message.
    (Uses NLTK to break down the messages into component sentences.)
    '''
    from nltk.tokenize import sent_tokenize

    relative_data_dir = '../data'
    messages_df = pd.read_csv(f'{relative_data_dir}/messages.csv')
    deployment = 'COGSCI21-LIVINGDOC-ITER-FR-1'
    file_path = f'{relative_data_dir}/ordered_message_history_by_sentence.csv'


    sorting_columns = ['deployment', 'chain', 'generation', 'exp_id', 'game_number', 'game_name']

    full_hist = messages_df['deployment'] == deployment
    passed_count = messages_df['passed_count'] != -1

    ordered_message_history_by_sentence = messages_df[full_hist & passed_count].copy()
    ordered_message_history_by_sentence = ordered_message_history_by_sentence.sort_values(sorting_columns)

    ordered_message_history_by_sentence['sentence'] = ordered_message_history_by_sentence.message.apply(sent_tokenize)
    ordered_message_history_by_sentence = ordered_message_history_by_sentence.explode('sentence')[sorting_columns + ['message', 'edit_distance', 'sentence']]
    ordered_message_history_by_sentence['sentence_number'] = ordered_message_history_by_sentence.groupby(sorting_columns + ['message', 'edit_distance']).cumcount()

    duplicated_sentence_columns = ['chain',
                               'game_number',
                               'game_name',
                               'sentence']

    ordered_message_history_by_sentence['sentence_is_duplicate'] = ordered_message_history_by_sentence.duplicated(duplicated_sentence_columns, 'first')



    save_df_as_csv_conditional(ordered_message_history_by_sentence, file_path)

    return ordered_message_history_by_sentence


if __name__ == "__main__":
    create_ordered_message_history()
    create_ordered_message_history_by_sentence()
