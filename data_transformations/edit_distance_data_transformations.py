import pandas as pd
import numpy as np
from os import path, mkdir
import json


def editDistanceWith2Ops(X, Y):
    '''
    Source: https://www.geeksforgeeks.org/edit-distance-and-lcs-longest-common-subsequence/

    Take two strings X, Y and compute the longest common substring.
    Return the number of characters deleted, added, and unchanged.
    '''

    if X is np.nan or Y is np.nan:
        return [np.nan, np.nan, np.nan]

    # Find LCS
    m = len(X)
    n = len(Y)
    L = [[0 for x in range(n + 1)]
            for y in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if (i == 0 or j == 0):
                L[i][j] = 0
            elif (X[i - 1] == Y[j - 1]):
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j],
                              L[i][j - 1])

    lcs = L[m][n]

    #        delete,    add,     unchanged
    return (m - lcs), (n - lcs), lcs


def compute_diff(a, b):
    '''
    Compute the diff between two strings a, b. This function relies on
    ndiff from the default Python library difflib. Note that the ndiff
    implementation is NOT optimal (i.e. the generated diffs are not
    guaranteed to be the mimimal set of changes needed to convert a to b).

    Returns a list of diffs, number of adds, number of deletes, and number
    of unchanged characters.

    Example:

    compute_diff("abcdefg", "xac")
    > [['ADD(x)', 'a', 'DEL(b)', 'c', 'DEL(defg)'], 1, 5, 2]
    '''

    import difflib

    if a is np.nan or b is np.nan:
        return [np.nan, np.nan, np.nan, np.nan]

    a = a.replace('\n',' ')
    b = b.replace('\n',' ')

    diff_list = []
    diff_add_count = 0
    diff_del_count = 0
    diff_unchanged_count = 0

    diff = list(difflib.ndiff(a, b, charjunk = lambda x: False))

    i = 0

    while i < len(diff):

        if diff[i][0] == ' ':
            temp_diff_str = ''

            while i < len(diff) and diff[i][0] == ' ':
                temp_diff_str += diff[i][-1]
                diff_unchanged_count += 1
                i += 1

            diff_list.append(temp_diff_str)

        if i < len(diff) and diff[i][0] == '-':
            temp_diff_str = 'DEL('

            while i < len(diff) and diff[i][0] == '-':
                temp_diff_str += diff[i][-1]
                diff_del_count += 1

                i += 1

            temp_diff_str += ')'

            diff_list.append(temp_diff_str)


        if i < len(diff) and diff[i][0] == '+':
            temp_diff_str = 'ADD('

            while i < len(diff) and diff[i][0] == '+':
                temp_diff_str += diff[i][-1]
                diff_add_count += 1

                i += 1

            temp_diff_str += ')'

            diff_list.append(temp_diff_str)

    return [diff_list, diff_add_count, diff_del_count, diff_unchanged_count]


def apply_edit_distance(m1, m2, edit_cost = 1):
    '''
    Compute the Levenshtein edit distance between m1, m2 using NLTK's
    implementation. Substitutions have a cost of edit_cost.

    https://en.wikipedia.org/wiki/Levenshtein_distance
    '''

    from nltk.metrics import edit_distance

    if m1 is np.nan or m2 is np.nan:
        return -1

    return edit_distance(m1, m2, substitution_cost=edit_cost, transpositions=False)


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


def create_messages_with_diff():

    relative_data_dir = '../data'
    messages_df = pd.read_csv(f'{relative_data_dir}/messages.csv')
    deployment = 'COGSCI21-LIVINGDOC-ITER-FR-1'
    file_path = f'{relative_data_dir}/messages_with_diff.csv'

    messages_with_diff_df = messages_df

    # Convert received_messages from a singleton list to a string
    messages_with_diff_df.received_messages = messages_with_diff_df.received_messages.apply(lambda x: json.loads(x)[0] if x is not np.nan else x)

    # Passed count of -1 means they didn't finish the study, this selects all valid messages
    messages_with_diff_df = messages_with_diff_df[messages_with_diff_df.passed_count != -1]

    messages_with_diff_df['edit_distance'] = messages_with_diff_df.apply(lambda row:
                                                                            apply_edit_distance(row['message'],
                                                                                                row['received_messages']),
                                                                         axis = 1)

    # We only care about the diff_list since it is qualitatively useful. The
    #  other values that are returned are not used since they are not optimal.
    messages_with_diff_df['diff_list'] = messages_with_diff_df.apply(lambda row:
                                                                        compute_diff(row['received_messages'],
                                                                                     row['message'])[0],
                                                                     axis = 1)

    # Compute the number of added, deleted and unchanged characters
    new_column_names = ['diff_del_count', 'diff_add_count', 'diff_unchanged_count']
    messages_with_diff_df[new_column_names] = messages_with_diff_df.apply(lambda row:
                                                                    editDistanceWith2Ops(row['received_messages'],
                                                                                        row['message']),
                                                                axis = 1,
                                                                result_type = 'expand')

    save_df_as_csv_conditional(messages_with_diff_df, file_path)

    return create_messages_with_diff


if __name__ == "__main__":
    create_messages_with_diff()
