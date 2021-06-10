## Raw data

### Gameplay data
`experiments_no_states.csv`

- __deployment__						text			not null
	- a name for the current deployment (often TESTING, pilot, ITER-pilot, etc.)
- __exp_id__								text 			not null
	- a unique id for a particular participant
- __val_id__  							text    	not null
	- another unique id for a particular participant
- __chain__                text       not null
  - a unique id for a particular chain within the experiment
- __game_name__							text			not null
	- the name of the game
- __game_number__						integer		not null
	- the game number (i.e. trial number)
- __desc_number__						integer		not null
	- the index of the vgdl description for this level
- __total_levels__					integer		not null
	- the 0-indexed total number of levels within a particular game
- __level_number__					integer		not null
	- the 0-indexed level currently being played
- __round_number__					integer		not null
	- a 0-indexed counter for the life number (1 => the participant is on their second life)
- __score__									numeric		not null
	- the current score (as of frame _frame_number_)
- __win__										text			not null
	the current state of the game -- '' if still playing, otherwise one of the following end conditions: 'win', 'lose', 'skip', 'refresh'
- __frame_number__					integer		not null
	- the current game frame Number at the time of data submission
- __start_time__						text			not null
	- the time (in ISO?) when the start button was pressed
- __time_playing__					text			not null
	- number of milliseconds since start button was pressed
- __game_end_time_bonus__		numeric
	- the time bonus for the current game -- iff win != '', else null
- __data__ 									text			not null
	- a json parsable object with extra metadata
		- retry_delay: amount of time before retry/give up message/button appears to participants for a given level
		- forfeit_delay: amount of time before forfeit message/button appears to participants for a given level
		- steps: a counter for the number of steps (as of frame _frame_number_)
		- index: the index of the current data submission for this level (i.e. how many posts have been made to the db for this level so far)
- __states__ 								text			not null
	- a json parsable list of objects where each object stores information about an individual frame of the current level
		- frame: the frame number
		- score: the current score (as of frame _frame_number_)
		- bonus_score: the current score with bonuses calculated by VGDL (as of frame _frame_number_) - bonuses are generally applied at the end of a game, so this will generally be equivalent to __score__ except for time-based games
		- ended: a boolean representing whether the game has ended
		- win: a boolean representing whether the game has been one, null if ended == false
		- objects: a json object representing the current state of the gameboard (all sprites and their locations) -- generated using `game.getFullState(...)` and can be used to create a video replay of the level using `setFullState(...)`
		- killed: any sprites that were killed this frame (e.g. `{"lime":{"86":{"x":204,"y":170}}`)
		- actions: any actions taken this frame
		- events: a list of events/interactions that occurred this frame. An event consists of a vgdl interaction type, sprite number and sprite number -- sprite numbers can be found in objects (e.g. `[["transforrmTo",49,58],["nothing",87,58],["nothing",58,87]]`)
		- real_time: time since game start (in milliseconds?)

__Note:__ This repo does not include the states column due to file size limitations and because it was not used in any of the analyses within the paper. Please reach out to the authors if you are interested in this data.  

### Message data
`messages.csv`

- __deployment__						text			not null
	- a name for the current deployment (often TESTING, pilot, ITER-pilot, etc.)
- __exp_id__								text 			not null
	- a unique id for a particular participant
- __val_id__  							text    	not null
	- another unique id for a particular participant
- __game_name__							text			not null
	- the name of the game
- __game_number__						integer		not null
	- the game number (i.e. trial number)
- __message__						text		not null
	- the message written by the participant _exp_id_
- __passed_count__			integer	not null
	- the number of times the message has be passed to another player
- __chain__                text       not null
  - a unique id for a particular chain within the experiment
- __generation__				integer	not null
	- the 0-indexed generation of the participant _exp_id_
- __received_message__ 	text,
	- a singleton list of messages received by the player prior to playing the name -- null if generation == 0
- __received_from_id__ 	text
	- the exp_id of the player who wrote the message this player received -- null if generation == 0


### Post-experiment survey data (anonymized)
`survey_responses.csv`

- __deployment__						text			not null
	- a name for the current deployment (often TESTING, pilot, ITER-pilot, etc.)
- __exp_id__								text 			not null
	- a unique id for a particular participant
- __val_id__  							text    	not null
	- another unique id for a particular participant
- __understand__						text
	- Survey: did the participant understand the instructions/experiment -- null if the participant did not finish the study or did not answer this question
- __age__										numeric
	- Survey: age of the participant -- null if the participant did not finish the study or did not answer this question
- __sex__										text
	- Survey: sex/gender of the participant --  null if the participant did not finish the study or did not answer this question
- __education__							text
	- Survey: education level of the participant -- null if the participant did not finish the study or did not answer this question
- __languages__							text
	- Survey: native language(s) of the participant -- null if the participant did not finish the study or did not answer this question
- __enjoyment__							text
	- Survey: did the participant enjoy the experiment (0 = worse than average, 1 = average, 2 = better) -- null if the participant did not finish the study or did not answer this question
- __problems__							text
	- Survey: did the participant note any problems with the experiment -- null if the participant did not finish the study or did not answer this question
- __fairprice__							money
	- Survey: what did the participant think was a fair price for the study -- null if the participant did not finish the study or did not answer this question
- __comments__							text
	- Survey: additional comments -- null if the participant did not finish the study or did not answer this question
- __previous_experience__							text
	- Survey: did the participant have previous experience with these games -- null if the participant did not finish the study or did not answer this question
- __received_from_id__ 	text
	- the exp_id of the previous participant in this chain (i.e. generation - 1) -- null if generation == 0
- __generation__				integer	not null
	- the 0-indexed generation of the participant _exp_id_
- __game_order__						text []
	- a list specifying the order the games were played in -- null if the participant did not finish the experiment
- __game_scores__						numeric []
	- a list specifying the players score for each of the games (order the same as game_order) -- null if the participant did not finish the experiment
- __passed_count__			integer	not null
	- the number of times a VALID (does not count participants who didn't complete the experiment or were otherwise disqualified) chain has been continued from this participant
- __chain__ 						text not null
	- a unique chain id (generally the exp_id of the first participant in the chain)
- __dead_end__					text
	- reason for disqualifying the participant -- null if the participant should not be disqualified

## Calculated Data

### Messages with Diff

Computed using: `edit_distance_data_transformations.py`

Resulting data: `messages_with_diff.csv`


A modified message table with additional computed statistics on edit distance/text changes between received messages and written messages.

___Same as raw data:___

[__deployment__, __exp_id__, __val_id__,	__game_name__,	__game_number__,	__message__, __passed_count__, __chain__, __generation__,	__received_messages__, __received_from_id__]

___New/Updated fields:___

- __edit_distance__: the Levenshtein Distance between received message and written message
- __diff_list__: a list of strings composed of a primitive str and two functions ADD(.) and DEL(.). The functions are represented as strings with a prefix based on the function name (i.e. 'ADD(' or 'DEL(') and an opened parenthesis and a suffix of a closed parenthesis. We do not define a notion of recursion, so there are no nested functions. _THIS LIST IS NOT OPTIMAL AND DOES NOT REFLECT THE SAME CHANGES AS __diff_del_count__ AND __diff_add_count__._
-	__diff_del_count__: the minimal number of characters that need to be removed to the received message in order transform to the new written message
-	__diff_add_count__: the minimal number of characters that need to be added to the received message in order transform to the new written message
- __diff_unchanged_count__: the number of characters that are unchanged between the received message and new written message


### Ordered Message History
Computed using: `ordered_message_history.py`

Resulting data: `ordered_message_history.csv`

A table with `n_chains`\*`n_games` rows (e.g. 10\*10 = 100 rows). Each row represents a unique chain-row pair and the table is ordered by [__deployment__, __chain__, __game_number__].


___Same as raw data:___

[__deployment__, __chain__, __game_number__, __game_name__]

___New/Updated fields:___

- __message__: A list of strings where the i-th string represents the message written by the  i-th generation of the particular chain for the particular game


### Ordered Message History by Sentence
Computed using: `ordered_message_history.py`

Resulting data: `ordered_message_history_by_sentence.csv`

An expansion of `messages.csv` where each row represents a sentence rather than an entire written message. Sentence parsing is done using `sent_tokenize` (from `nltk.tokenize`). By default, the table is sorted by [__deployment__, __chain__, __generation__, __game_number__, __sentence_number__].


___Same as raw data:___

[__deployment__, __chain__, __generation__, __exp_id__, __game_number__, __game_name__, __message__]

___New/Updated fields:___

- __edit_distance__: the Levenshtein Distance between received message and written message
- __sentence__: A component sentence of __message__ (as parsed by `nltk`)
- __sentence_number__: The index of the sentence within the message
- __sentence\_is\_duplicate__: FALSE if this is the first time the sentence occurs (first based on the ordering described above), otherwise TRUE



### Ngrams
Computed using: `ngram_data_transformations.py`

Resulting data: `unigrams.csv`, `bigrams.csv`, `trigrams.csv`

An expansion of `messages.csv` where each row represents an ngram within a particular sentence of a particular message rather than an entire written message. Sentence parsing is done using `sent_tokenize` (from `nltk.tokenize`) and tokenization/lemmatization/POS relies on `spacy`. By default, the table is sorted by [__deployment__, __chain__, __generation__, __game_number__, __sentence\_number__, __ngram\_number__].

___Same as raw data:___

[__deployment__, __chain__, __generation__, __exp\_id__, __game\_number__, __game\_name__, __message__]


___New/Updated fields:___

- __edit\_distance__: the Levenshtein Distance between received message and written message
- __sentence__: A component sentence of __message__ (as parsed by `nltk`)
- __sentence\_number__: The index of the sentence within the message
- __sentence\_is\_duplicate__: FALSE if this is the first time the sentence occurs (first based on the ordering described above), otherwise TRUE
- __ngram\_raw__: the raw tokens of the ngram separated by space (' ') if n > 1
- __ngram\_number__: the index of the ngram within the sentence
- __ngram\_lemmatized__: the lemmatized tokens of the ngram separated by space (' ') if n > 1
- __ngram\_pos__: the part of speech tag of each token in the ngram separated by space (' ') if n > 1
- __contains\_stopword__: TRUE if any of the tokens in the ngram are considered stop words, otherwise FALSE


___Note:___ Different counts of ngrams (e.g. `unigrams.csv`, `bigrams.csv`, `trigrams.csv`) all have the same fields, and __ngram_raw__, __ngram_lemmatized__, __ngram_pos__ are always strings. However, in ngrams where n > 1, we separate tokens with single spaces. For example, consider the sentence "Touch the blue square". The first unigram and bigram are shown below:

#### Unigrams

- __ngram_raw__: "Touch"
- __ngram_number__: 0
- __ngram_lemmatized__: "touch"
- __ngram_pos__: "VERB"
- __contains_stopword__: FALSE

#### Bigrams

- __ngram_raw__: "Touch the"
- __ngram_number__: 0
- __ngram_lemmatized__: "touch the"
- __ngram_pos__: "VERB DET"
- __contains_stopword__: TRUE
