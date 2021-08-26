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



# Returns a dataframe containing all occurances of a featiure value, 
# Along with the sentiment of the sentence in which they were found, 
# and the associated review score

# Pass the observation dataframe, and the column to extract
def term_df_with_scores(df, column):
    term_frame = pd.DataFrame(columns = ["term","sentiment","promoter_score"])

    for i in range(len(df)):
        row = df[column].iloc[i]
        row_frame = pd.DataFrame.from_records(row, columns=['term','sentiment','promoter_score'])
        term_frame = term_frame.append(row_frame)

    return term_frame


## Create a function to return the pearson correlation between score and sentiment 
# for Features encoded as leists of tuples

# Pass the observation dataframe and feature column to process
def get_corr(df, column):
    term_frame = term_df_with_scores(df, column)
    term_frame[["sentiment", "promoter_score"]] = term_frame[["sentiment", "promoter_score"]].apply(pd.to_numeric)
    result_frame = pd.DataFrame(columns = ["term","sentiment_correlation","count"])
    unique_terms = term_frame.term.unique()
    
    for term in unique_terms:
        temp_frame = term_frame[term_frame.term==term]
        correlation = temp_frame["sentiment"].corr(temp_frame["promoter_score"])
        count = len(temp_frame)
        if not np.isnan(correlation):
            result_frame = result_frame.append(pd.DataFrame([[term, correlation, count]], columns = ["term","sentiment_correlation","count"]))
    return result_frame


# Get count of documents each word or phrase appears in
# As well as percentage, and rank

def doc_count(df, column):
    # Produce a 2 column df with the document ID and the column to be measured
    temp_df = pd.DataFrame(columns=['review_id', 'term'])
    num_reviews = df.review_id.nunique()
    for i in range(len(df)):
        review_id = df['review_id'].iloc[i]
        for item in df[column].iloc[i]:
            term = item[0]
            temp_df = temp_df.append(pd.DataFrame([[review_id, term]], columns = ["review_id", "term"]))
            
    results = temp_df.groupby(by='term', as_index=False).agg({'review_id': pd.Series.nunique})
    results['percentage'] = results['review_id']/num_reviews * 100
    results = results.sort_values(by='percentage',ascending=False)
    # add a column for rank
    results['rank'] = 0
    r = 1
    for i in range(len(results)):
        results['rank'].iloc[i] = r
        r += 1
    
    results = results.rename(columns={"review_id": "reviews_containing_term"})
    return results

# return a dataframe containing all unique terms for
# a list encoded feature column
def get_unique_terms(df, column):
    
    temp_df = pd.DataFrame(columns=['term'])
    for i in range(len(df)):
        for item in df[column].iloc[i]:
            term = item[0]
            temp_df = temp_df.append(pd.DataFrame([[term]], columns = ["term"]))
            
    return pd.DataFrame(temp_df.term.unique(), columns=['term'])


# For revoews containing each term, return the percentage
# of the reviews that are Detractors, Promoters, and  passive customers
# as well as the difference in count between
# detractors and promoters

def track_rank_changes(df, column):
    #results = pd.DataFrame(columns=['term', 'perc_detractor', 'perc_passive', 'perc_promoter', 'total_change'])
    all_unique_terms = get_unique_terms(df, column)
    #print(all_unique_terms)
    all_unique_terms['perc_detractor'] = 0
    all_unique_terms['perc_passive'] = 0
    all_unique_terms['perc_promoter'] = 0
    all_unique_terms['total_change'] = 0    
    
    
    detractors = doc_count(df[df['score'] <=3], column)
    passive = doc_count(df[df['score'] ==4], column)
    promotors = doc_count(df[df['score'] ==5], column)
    
    for i in range(len(all_unique_terms)):
        if all_unique_terms['term'].iloc[i] in detractors['term'].tolist():
            perc_detractor = detractors[detractors['term'] == all_unique_terms['term'].iloc[i]].percentage.iloc[0]
        else:
            perc_detractor = 0
            
        if all_unique_terms['term'].iloc[i] in passive['term'].tolist():
            perc_passive = passive[passive['term'] == all_unique_terms['term'].iloc[i]].percentage.iloc[0]
        else:
            perc_passive = 0
        
        if all_unique_terms['term'].iloc[i] in promotors['term'].tolist():
            perc_promoter = promotors[promotors['term'] == all_unique_terms['term'].iloc[i]].percentage.iloc[0]
        else:
            perc_promoter = 0
            
        total_change = perc_promoter - perc_detractor
        
        all_unique_terms['perc_detractor'].iloc[i] = perc_detractor
        all_unique_terms['perc_passive'].iloc[i] = perc_passive
        all_unique_terms['perc_promoter'].iloc[i] = perc_promoter
        all_unique_terms['total_change'].iloc[i] = total_change        

    return all_unique_terms.sort_values(by='total_change',ascending=False)


if __name__ == '__main__':
	term_df_with_scores()