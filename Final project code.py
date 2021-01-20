import matplotlib.pyplot as plt
import pandas as pd
import tweepy
import ssl
import csv
from textblob import TextBlob

ssl._create_default_https_context = ssl._create_unverified_context
# Oauth keys
consumer_key = "c2rNqpUE2R4SBHPwL32Vsglw4"
consumer_secret = "AWOyMLny3DT4SJ63dBAlKdUuswfvEziBYwnsqIc5qkrI2Ml25B"

callback = 'oob' 
# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
redirect_url = auth.get_authorization_url()

user_pin = input("Please enter user pin : ")
auth.get_access_token(user_pin)
api = tweepy.API(auth)

name ="JoeBiden"


replies=[]
for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout = 999999, lang='en').items(1000):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
            replies.append(tweet)
            
outtweets = [[ tweet.text] for tweet in replies]
df = pd.DataFrame(outtweets)
df.to_csv('replies.csv', index=False)


positive = 0
negative = 0
neutral = 0
polarity = 0

infile = 'replies.csv'


with open(infile, 'r' , encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        sentence = row[0]
        analyze = TextBlob(sentence)
        polarity += analyze.sentiment.polarity
        
        if (analyze.sentiment.polarity == 0):
            neutral += 1
        elif (analyze.sentiment.polarity < 0.00):
            negative += 1
        elif (analyze.sentiment.polarity > 0.00):
            positive += 1
print("Sentiment Scores are :")            
print(positive)
print(negative)
print(neutral)

def percentage(part,whole):
        return 100 * float(part)/float(whole)

            
Positive =percentage(positive, 1000)
print(Positive)
Negative =percentage(negative, 1000)
print(Negative)                         
Neutral = percentage(neutral, 1000)
print(Neutral)
Polarity = percentage(polarity, 1000)
print(Polarity)

positive = format(positive , '2f')            
negative = format(negative , '2f')       
neutral = format(neutral , '2f')

label = ['Positive [' + str(Positive) + '%]', 'Negative [' + str(Negative) + '%]','Neutral [' + str(Neutral) + '%]']
sizes = [positive, negative, neutral]
colors = ['orange','blue','grey']
patches,text = plt.pie(sizes , colors = colors, shadow = True )
plt.legend(patches,label, loc="best")
plt.title("People reacting to Joe Biden tweets is :")
plt.axis('equal')
plt.tight_layout()
plt.show()