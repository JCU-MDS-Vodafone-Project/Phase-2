# Phase-2

## Description of phase 2

The NLP component is designed to extract low level features from the review text for analysis and modelling, whilst enriching and augmenting the data with lexicographic sentiment analysis. The normalised and cleansed data from the pre-processing pipeline is ingested and the following processes are performed as outlined in Figure 11.

- Sentiment analysis of each review, and each sentence of the review
- Tokenisation of reviews into sentences
- Extraction of meaningful bigrams and trigrams
    - Bigrams of the form noun-noun, or adjective-noun
    - Trigrams of the form (noun or adjective) - anything - (noun or adjective)
- Extraction of noun phrases
- Cardinality reduction through lemmatisation and stopword removal
- Extraction of word lists and noun lists

The output of the NLP pipeline is a set of features including individual sentences, word and noun lists, noun phrases, bigrams and trigrams in a lemmatised form to reduce cardinality and tagged with their original survey score and the sentiment of their originating sentence. This data formatting was chosen to allow relationships between features and either their original rating or sentiment to be determined with reduced computational overhead in subsequent pipelines. The processed data is saved alongside any additional metadata in a format compatible with the modelling and analysis pipeline.