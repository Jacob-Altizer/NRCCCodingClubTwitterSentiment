from msilib.schema import Error
from requests import request
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import requests as re
import pytwits as pt
import plotly
import tweepy
from TwitterSentiment import twitterclient
import dotenv
import matplotlib.pyplot as plt

### Load Bearer token
dotenv.load_dotenv()

### Page config (Title at top and icon at top )
st.set_page_config(page_title="Tweet Analysis", page_icon="chart_with_upwards_trend")

### Dashboard Title
st.title("Dashboard")

### Sidebar Title
st.sidebar.title("Options:")

### Sidebar Dropdown
option = st.sidebar.selectbox("Select Dashboard:", ("Twitter", "Stocks"))

### Sidebar user Search bar


### uses css to create styles for each tweet
def create_tweet_styles():
    ## CSS selectors created by manually grabbing class from inpsect element in browser / all containers will have the same auto-generated class in the html
    tweet_styles = '''
    <style>
        /* container encompasing tweet */
        div.css-1ex6qxy.e1tzin5v0 div.css-1ex6qxy.e1tzin5v0 {
            background-color: rgb(34, 42, 64);
            padding: 0px;
            overflow-wrap: break-word;
            border: 2px solid;
            border-radius: 10px;
        }

    </style>
    '''
    st.markdown(tweet_styles, unsafe_allow_html=True)


### Use the class from TwitterSentiment file to get sentiment of tweets
def main_twitter():

    ## Oauth
    api = twitterclient()

    try:
        ### for each tweet in tweets, if tweet is positive, add to ptweets, if negative, add to ntweets
        tweets = api.get_tweets(query = search, count = 3000)
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        
        # Finds the tweet with the most likes of the list NOTE: CLEANUP THIS AND MOST RETWEETS SECTION ASAP...PROBABLY CREATE FUNCTION TO GET MAX
        try:
            max_likes = tweets[0]['num_likes']

            for tweet in tweets:
                if tweet['num_likes'] >= max_likes:
                    max_likes = tweet['num_likes']
                    tweet_most_likes = tweet['text']
                    screen_name_most_likes = tweet['screen_name']
                    profile_pic_most_likes = tweet['profile_pic']

        except IndexError:
            pass

        # Finds the tweet with the most retweets of the list
        try:
            max_retweets = tweets[0]['retweet_count']

            for tweet in tweets:
                if tweet['retweet_count'] >= max_retweets:
                    max_retweets = tweet['retweet_count']
                    tweet_most_retweets = tweet['text']
                    screen_name_most_retweets = tweet['screen_name']
                    profile_pic_most_retweets = tweet['profile_pic']
                    num_likes_most_retweets = tweet['num_likes']
                    
        except IndexError:
            pass
        
        # Displays the user's profile pic, username, number of likes, and tweet at the top of the page.  If all tweets found have 0 likes (max_likes = 0), then it will display that all tweets found have 0 likes 
        try:
            if max_likes >= 1:
                st.write("---")
                st.write("The tweet with the most likes was:")
                ## Markdown
                st.image(profile_pic_most_likes)
                st.markdown('Username: ' + screen_name_most_likes, unsafe_allow_html=False)
                st.write(f"Number of likes: {max_likes}")
                # st.markdown(tweet, unsafe_allow_html=False)
                        
                ## Text
                st.write(tweet["text"])
            else:
                st.write("---")
                st.write("All tweets found have 0 likes.")
        except UnboundLocalError:
            pass

        # Does same as above, but for user with the most retweets.
        try:
            if max_retweets >= 1:
                st.write("---")
                st.write("The tweet with the most retweets was:")
                ## Markdown
                st.image(profile_pic_most_retweets)
                st.markdown('Username: ' + screen_name_most_retweets, unsafe_allow_html=False)
                st.write(f"Number of likes: {num_likes_most_retweets}")
                st.write(f"Number of retweets: {max_retweets}")
                # st.markdown(tweet, unsafe_allow_html=False)
                        
                ## Text
                st.write(tweet["text"])
            else:
                st.write("---")
                st.write("All tweets found have 0 retweets.")
        except UnboundLocalError:
            pass

        
        st.write("---")
        positive_tweets_percent = (100*len(ptweets)/len(tweets))
        negative_tweets_percent = (100*len(ntweets)/len(tweets))
        neutral_tweets_percent = (100*(len(tweets)-(len( ntweets )+len( ptweets)))/len(tweets))
        
        # NOTE: CLEAN UP ASAP
        labels = ['Positive', 'Negative', 'Neutral']
        sizes = [positive_tweets_percent, negative_tweets_percent, neutral_tweets_percent]
        max_percent = max([positive_tweets_percent, negative_tweets_percent, neutral_tweets_percent])
        pos_explode = 0
        neg_explode = 0
        neutral_explode = 0
        if max_percent == positive_tweets_percent:
            pos_explode = 0.05
        elif max_percent == negative_tweets_percent:
            neg_explode = 0.05
        elif max_percent == neutral_tweets_percent:
            neutral_explode = 0.05
        explode = [pos_explode,neg_explode,neutral_explode]
        fig1,ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        fig1.set_facecolor('#0e1117')
    
        st.pyplot(fig1)
        
        st.write("---")

        ### display tweet text
        for tweet in tweets:

            with st.container():

                create_tweet_styles()

                ## Markdown
                st.image(tweet["profile_pic"])
                st.markdown('Username: ' + tweet["screen_name"], unsafe_allow_html=False)
                st.write(f"Number of likes: {tweet['num_likes']}")
                # st.markdown(tweet, unsafe_allow_html=False)
                
                ## Text
                st.write(tweet["text"])


    except:
        st.subheader("There were no tweets found.")
        st.write("---")

    ### for each tweet in tweets, if tweet is positive, add to ptweets, if negative, add to ntweets
    # tweets = api.get_tweets(query = search, count = 3000)
    # ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']


    # ### Calculate pos, neg, and neutral tweets and display information
    # st.write("---")
    # st.text("Positive tweets percentage:\t {:.2f} %".format(100*len(ptweets)/len(tweets)))
    # st.text("Negative tweets percentage:\t {:.2f} %".format(100*len(ntweets)/len(tweets)))
    # st.text("Neutral tweets percentage: \t {:.2f} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
    # st.write("---")





def for_users():

    ## Oauth
    auth = tweepy.OAuth2BearerHandler('Bearer_token')
    api = tweepy.API(auth)

    # Gets user's last tweet
    tweets = api.user_timeline(screen_name=search[1:], count=1, tweet_mode='extended')

    # Must be formatted into for loop or a new variable must be set equal to index of it because "user_timeline" returns a list.
    for tweet in tweets:

        st.markdown(f"{tweet.user.screen_name}'s most recent tweet/reply was:")
        st.markdown(f'{tweet.full_text}')



### Sidebar dropdown option for twitter, display twitter stats
if option == "Twitter":

    ## subheader
    st.subheader("Twitter Stats:")

    ### Sidebar dropdown for types of searching
    search = st.sidebar.text_input("Search a phrase:")
    
    ### subheader for stock title
    st.subheader('Phrase: {}'.format(search.upper()))

    ## use twitter function to get tweets, or display an error message
    if search.startswith('@'):
         for_users()
    else:
        try:
            main_twitter()
        except TypeError as e:
            st.text("Search for a phrase!")

if option == "Stocks":

    ## subheader
    st.subheader("Stock Trends:")

    ## Sidebar input for stock ticker
    search = st.sidebar.text_input("Check out a Stock:", value="TSLA", max_chars=5)

    ## displays searched ticker on page
    st.markdown("Ticker: " + search)  # Incorporate a function to change it to company name instead of their ticker. Makes more user-friendly for people not "stock saavy"

    ## inserts ticker into finviz.com url to get chart
    st.image(f"https://finviz.com/chart.ashx?t={search}")

    try:
        main_twitter()
    except TypeError as e:
        st.text("Search for a stock ticker!")



### wallstreetbets 
# if option == "Wallstreetbets":

    ### subheader
    # st.subheader("Wallstreetbets Mentions:")

### Stocktwits mentions of stock
# if option == "StockTwits":

#     ### subheader
#     st.subheader("Stocktwits Mentions:")

#     stocktwit = pt.StockTwits()
#     symbols = stocktwit.search(path='search/symbols', q=search_option.upper())
#     stock = symbols[0]

# ### display charts and relevant information
# if option == "Chart":

#     ### subheader
#     st.subheader("Charts:")
#     stock = yf.download(search_option, interval="1d", period="1y")["Close"]
#     st.line_chart(stock)

### display patterns and options
# if option == "Pattern":
#     st.subheader("Patterns")
