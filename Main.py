from msilib.schema import Error
from requests import request
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import requests as re
import pytwits as pt
import plotly
from TwitterSentiment import twitterclient
import dotenv

### Load Bearer token
dotenv.load_dotenv()

### Dashboard Title
st.title("Dashboard")

### Sidebar Title
st.sidebar.title("Options:")

### Sidebar Dropdown
option = st.sidebar.selectbox("Select Dashboard:", ("Twitter", "Wallstreetbets", "StockTwits", "Chart", "Pattern"))

### Sidebar Search bar
search_option = st.sidebar.text_input("Search a ticker:")

### subheader for stock title
st.subheader("Phrase: " + search_option.upper())

### Use the class from TwitterSentiment file to get sentiment of tweets
def main_twitter():
    
    ## Oauth
    api = twitterclient()

    ### for each tweet in tweets, if tweet is positive, add to ptweets, if negative, add to ntweets
    tweets = api.get_tweets(query = search_option, count = 3000)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    ### Calculate pos, neg, and neutral tweets and display information
    st.write("-------------------------------------------------------")
    st.text("Positive tweets percentage:\t {} %".format(100*len(ptweets)/len(tweets)))
    st.text("Negative tweets percentage:\t {} %".format(100*len(ntweets)/len(tweets)))
    st.text("Neutral tweets percentage: \t {} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
    st.text("--------------------------------------------------------")

    ### display tweet text
    for tweet in tweets:

        ## Markdown
        st.markdown(tweet, unsafe_allow_html=False)

        ## Text
        st.text(tweet)

        ## Line
        st.text("--------------------------------------------------------")


### Sidebar dropdown option for twitter, display twitter stats
if option == "Twitter":

    ## subheader
    st.subheader("Twitter Stats:")

    ## use twitter function to get tweets, or display an error message
    try:
        main_twitter()
    except TypeError as e:
        st.text("Search for a stock!")

### wallstreetbets 
if option == "Wallstreetbets":
    st.subheader("Wallstreetbets Mentions:")

### Stocktwits mentions of stock
if option == "StockTwits":
    st.subheader("Stocktwits Mentions:")

    stocktwit = pt.StockTwits()
    symbols = stocktwit.search(path='search/symbols', q=search_option.upper())
    stock = symbols[0]

### display charts and relevant information
if option == "Chart":
    st.subheader("Charts:")
    stock = yf.download(search_option, interval="1d", period="1y")["Close"]
    st.line_chart(stock)

### display patterns and options
if option == "Pattern":
    st.subheader("Patterns")

