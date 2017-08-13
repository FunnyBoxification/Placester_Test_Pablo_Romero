# For this solution I'm using TextBlob, using it's integration with WordNet.

from textblob import TextBlob
from textblob import Word
from textblob.wordnet import VERB
import nltk
import os
import sys
import re
import json

results = { "results" : [] }

#Override NLTK data path to use the one I uploaded in the folder
dir_path = os.path.dirname(os.path.realpath(__file__))
nltk_path = dir_path + os.path.sep + "nltk_data"
nltk.data.path= [nltk_path]

#Text to analyze
TEXT = """
        Take this paragraph of text and return an alphabetized list of ALL unique words.  A unique word is any form of a word often communicated
        with essentially the same meaning. For example,
        fish and fishes could be defined as a unique word by using their stem fish. For each unique word found in this entire paragraph,
        determine the how many times the word appears in total.
        Also, provide an analysis of what sentence index position or positions the word is found.
        The following words should not be included in your analysis or result set: "a", "the", "and", "of", "in", "be", "also" and "as".
        Your final result MUST be displayed in a readable console output in the same format as the JSON sample object shown below. 
        """
TEXT = TEXT.lower()

WORDS_NOT_TO_CONSIDER = ["a", "the", "and", "of", "in", "be", "also", "as"]
nlpText= TextBlob(TEXT)

def getSentenceIndexesForWord(word, sentences):
    sentenceIndexes = []
    for index, sentence in enumerate(sentences):
        count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word.lower()), sentence))
        if count > 0:
            sentenceIndexes.append(index)
    return sentenceIndexes

#1: Get all words, excluding repetitions and all the sentences in the text
nlpTextWords = sorted(set(nlpText.words))
nlpTextSentences = nlpText.raw_sentences

#2 Get results
synonymsList = []
allreadyReadWords = []
for word in nlpTextWords:
    if word not in WORDS_NOT_TO_CONSIDER and word not in allreadyReadWords:
        timesInText = nlpText.word_counts[word]
        
        #Get sentence indexes where the word can be found
        sentenceIndexes = getSentenceIndexesForWord(word, nlpTextSentences)

        #Check for synonyms
        for word2 in nlpTextWords:
            if word2 not in WORDS_NOT_TO_CONSIDER and ( word.lower() != word2.lower() and len(list(set(word.synsets) & set(word2.synsets))) > 0 ):
                #If I find a synonym of the word I add it to the list of words allready read and add the times that synonym appeared in the text to the total
                #count of the unique word and the corresponding sentence indexes
                allreadyReadWords.append(word2)
                timesInText = timesInText + nlpText.word_counts[word2]
                sentenceIndexes += getSentenceIndexesForWord(word2,nlpTextSentences)
                
        allreadyReadWords.append(word)
        
        results["results"].append({"word" : word.lemmatize(), #I return the lemma of the word because TextBlob's stems seem to be wrong for certain words
                                   "total-occurances": timesInText,
                                   "sentence-indexes": sorted(set(sentenceIndexes))})

print(json.dumps(results, indent=4))
            
            
        
