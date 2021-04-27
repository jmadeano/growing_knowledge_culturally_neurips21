# Growing knowledge culturally across generations to solve  novel, complex tasks

This repo contains all of the code and data necessary to recreate the figures and results from the paper.



## Data

Experiment data can be found in the form of CSVs in the `data` directory. This
repository includes both raw data directly from the experiment as well as
calculated data that was generated from the raw data (e.g. split messages by
sentence, calculate edit distance between consecutive messages, etc.). All
data files are listed below. Each file is described in detail in the README
contained in the `data` directory.

### Raw data:

- `experiments_no_states.csv`: Participant gameplay data
- `messages.csv`: Participant message data
- `survey_responses.csv`: Post-experiment survey responses/metadata

### Calculated data:
- `ordered_message_history.csv`:
- `ordered_message_history_by_sentence.csv`:


- `messages_with_diff.csv`:


- `unigrams.csv`:
- `bigrams.csv`:
- `trigrams.csv`:


## Data transformation code

The calculated data tables listed above were generated using a number of
Python scripts. These scripts can be found in the `data_transformations`
directory.

- `ordered_message_history.py`:
  - `ordered_message_history.csv`
  - `ordered_message_history_by_sentence.csv`

- `edit_distance_data_transformations.py`
  - `messages_with_diff.csv`

- `ngram_data_transformations.py`
  - `unigrams.csv`
  - `bigrams.csv`
  - `trigrams.csv`


## Analysis Code

The analysis and figures for the paper were generated using R. These scripts
can be found in the `analysis` folder.
