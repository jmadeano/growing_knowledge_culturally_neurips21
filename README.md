# [Learning to solve complex tasks by growing knowledge culturally across generations](https://arxiv.org/abs/2107.13377)

This repo contains all of the code and data necessary to recreate the figures and results from [the paper](https://arxiv.org/abs/2107.13377).

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

- `ordered_message_history.csv`: Ordered summary of all participant messages
- `ordered_message_history_by_sentence.csv`: Ordered summary of all participant messages broken into sentences/utterances
- `all_sentences_tagged_9-15.csv`: Human and GPT3 sentence tagging data

- `messages_with_diff.csv`:

- `unigrams.csv`
- `bigrams.csv`
- `trigrams.csv`

## Data transformation code

The calculated data tables listed above were generated using a number of
Python scripts. These scripts can be found in the `data_transformations`
directory.

_NOTE:_ At this time, the code used to perform language coding/classification with GPT3 is not available. Check out [Elicit](https://elicit.org/) to learn more about the process and implement your own classification workflows.

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

The analysis and figures for the paper were generated using R (see `analysis.Rmd` for the code).
You will likely need to modify `path_to_repo_folder` and `project.path` variables at line ~35 to point to
the location of the git repository on your system.
