from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize


def get_contractions():
    contractions = { 
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he's": "he is",
        "how'd": "how did",
        "how'll": "how will",
        "how's": "how is",
        "i'd": "i would",
        "i'll": "i will",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it'd": "it would",
        "it'll": "it will",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "must've": "must have",
        "mustn't": "must not",
        "needn't": "need not",
        "oughtn't": "ought not",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "that'd": "that would",
        "that's": "that is",
        "there'd": "there had",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'll": "we will",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "where'd": "where did",
        "where's": "where is",
        "who'll": "who will",
        "who's": "who is",
        "won't": "will not",
        "wouldn't": "would not",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are"
    }

    return contractions;

contractions = get_contractions()

def get_all_data():
	# Load data
	engine = create_engine('mysql://root:@localhost:3306/steam')
	# steam_data_query = """SELECT url AS reviewid, content, CAST(recommend AS SIGNED) AS recommend
	#     FROM latest_review"""
	data_query = """SELECT gameid, url, CAST(recommend AS SIGNED) AS recommend, hours_2w, hours_all, posttime, updatetime, EAG, CAST(compensation AS SIGNED) AS compensation, content, initial_release_date, lang
	FROM latest_review
	WHERE lang = 'en'
	AND (trim(content) != ''
	OR trim(content) != ' '
	OR content IS NOT NULL);
	"""
	data = pd.read_sql(data_query, engine)
	print(len(data))
	return data;

def pre_process(text):
#   review_lines = []

#   lines = data['content'].values.tolist()

  text = text.lower().rstrip('\n').strip()
  
  tokens = word_tokenize(text)
  new_text = []
  for word in tokens:
      if word in contractions:
          new_text.append(contractions[word])
      else:
          new_text.append(word)
          
  text = " ".join(new_text)
  return text;

def preprocessing_step():
    data = get_all_data()
    data['pre'] = data['content'].map(pre_process)

    return split_data(data['pre'].values)

def main():
	preprocessing_step()



if __name__ == '__main__':
	main()