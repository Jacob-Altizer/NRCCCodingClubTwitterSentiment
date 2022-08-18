##Main file for the Twitter Sentiment analysis project for the NRCC Coding Club
##Authors: Aidan Murphy

##Import Resources
import re
from time import sleep
from tkinter import StringVar, font, ttk
from tkinter.tix import COLUMN
import tweepy
from tweepy import OAuthHandler
import textblob
from dotenv import load_dotenv
import os
import tkinter
from ttkthemes import ThemedTk

load_dotenv()

### create main window for GUI
window = ThemedTk(theme = "breeze")
window.title("Tweet Sentiment: A Program")
window.geometry("780x340")

### Title and one tab objects
tab_parent = ttk.Notebook(window)
tab1 = ttk.Frame(tab_parent)

## title
tab_parent.add(tab1, text = "Sentiment Anlysis")
tab_parent.pack(expand=1, fill="both")

## labels
ttk.Label(tab1, text="Tweet Analysis", font=("Harlow Solid Italic",15)).grid(row=0,column=1)

## label 1
ttk.Label(tab1, text="User Search", font=("Times New Roman", 15)).grid(column=0,row=5, padx=10,pady=10)
## label 2
ttk.Label(tab1, text="Phrase Search", font=("Times New Roman", 15)).grid(column=0,row=6, padx=10,pady=10)

## label vars
user_var = tkinter.StringVar()
phrase_var = tkinter.StringVar()

tab_parent.pack(expand=1,fill="both")

## run main window
window.mainloop()

### get phrase to analyze from user
user_input = input("Phrase to analyze:\t")

## if phrase starts with "@", analyze last tweet of user
if not user_input.startswith("@"):
    Tweets_to_analyze = int(input("Tweets to anlayze:\t"))
    iterations = int(input("Iterations:\t\t"))
print("-------------------------------------------------------")

##Authorize Twitter Clients via class
class twitterclient(object):
    
    def __init__(self):
    
        self.auth = tweepy.OAuth2BearerHandler(os.environ.get('Bearer_token'))
        self.api = tweepy.API(self.auth)

    ## first func, Clean tweets of hyperlinks
    def clean_tweet(self, tweet):
    
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    ## Second func, Analyze tweets for sentiment
    def get_tweet_sentiment(self, tweet):

        ## Use textblob to analyze sentiment
        analysis = textblob.TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    ## third func, get retweet count
    def get_retweet_count(self, tweet):
        
        count = self.api.get_status(tweet)
        return count

    ## fourth func, get last tweet of user
    def get_last_tweet(self,account):
        
        tweets = []
        
        tweet = self.api.user_timeline(id=account, count = 1, tweet_mode = "extended")[0]
        
        tweets.append(tweet)

        for tweet in tweets:

                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)
                parsed_tweet['retweet_count'] = tweet.retweet_count

                print("Date: " + str(tweet.created_at))
                print("Text: "+str(parsed_tweet['text']) + "\n")
                print("Sentiment: "+str(parsed_tweet['sentiment']))
                print("Retweets: "+str(parsed_tweet['retweet_count']))
                print("Likes: " + str(tweet.favorite_count))




    ## fifth func, retrieve tweets
    def get_tweets(self, query, count= 5):
        
        ## create tweet list
        tweets = []

        ## get tweets containing phrase
        try:
            fetched_tweets = self.api.search_tweets(q=query, count = count, tweet_mode = 'extended')
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)
                parsed_tweet['retweet_count'] = tweet.retweet_count

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepyException as e:
            print("ERROR: " + str(e))

## Get tweets then add them to positive or negative tweets based on sentiment
def main():
    
    ## Oauth
    api = twitterclient()
    
    ## if input starts with
    if user_input.startswith('@'):
        print("-------------------------------------------------------")
        api.get_last_tweet(user_input)
        print("-------------------------------------------------------")
    else:
        z=0
        while z<int(iterations):
            print("-------------------------------------------------------")
            print("Iteration: " + str(z+1))
            tweets = api.get_tweets(query = user_input, count = Tweets_to_analyze)
            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
            print("Positive tweets percentage:\t {} %".format(100*len(ptweets)/len(tweets)))
            print("Negative tweets percentage:\t {} %".format(100*len(ntweets)/len(tweets)))
            print("Neutral tweets percentage: \t {} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
            print("-------------------------------------------------------")

            # print("-------------------------------------------------------")
            # max_retweets = max(tweets, key=lambda x:x['retweet_count'])
            # for key in max_retweets:
            #     print("\n")
            #     print(key + ': ' + str(max_retweets[key]))
            # print("-------------------------------------------------------")

            # max_pretweets = max(ptweets, key=lambda x:x['retweet_count'])
            # for key in max_pretweets:
            #     print("\n")
            #     print(key + ': ' + str(max_pretweets[key]))
            # print("-------------------------------------------------------")

            # max_nretweets = max(ntweets, key=lambda x:x['retweet_count'])
            # for key in max_nretweets:
            #     print("\n")
            #     print(key + ': ' + str(max_nretweets[key]))
            #     print("\n")
            # print("-------------------------------------------------------")

            z = z+1
            sleep(10)

if __name__ == "__main__":
    main()
