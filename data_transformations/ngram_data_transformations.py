import pandas as pd
import numpy as np
from os import path, mkdir
import spacy
from nltk.util import ngrams
from nltk.lm import NgramCounter
from ordered_message_history import create_ordered_message_history_by_sentence
nlp = spacy.load("en_core_web_sm")

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

def create_ngrams_list(string, n = 1, remove_stop_tokens = False, lemmatize = True, as_str = False):

    doc = nlp(string)

    if len(doc) < n:
        return np.nan

#     if remove_stop_tokens:
#         doc = [token for token in doc if not token.is_stop]

    if lemmatize:
        doc = [token.lemma_.lower() for token in doc]
    else:
        doc = [token.text for token in doc]

    if as_str:
        return [' '.join(gram) for gram in ngrams(doc, n)]

    return list(ngrams(doc, n))


def create_unigrams():
    relative_data_dir = '../data'
    by_sentence_file_path = f'{relative_data_dir}/ordered_message_history_by_sentence.csv'

    if path.exists(by_sentence_file_path):
        unigram_df = pd.read_csv(by_sentence_file_path)
    else:
        unigram_df = create_ordered_message_history_by_sentence()

    def add_nlp_info(string):
        return [[token.text, token.lemma_.lower(), token.pos_, token.is_stop] for token in nlp(string)]

    unigram_df['temp_nlp'] = unigram_df.sentence.apply(add_nlp_info)
    unigram_df = unigram_df.explode('temp_nlp').reset_index(drop = True)
    unigram_df['token_number'] = unigram_df.groupby(sorting_columns + ['message', 'sentence_is_duplicate', 'sentence', 'sentence_number']).cumcount()
    unigram_df[['original_token', 'lemmatized_1gram', 'POS', 'is_stopword']] = unigram_df.temp_nlp.apply(pd.Series)
    unigram_df = unigram_df.drop(columns = ['temp_nlp'])

    file_path = 'unigrams.csv'
    save_df_as_csv_conditional(unigram_df, file_path)

    return unigram_df


def create_ngrams(n, output_filename):
    relative_data_dir = '../data'
    by_sentence_file_path = f'{relative_data_dir}/ordered_message_history_by_sentence.csv'

    if path.exists(by_sentence_file_path):
        ngram_df = pd.read_csv(by_sentence_file_path)
    else:
        ngram_df = create_ordered_message_history_by_sentence()


    def add_nlp_info(string):
        ngram_lemmatized = []
        ngram_pos = []
        ngram_is_stop = []

        if string is np.nan:
            return [np.nan, np.nan, np.nan]

        for token in nlp(string):

            ngram_lemmatized.append(token.lemma_.lower())
            ngram_pos.append(token.pos_)
            ngram_is_stop.append(token.is_stop)

        return [' '.join(ngram_lemmatized), ' '.join(ngram_pos), any(ngram_is_stop)]


    sorting_columns = ['chain', 'generation', 'game_number', 'game_name']

    ngram_df['ngram_raw'] = ngram_df.sentence.apply(lambda x: create_ngrams_list(x, n = n, remove_stop_tokens = False, lemmatize = False, as_str = True))
    ngram_df = ngram_df.explode('ngram_raw').reset_index(drop = True)
    ngram_df['ngram_number'] = ngram_df.groupby(sorting_columns + ['message', 'sentence_is_duplicate', 'sentence', 'sentence_number']).cumcount()


    new_column_names = ['ngram_lemmatized', 'ngram_pos', 'contains_stopword']
    ngram_df[new_column_names] = ngram_df.apply(lambda row:
                                                        add_nlp_info(row['ngram_raw']),
                                                        axis = 1,
                                                        result_type = 'expand')


    save_df_as_csv_conditional(ngram_df, f'{relative_data_dir}/{output_filename}')

    return ngram_df


if __name__ == "__main__":
    create_ngrams(1, 'unigrams.csv')
    create_ngrams(2, 'bigrams.csv')
    create_ngrams(3, 'trigrams.csv')
