## Raw data

### Gameplay data

`experiments_no_states.csv`

Note each row represents one level of gameplay on one game, ending either in a win or a loss.

- **deployment** text not null
  - a name for the current deployment (often TESTING, pilot, ITER-pilot, etc.)
- **exp_id** text not null
  - a unique id for a particular participant
- **val_id** text not null
  - another unique id for a particular participant
- **chain** text not null
  - a unique id for a particular chain within the experiment
- **game_name** text not null
  - the name of the game
- **game_number** integer not null
  - the game number (i.e. trial number)
- **desc_number** integer not null
  - the index of the vgdl description for this level
- **total_levels** integer not null
  - the 0-indexed total number of levels within a particular game
- **level_number** integer not null
  - the 0-indexed level currently being played
- **round_number** integer not null
  - a 0-indexed counter for the life number (1 => the participant is on their second life)
- **score** numeric not null
  - the current score (as of frame _frame_number_)
- **win** text not null
  the current state of the game -- '' if still playing, otherwise one of the following end conditions: 'win', 'lose', 'skip', 'refresh'
- **frame_number** integer not null
  - the current game frame Number at the time of data submission
- **start_time** text not null
  - the time (in ISO?) when the start button was pressed
- **time_playing** text not null
  - number of milliseconds since start button was pressed
- **game_end_time_bonus** numeric
  - count of negative events that occured (EXPERIMENTAL -- not fully implemented yet)
- **data** text not null
  - a json parsable object with extra metadata
    - retry_delay: amount of time before retry/give up message/button appears to participants for a given level
    - forfeit_delay: amount of time before forfeit message/button appears to participants for a given level
    - steps: a counter for the number of steps (as of frame _frame_number_)
    - index: the index of the current data submission for this level (i.e. how many posts have been made to the db for this level so far)
- **states** text not null
  - a json parsable list of objects where each object stores information about an individual frame of the current level
    - frame: the frame number
    - score: the current score (as of frame _frame_number_)
    - bonus*score: the current score with bonuses calculated by VGDL (as of frame \_frame_number*) - bonuses are generally applied at the end of a game, so this will generally be equivalent to **score** except for time-based games
    - ended: a boolean representing whether the game has ended
    - win: a boolean representing whether the game has been one, null if ended == false
    - objects: a json object representing the current state of the gameboard (all sprites and their locations) -- generated using `game.getFullState(...)` and can be used to create a video replay of the level using `setFullState(...)`
    - killed: any sprites that were killed this frame (e.g. `{"lime":{"86":{"x":204,"y":170}}`)
    - actions: any actions taken this frame
    - events: a list of events/interactions that occurred this frame. An event consists of a vgdl interaction type, sprite number and sprite number -- sprite numbers can be found in objects (e.g. `[["transforrmTo",49,58],["nothing",87,58],["nothing",58,87]]`)
    - real_time: time since game start (in milliseconds?)
- **missing_frames** boolean not null
  - whether the row has any corrupted/missing frames
- **events_involving_avatar** text[] not null
  - list of event triples that occured in the form ["eventName", "sprite1", "sprite2"], where either "sprite1" or "sprite2" equals "avatar"
- **negative** numeric
  - count of negative events that occured (EXPERIMENTAL -- not fully implemented yet)
- **intrumental** numeric
  - count of instrumental events that occured (EXPERIMENTAL -- not fully implemented yet)
- **neutral** numeric
  - count of neutral events that occured (EXPERIMENTAL -- not fully implemented yet)
- **positive** numeric
  - count of positive events that occured (EXPERIMENTAL -- not fully implemented yet)
- **lookup** numeric
  - count of unlabeled events that occured (EXPERIMENTAL -- not fully implemented yet)

**Note:** This repo does not include the states column due to file size limitations and because it was not used in any of the analyses within the paper. Please reach out to the authors if you are interested in this data.

### Message data

`messages.csv`

- **deployment** text not null
  - a name for the current deployment (often TESTING, pilot, ITER-pilot, etc.)
- **exp_id** text not null
  - a unique id for a particular participant
- **val_id** text not null
  - another unique id for a particular participant
- **game_name** text not null
  - the name of the game
- **game_number** integer not null
  - the game number (i.e. trial number)
- **message** text not null
  - the message written by the participant _exp_id_
- **passed_count** integer not null
  - the number of times the message has be passed to another player
- **chain** text not null
  - a unique id for a particular chain within the experiment
- **generation** integer not null
  - the 0-indexed generation of the participant _exp_id_
- **received_message** text,
  - a singleton list of messages received by the player prior to playing the name -- null if generation == 0
- **received_from_id** text

  - the exp_id of the player who wrote the message this player received -- null if generation == 0

  ### Tagged Message Data

` all_sentences_tagged_9-15.csv`

'deployment', 'chain', 'generation', 'exp_id', 'game_number',
'game_name', 'message', 'edit_distance', 'sentence', 'sentence_number',
'dynamics_elicit_label', 'dynamics_elicit_confidence',
'dynamics_human_label', 'dynamics_elicit_aboveThreshold', 'P(dynamics)',
'P(notDynamics)', 'policy_elicit_label', 'policy_elicit_confidence',
'policy_human_label', 'policy_elicit_aboveThreshold', 'P(policy)',
'P(notPolicy)', 'abstract_elicit_label', 'abstract_elicit_confidence',
'abstract_human_label', 'abstract_elicit_aboveThreshold', 'P(abstract)',
'P(concrete)', 'P(ignorance)', 'valence_elicit_label',
'valence_elicit_confidence', 'valence_human_label',
'valence_elicit_aboveThreshold', 'P(neutral)', 'P(lose)', 'P(win)',
'count_tagAboveThreshold', 'dynamics_elicitMatchesHuman',
'policy_elicitMatchesHuman', 'abstract_elicitMatchesHuman',
'valence_elicitMatchesHuman'

### Post-experiment survey data (anonymized)

`survey_responses.csv`

- **deployment** text not null
  - a name for the current deployment (often TESTING, pilot, ITER-pilot, etc.)
- **exp_id** text not null
  - a unique id for a particular participant
- **val_id** text not null
  - another unique id for a particular participant
- **understand** text
  - Survey: did the participant understand the instructions/experiment -- null if the participant did not finish the study or did not answer this question
- **age** numeric
  - Survey: age of the participant -- null if the participant did not finish the study or did not answer this question
- **sex** text
  - Survey: sex/gender of the participant -- null if the participant did not finish the study or did not answer this question
- **education** text
  - Survey: education level of the participant -- null if the participant did not finish the study or did not answer this question
- **languages** text
  - Survey: native language(s) of the participant -- null if the participant did not finish the study or did not answer this question
- **enjoyment** text
  - Survey: did the participant enjoy the experiment (0 = worse than average, 1 = average, 2 = better) -- null if the participant did not finish the study or did not answer this question
- **problems** text
  - Survey: did the participant note any problems with the experiment -- null if the participant did not finish the study or did not answer this question
- **fairprice** money
  - Survey: what did the participant think was a fair price for the study -- null if the participant did not finish the study or did not answer this question
- **comments** text
  - Survey: additional comments -- null if the participant did not finish the study or did not answer this question
- **previous_experience** text
  - Survey: did the participant have previous experience with these games -- null if the participant did not finish the study or did not answer this question
- **received_from_id** text
  - the exp_id of the previous participant in this chain (i.e. generation - 1) -- null if generation == 0
- **generation** integer not null
  - the 0-indexed generation of the participant _exp_id_
- **game_order** text []
  - a list specifying the order the games were played in -- null if the participant did not finish the experiment
- **game_scores** numeric []
  - a list specifying the players score for each of the games (order the same as game_order) -- null if the participant did not finish the experiment
- **passed_count** integer not null
  - the number of times a VALID (does not count participants who didn't complete the experiment or were otherwise disqualified) chain has been continued from this participant
- **chain** text not null
  - a unique chain id (generally the exp_id of the first participant in the chain)
- **dead_end** text
  - reason for disqualifying the participant -- null if the participant should not be disqualified

## Calculated Data

### Messages with Diff

Computed using: `edit_distance_data_transformations.py`

Resulting data: `messages_with_diff.csv`

A modified message table with additional computed statistics on edit distance/text changes between received messages and written messages.

**_Same as raw data:_**

[__deployment__, __exp_id__, __val_id__, __game_name__, __game_number__, __message__, __passed_count__, __chain__, __generation__, __received_messages__, __received_from_id__]

**_New/Updated fields:_**

- **edit_distance**: the Levenshtein Distance between received message and written message
- **diff_list**: a list of strings composed of a primitive str and two functions ADD(.) and DEL(.). The functions are represented as strings with a prefix based on the function name (i.e. 'ADD(' or 'DEL(') and an opened parenthesis and a suffix of a closed parenthesis. We do not define a notion of recursion, so there are no nested functions. _THIS LIST IS NOT OPTIMAL AND DOES NOT REFLECT THE SAME CHANGES AS **diff_del_count** AND **diff_add_count**._
- **diff_del_count**: the minimal number of characters that need to be removed to the received message in order transform to the new written message
- **diff_add_count**: the minimal number of characters that need to be added to the received message in order transform to the new written message
- **diff_unchanged_count**: the number of characters that are unchanged between the received message and new written message

### Ordered Message History

Computed using: `ordered_message_history.py`

Resulting data: `ordered_message_history.csv`

A table with `n_chains`\*`n_games` rows (e.g. 10\*10 = 100 rows). Each row represents a unique chain-row pair and the table is ordered by [__deployment__, __chain__, __game_number__].

**_Same as raw data:_**

[__deployment__, __chain__, __game_number__, __game_name__]

**_New/Updated fields:_**

- **message**: A list of strings where the i-th string represents the message written by the i-th generation of the particular chain for the particular game

### Ordered Message History by Sentence

Computed using: `ordered_message_history.py`

Resulting data: `ordered_message_history_by_sentence.csv`

An expansion of `messages.csv` where each row represents a sentence rather than an entire written message. Sentence parsing is done using `sent_tokenize` (from `nltk.tokenize`). By default, the table is sorted by [__deployment__, __chain__, __generation__, __game_number__, __sentence_number__].

**_Same as raw data:_**

[__deployment__, __chain__, __generation__, __exp_id__, __game_number__, __game_name__, __message__]

**_New/Updated fields:_**

- **edit_distance**: the Levenshtein Distance between received message and written message
- **sentence**: A component sentence of **message** (as parsed by `nltk`)
- **sentence_number**: The index of the sentence within the message
- **sentence_is_duplicate**: FALSE if this is the first time the sentence occurs (first based on the ordering described above), otherwise TRUE

### All Sentences Tagged

An expansion of `ordered_message_history_by_sentence.csv` where each row represents a sentence rather than an entire written message. Sentence parsing is done using `sent_tokenize` (from `nltk.tokenize`). Each sentence is tagged (either by humans or GPT3) as containing some combination of dynamics, policy, valence, and abstractness -- see the paper for more information on this coding scheme. By default, the table is sorted by [__deployment__, __chain__, __generation__, __game_number__, __sentence_number__].

**_Same as original data:_**
[__deployment__, __chain__, __generation__, __exp_id__, __game_number__, __game_name__, __message__, __edit_distance__, __sentence__, __sentence_number__]

**_New/Updated fields:_**

- **dynamics_elicit_label**: GPT3's prediction of the dynamics label
  - 'dynamics, or how the world works including explanations or affordances'
  - 'not dynamics, or how the world works including explanations or affordances'
- **dynamics_elicit_confidence**: Confidence/probability of GPT3's dynamics label prediction
- **dynamics_human_label**: Human-coded dynamics label (if part of the training/validation set, otherwise null)
- **dynamics_elicit_aboveThreshold**: boolean denoted whether the confidence for dynamics is above the threshold
- **P(dynamics)**: GPT3's confidence/probability that the sentence contains dynamics information
- **P(notDynamics)**: GPT3's confidence/probability that the sentence DOES NOT contains dynamics information

- **policy_elicit_label**: GPT3's prediction of the policy label
  - 'policy, or what actions to take including strategies or instructions'
  - 'not policy, or what actions to take including strategies or instructions'
- **policy_elicit_confidence**: Confidence/probability of GPT3's policy label prediction
- **policy_human_label**: Human-coded policy label (if part of the training/validation set, otherwise null)
- **dynamics_policy_aboveThreshold**: boolean denoted whether the confidence for policy is above the threshold
- **P(policy)**: GPT3's confidence/probability that the sentence contains policy information
- **P(notPolicy)**: GPT3's confidence/probability that the sentence DOES NOT contains policy information

- **abstract_elicit_label**: GPT3's prediction of the abstract label
  - abstract, complex, high-level information
  - concrete, simple, low-level information
  - ignorance statements or specific experiences
- **abstract_elicit_confidence**: Confidence/probability of GPT3's abstract label prediction
- **abstract_human_label**: Human-coded abstract label (if part of the training/validation set, otherwise null)
- **abstract_elicit_aboveThreshold**: boolean denoted whether the confidence for abstract is above the threshold
- **P(abstract)**: GPT3's confidence/probability that the sentence contains abstract information
- **P(concrete)**: GPT3's confidence/probability that the sentence contains concrete information
- **P(ignorance)**: GPT3's confidence/probability that the sentence contains ignorance/experience information

- **valence_elicit_label**: GPT3's prediction of the valence label
  - winning, including mentions of scoring points, victory, success, goals, solutions, best strategies
  - losing, including information about death, losing points, lowering scores, forfeiting, losing lives, getting stuck or trapped
  - neutral information
- **valence_elicit_confidence**: Confidence/probability of GPT3's valence label prediction
- **valence_human_label**: Human-coded valence label (if part of the training/validation set, otherwise null)
- **P(neutral)**: GPT3's confidence/probability that the sentence DOES NOT contains valence information
- **P(lose)**: GPT3's confidence/probability that the sentence contains positive valence information
- **P(win)**: GPT3's confidence/probability that the sentence contains negative valence information

- **count_tagAboveThreshold**: Number of tags for the sentence that had a confidence above their threshold
- **dynamics_elicitMatchesHuman**: boolean denoting whether GPT3's dynamics prediction matches human coding (if part of the training/validation set, otherwise null)
- **policy_elicitMatchesHuman**: boolean denoting whether GPT3's policy prediction matches human coding (if part of the training/validation set, otherwise null)
- **abstract_elicitMatchesHuman**: boolean denoting whether GPT3's abstract prediction matches human coding (if part of the training/validation set, otherwise null)
- **valence_elicitMatchesHuman**: boolean denoting whether GPT3's valence prediction matches human coding (if part of the training/validation set, otherwise null)

### Ngrams

Computed using: `ngram_data_transformations.py`

Resulting data: `unigrams.csv`, `bigrams.csv`, `trigrams.csv`

An expansion of `messages.csv` where each row represents an ngram within a particular sentence of a particular message rather than an entire written message. Sentence parsing is done using `sent_tokenize` (from `nltk.tokenize`) and tokenization/lemmatization/POS relies on `spacy`. By default, the table is sorted by [__deployment__, __chain__, __generation__, __game_number__, __sentence\_number__, __ngram\_number__].

**_Same as raw data:_**

[__deployment__, __chain__, __generation__, __exp\_id__, __game\_number__, __game\_name__, __message__]

**_New/Updated fields:_**

- **edit_distance**: the Levenshtein Distance between received message and written message
- **sentence**: A component sentence of **message** (as parsed by `nltk`)
- **sentence_number**: The index of the sentence within the message
- **sentence_is_duplicate**: FALSE if this is the first time the sentence occurs (first based on the ordering described above), otherwise TRUE
- **ngram_raw**: the raw tokens of the ngram separated by space (' ') if n > 1
- **ngram_number**: the index of the ngram within the sentence
- **ngram_lemmatized**: the lemmatized tokens of the ngram separated by space (' ') if n > 1
- **ngram_pos**: the part of speech tag of each token in the ngram separated by space (' ') if n > 1
- **contains_stopword**: TRUE if any of the tokens in the ngram are considered stop words, otherwise FALSE

**_Note:_** Different counts of ngrams (e.g. `unigrams.csv`, `bigrams.csv`, `trigrams.csv`) all have the same fields, and **ngram_raw**, **ngram_lemmatized**, **ngram_pos** are always strings. However, in ngrams where n > 1, we separate tokens with single spaces. For example, consider the sentence "Touch the blue square". The first unigram and bigram are shown below:

#### Unigrams

- **ngram_raw**: "Touch"
- **ngram_number**: 0
- **ngram_lemmatized**: "touch"
- **ngram_pos**: "VERB"
- **contains_stopword**: FALSE

#### Bigrams

- **ngram_raw**: "Touch the"
- **ngram_number**: 0
- **ngram_lemmatized**: "touch the"
- **ngram_pos**: "VERB DET"
- **contains_stopword**: TRUE
