# Classification-of-online-chat-order
Classification of chat text into predefined classes

The problem statement is to classify a chat sentence through which user wants to have a service. The classes are predefined – food, movie, travel and grocery.

Words and phrases ring the bell in our brain to recognize which category a particular sentence is talking about. This aspect is taken into consideration i.e. the algorithm desgined here is based on a database from which classes are recognized, else if not found the database can be updated from the answer of the user.

It is kept in mind that these four categories have many common words and common phrases which are enough to confuse the system and generate wrong outputs. For example, 'Salt' belongs to both movie and grocery category. 'Bombay to Goa' is a movie name as well as an indication for travel. 'ticket', 'booking' both are usually brought in case of travel and movie shows. 'rice' cn be found in grocery or it can be meant as cooked rice. To prevent this confusion a scoring system is implemented. Multiwords or phrases are given high preference than single word matching. Whenever a phrase or word matches with word listed under a certain category, score of that category is increased by 1 (for single word) or 2 (for multiword). A separate database is created for updating database taking rsponse from the user so that the similar query can be classified next time. A different code can be implemented after manual correction, if needed, to enhance database by transferring from new entries to main database.

To address multiword checking problem n-grams are generated from the query chat.

The system can be made more 'rational' by introducing few extra feature extraction method based on rule based approach of NLP. e.g. words can further be stemmed and compared with database of categories but actual words should be present as to avoid misinterpretation. Named entiy recognizer (to recognize place name) or POS tagger can also be used as a future version of this code. In newclass.json file all conversation output is stored as user data need screening before updating main database. In class.json file, each word/phrase has value as an empty dictionary. Many attributes/information can be introduced in later phase of work : e.g. in movie – release date, language, 3D/2D etc.


Algorithm:

[1] Take query input from user as string.
[2] Process text and tokenize (in future POS tagging can be done)
[3] Open two json files to load the dictionaries.
[4] For each n-grams produced, longest first i.e. 5-grams is generated first then 4-grams and so on
	[5] For each n-gram tuple
		[6] If it is a phrase : calculate score with point 2 for each occurrence
		[7] If it is a word : calculate score with point 1 for each occurrence
	[8] If any multiword is found to be matched with any ONE category go to step [13]
[9] If NO match found : ask user and update to 'newclass' json file; go to step[14]
[10] If more than one match found:
	[11] If one word/phrase has score much greater than others (50% of its own score):
											go to step[13]
	[12] If more than one words has big scores (there is a high chance of other classes):
											go to step [14]
[13] Seemingly the category is known – ask user for confirmation:
		If yes – store data for future work (optional)
		If no – ask correct category and store in newclass.json
	End
[14] System could not single out a possible class : Ask user for information
		Store the information in newclass.json
	End
