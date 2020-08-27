import tweepy
import logging
import time
from config import create_api
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
from textblob import TextBlob
import re
from matplotlib import pyplot as plt
import streamlit as st


## loading .env file into process.env and starting logging
load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

## grabbing keys for twitter authentication
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

## setting up connection to twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

## sidebar widgets
searchtype = st.sidebar.radio(
    "Search by user or text query",
    ('Query', 'Username'))
searchquery = st.sidebar.text_input("Query/Username", "")
searchcount = st.sidebar.slider('# of posts', 0, 100, 30)

## helper functions for  cleaning up tweet data and getting sentiment
def clean_tweet( tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def get_tweet_sentiment(tweet): 
    analysis = TextBlob(clean_tweet(tweet)) 
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'

st.title("Twitter Sentiment Analysis")
if searchtype == "Query":
    st.markdown("From Query: " + searchquery)
if searchtype == "Username":
    st.markdown("From Username: " + searchquery )


if st.sidebar.button('Search'):
    try:
    # Creation of query method using parameters
        if searchtype == 'Query':
            tweets = tweepy.Cursor(api.search,q=searchquery).items(searchcount)
        else: 
            tweets = tweepy.Cursor(api.user_timeline,id=searchquery).items(searchcount)
        # Pulling information from tweets
        tweets_list = [[clean_tweet(tweet.text), get_tweet_sentiment(tweet.text)]  for tweet in tweets]

        ## Sorting positive, negative, and neutral tweets
        postweets = [tweet for tweet in tweets_list if tweet[1] == 'positive']
        negtweets = [tweet for tweet in tweets_list if tweet[1] == 'negative']
        neutweets = [tweet for tweet in tweets_list if tweet[1] == 'neutral']
        positive = len(postweets)
        negative = len(negtweets)
        neutral = len(neutweets)

        #building pie chart with matplotlib
        fig = plt.figure()
        labels = ["Positive", "Negative", "Neutral"]
        values = [positive, negative, neutral]
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        ax.pie(values, labels = labels, autopct='%1.0f%%', colors=['g','r','gray'])
        st.pyplot()

        #dataframe of tweet and sentiment
        datatable = pd.DataFrame(tweets_list, columns=['Tweet','Sentiment'])
        st.write("Tweets")
        st.table(datatable)

    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)


