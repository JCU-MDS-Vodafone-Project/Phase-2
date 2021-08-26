#Import Libraries
# Probably more functions than you'll need...
from bs4 import BeautifulSoup
import re
import pandas as pd
from spellchecker import SpellChecker
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast


import numpy as np
# Install new libraries
#%pip install pyspellchecker
#%pip install TextBlob

import warnings
warnings.filterwarnings('ignore')


def load_path(data_path):
    
    # Load processed dataset into DataFrame
    preprocessed_vodafone_reviews = pd.read_csv(data_path)  

    # Identify which columns are lists

    columns = list(preprocessed_vodafone_reviews.columns)

    # create empty list to contain a list of columns that are lists...  listslistslistslists...lists
    list_columns = []


    for column in columns:
        first_row_value = str(preprocessed_vodafone_reviews[column].iloc[0])
        first_character = first_row_value[0]
        last_character = first_row_value[len(first_row_value)-1]
        # A column /probably/ contains lists if values starte with a [ and end with a ]
        if first_character == "[" and last_character == "]":
            list_columns = list_columns + [column]

    # Lists will initially be expressed as strings when imported form CSV
    # We will use AST to convert these string columns back to list
    # This function could probably be better implemented without a for loop
    # but works for now...

    # List encode columns contain lists of tuples in the format:
    # ("feature value", "Sentiment of originating sentence", "Review Promoter score")

    # Abstract syntax tree is used to recreate the lists of tuples stored in the pre-processed data
    for i in range(len(preprocessed_vodafone_reviews)):
        for column in list_columns:
            preprocessed_vodafone_reviews[column].iloc[i] = list(ast.literal_eval(preprocessed_vodafone_reviews[column].iloc[i]))


    return preprocessed_vodafone_reviews

if __name__ == '__main__':
	load_path()