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



### Use the class from TwitterSentiment file to get sentiment of tweets
def main_twitter():
    
    ## Oauth
    api = twitterclient()
    
    ### for each tweet in tweets, if tweet is positive, add to ptweets, if negative, add to ntweets
    tweets = api.get_tweets(query = search, count = 3000)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']


    ### Calculate pos, neg, and neutral tweets and display information
    with st.container():
        st.write("---")
        st.text("Positive tweets percentage:\t {:.2f} %".format(100*len(ptweets)/len(tweets)))
        st.text("Negative tweets percentage:\t {:.2f} %".format(100*len(ntweets)/len(tweets)))
        st.text("Neutral tweets percentage: \t {:.2f} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
        st.write("---")

    ### display tweet text
    for tweet in tweets:

        with st.container():
            ## Markdown
            st.image(tweet["profile_pic"])
            st.markdown('Username: ' + tweet["screen_name"], unsafe_allow_html=False)
            # st.markdown(tweet, unsafe_allow_html=False)
            
            ## Text
            st.write(tweet["text"])

            ## Line
            st.write("---")


def for_users():
        
    ## Oauth
    auth = tweepy.OAuth2BearerHandler(bearer_token='AAAAAAAAAAAAAAAAAAAAAJnleQEAAAAA7BqokH6Q506cB%2FfPDUNaL4%2F8slw%3D0kh9sCDAEVYZJg43oYlVyYRyxwjQt3GrrfQI5JdZ6ITpWV9rAW')
    api = tweepy.API(auth)

    # Gets user's last tweet
    tweets = api.user_timeline(screen_name=search[1:], count=1, tweet_mode='extended')

    # Must be formatted into for loop or a new variable must be set equal to index of it because "user_timeline" returns a list.
    for tweet in tweets:

        st.markdown(tweet.user.screen_name + "'s most recent tweet/reply was:")
        st.markdown('"' + tweet.full_text + '"')





### Sidebar dropdown option for twitter, display twitter stats
if option == "Twitter":

    ## subheader
    st.subheader("Twitter Stats:")

    ### Sidebar dropdown for types of searching
    search = st.sidebar.text_input("Search a phrase:")
    
    ### subheader for stock title
    st.subheader(f"Phrase:" + " " + search.upper())

    ## use twitter function to get tweets, or display an error message
    if search.startswith('@'):
         for_users()
    else:
        try:
            main_twitter()
        except TypeError as e:
            st.text("Search for a phrase!")

if option == "Stocks":

    with st.container():

        st.subheader("Stock Trends")
        ticker = st.sidebar.text_input("Check a Stock:", value="TSLA", max_chars=5)
        st.markdown("Ticker: " + ticker)  # Incorporate a function to change it to company name instead of their ticker.  Makes more user-friendly for people not "stock saavy"
        st.image(f"https://finviz.com/chart.ashx?t={ticker}")

    with st.container():
        ## Oauth
        api = twitterclient()
        
        ### for each tweet in tweets, if tweet is positive, add to ptweets, if negative, add to ntweets
        tweets = api.get_tweets(query = ticker, count = 3000)
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

        ### Calculate pos, neg, and neutral tweets and display information
        with st.container():
            st.write("---")
            st.text("Positive tweets percentage:\t {:.2f} %".format(100*len(ptweets)/len(tweets)))
            st.text("Negative tweets percentage:\t {:.2f} %".format(100*len(ntweets)/len(tweets)))
            st.text("Neutral tweets percentage: \t {:.2f} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
            st.write("---")

        ### display tweet text
        for tweet in tweets:

            with st.container():
                ## Markdown
                st.image(tweet["profile_pic"])
                st.markdown('Username: ' + tweet["screen_name"], unsafe_allow_html=False)
                # st.markdown(tweet, unsafe_allow_html=False)
                
                ## Text
                st.write(tweet["text"])

                ## Line
                st.write("---")



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
