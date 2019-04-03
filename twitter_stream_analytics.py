# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 01:30:14 2016

"""

print("")
print (" BIENVENUE CHEZ NSAT TWITTER ANALYTIC")
print (" ------------------------------------")
print (" COLLECTION DE TWEETS AVEC HASHTAG EN LANGUE FRANCAISE DE LA DATE LA PLUS RECENTE")
print (" A LA PLUS ANCIENNE DEPENDANT DE LA LIMITE DE NOMBRE DES ITEMS VOULUS COLLECTER")
print (" ------------------------------------------------------------------------------")

import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import re
import webbrowser

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import time

consumer_key = "Hje0T2vksU56tWqxKQfKFdOm0"
consumer_secret = "HZ8idpwO4cXusS0EvAjbe8qO7aSPXV12FdwnqKxZSKEpZA4OAF"
access_token = "1107932776840347649-pv3tfClcTj3MRRxiPFmP6yL3Cqwkdh"
access_token_secret = "eL4wMl6NEFQiVmywQNkVbZmCbQJYXGp4zVSbng6rh3rys"

#authenticates our API access

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Saisir le mot clé

print (" Entrer le mot_clé pour la recherche de tweet")
print (" --------------------------------------------")

string = ""

while(True):

    Mot_cle1 = input(" Entrer votre premier mot_cle : ")
    Mot_cle2 = input(" Entrer votre deuxieme mot_cle : ")

    if not Mot_cle1.isdigit() and not Mot_cle2.isdigit() and Mot_cle1 != string and Mot_cle2 != string and type(Mot_cle1) is str and type(Mot_cle1) is str:

        print(" votre premier mot_cle est : ",Mot_cle1)
        print(" votre deuxieme mot_cle est : ",Mot_cle2) 
		#print ("................................")

        class MyStreamListener(StreamListener):
            def __init__(self, time_limit):
                self.start_time = time.time()
                self.limit = time_limit
                self.saveFile = open('twitter_jobs.json', 'a')
                super(MyStreamListener, self).__init__()

            def on_data(self, data):
                if (time.time() - self.start_time) < self.limit:
                    self.saveFile.write(data)
                    self.saveFile.write('\n')
                    return True
                else:
                    self.saveFile.close()
                    return False
					
		#print ("................................")
        print (" VOTRE ANALYSE EST EN COUR ...")
        print ("................................")
		
        myStream = Stream(auth, listener=MyStreamListener(time_limit=1200))
        myStream.filter(track=['#'+Mot_cle1,'#'+Mot_cle2],languages=['fr','en'])

        tweets_data_path = 'twitter_jobs.json'

        tweets_data = []
        tweets_file = open(tweets_data_path, "r")
        for line in tweets_file:
            try:
                tweet = json.loads(line)
                tweets_data.append(tweet)
            except:
                continue
    
        print(len(tweets_data))

        tweets = pd.DataFrame()

        #tweets['YOUR STRING HERE'] = list(map(lambda tweet: tweet.get('YOUR STRING HERE', None),tweets_data))
	
        def word_in_text(word,text):
            if text == None:
                return False
            word = word.lower()
            text = text.lower()    
            match = re.search(word,text)
            if match:
                return True
            else:
                return False
        
        tweets[Mot_cle1] = tweets['text'].apply(lambda tweet: word_in_text(Mot_cle1, tweet))
        tweets[Mot_cle2] = tweets['text'].apply(lambda tweet: word_in_text(Mot_cle2, tweet))

        titles = [ Mot_cle1, Mot_cle2]
        tweets_by_titles = [tweets[Mot_cle1].value_counts()[True], tweets[Mot_cle2].value_counts()[True]]

        x_pos = list(range(len(titles)))
        width = 0.8
        fig, ax = plt.subplots()
        plt.bar(x_pos, tweets_by_titles, width,alpha=1,color='g')
        ax.set_ylabel('Number of tweets', fontsize=15)
        ax.set_title('Ranking: '+Mot_cle1+' vs. '+Mot_cle2+' (Data)', fontsize=10, fontweight='bold')
        ax.set_xticks([p + 0.4 * width for p in x_pos])
        ax.set_xticklabels(titles)
        plt.grid()
        plt.savefig("RankingData.png")
        plt.show()

        def extract_link(text):
            if text == None:
                return ''
            regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
            match = re.search(regex, text)
            if match:
                return match.group()
            return ''
			
        tweets['job'] = tweets['text'].apply(lambda tweet: word_in_text('job', tweet))
        tweets['position'] = tweets['text'].apply(lambda tweet: word_in_text('position', tweet))	
        tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('job', tweet) or word_in_text('position', tweet))
        tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

        tweets_relevant = tweets[tweets['relevant'] == True] #only relevant tweets
        tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != ''] #only tweets with a link
        tweets_relevant_with_link = tweets_relevant_with_link.drop_duplicates(subset=['link']) #remove duplicates

        #open all the links in your default browser
        link_count = 0
        for link_number in range(len(tweets_relevant_with_link)):   
            webbrowser.get().open(tweets_relevant_with_link.iat[link_number,8])
            link_count += 1
            if link_count == 9: #if 10 links have been opened (we start at 0)
                input('Press enter to continue opening links') #wait for user to press enter
                link_count = 0 #reset link_count to 0
  
		# # Store Data in dataframe

	
        def tweets_df(tweets_data):
                        id_list = [tweet.id for tweet in tweets_file]
                        data_set = pd.DataFrame(id_list, columns = ["id"])
                        data_set["text"] = list(map(lambda tweet: tweet.get('text'),tweets_data))
                        data_set["created_at"] = list(map(lambda tweet: tweet.get('created_at'),tweets_data))
                        data_set["retweet_count"] = list(map(lambda tweet: tweet.get('retweet_count'),tweets_data))
                        data_set["user_screen_name"] = list(map(lambda tweet:tweet.get('tweet.author.screen_name'),tweets_data))
                        data_set["user_followers_count"] = list(map(lambda tweet:tweet.get('tweet.author.followers_count'),tweets_data))
                        data_set["user_location"] = list(map(lambda tweet: tweet.get('tweet.author.location'),tweets_data))
                        data_set["Hashtags"] = list(map(lambda tweet: tweet.get('hashtags'),tweets_data))
		    
                        return data_set 
						#data_set = tweets_df(tweets_data)
        data_set = tweets_df(tweets_data)				
        data_set.to_csv(".\\hashtag_nsat.csv")
		
        print( "---------------------------------------------------------------")
        print( "Votre collection des tweets a été effectuee avec succes !") 
		
			
        break
 
    else:
        print(" Le mot_cle ----- "+Mot_cle1+" et "+Mot_cle2+" ----- est invalide !")
        print(" Vueillez entrer une chaine de caractère valide ( ex : 'cette chaine est valide...') ")
 
        continue