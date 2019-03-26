# -*- coding: utf-8 -*-

# # Import Libraries

# In[1]:

print("")
print (" BIENVENUE CHEZ NSAT TWITTER ANALYTIC")
print (" ------------------------------------")
print (" COLLECTION DE TWEETS AVEC HASHTAG EN LANGUE FRANCAISE DE LA DATE LA PLUS RECENTE")
print (" A LA PLUS ANCIENNE DEPENDANT DE LA LIMITE DE NOMBRE DES ITEMS VOULUS COLLECTER")
print (" ------------------------------------------------------------------------------")

import tweepy
import matplotlib.pyplot as plt
import numpy as np
import pylab
import json
import pandas as pd
import random

import scipy.misc 
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib as mpl
import csv

import operator 
from textblob import TextBlob
from textblob import Word
from textblob.sentiments import NaiveBayesAnalyzer

# # Authentication

# In[2]:

#Twitter API credentials

consumer_key = "Hje0T2vksU56tWqxKQfKFdOm0"
consumer_secret = "HZ8idpwO4cXusS0EvAjbe8qO7aSPXV12FdwnqKxZSKEpZA4OAF"
access_token = "1107932776840347649-pv3tfClcTj3MRRxiPFmP6yL3Cqwkdh"
access_token_secret = "eL4wMl6NEFQiVmywQNkVbZmCbQJYXGp4zVSbng6rh3rys"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Interacting with twitter's API
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API (auth) #creating the API object

# # Extracting Tweets

# In[3]:

# Saisir le mot clé

print (" Entrer le mot_clé pour la recherche de tweet")
print (" --------------------------------------------")

Mot_cle =input(" Entrer votre mot_cle : ")

while True:
	# on test si le mot clé est bien une chaine de caractère
	if Mot_cle.isalpha():
		print(" Le mot_cle est : ",Mot_cle) 

		results = []
		for tweet in tweepy.Cursor (api.search, q = Mot_cle, lang = "fr").items(200): 
		    results.append(tweet)
		print (type(results))
		print (len(results))

		#print (results[4000].text)

		# # Store Data in dataframe

		# In[4]:
		
		def tweets_df(results):
		    id_list = [tweet.id for tweet  in results]
		    data_set = pd.DataFrame(id_list, columns = ["id"])
		   	
		    data_set["text"] = [tweet.text for tweet in results]
		    data_set["created_at"] = [tweet.created_at for tweet in results]
		    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
		    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
		    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
		    data_set["user_location"] = [tweet.author.location for tweet in results]
		    data_set["Hashtags"] = [tweet.entities.get('hashtags') for tweet in results]
		    
		    return data_set
		data_set = tweets_df(results)

		# Remove duplicate tweets
		# On procède à la suppression de tweets dupliqués pour de raison de performance
		# In[5]:

		text = data_set["text"]

		for i in range(0,len(text)):
		    txt = ' '.join(word for word in text[i] .split() if not word.startswith('https:'))
		    data_set.set_value(i, 'text2', txt)
		    
		data_set.drop_duplicates('text2', inplace=True)
		data_set.reset_index(drop = True, inplace=True)
		data_set.drop('text', axis = 1, inplace = True)
		data_set.rename(columns={'text2': 'text'}, inplace=True)

		# # Sentiment Analysis of tweets
		# Analyse de tweets le plus suivi 
		# In[6]:

		text = data_set["text"]
		
		for i in range(0,len(text)):
		    textB = TextBlob(text[i])
		    sentiment = textB.sentiment.polarity
		    data_set.set_value(i, 'Sentiment',sentiment)
		    if sentiment <0.00:
		        SentimentClass = 'Negative'
		        data_set.set_value(i, 'SentimentClass', SentimentClass )
		    elif sentiment >0.00:
		        SentimentClass = 'Positive'
		        data_set.set_value(i, 'SentimentClass', SentimentClass )
		    else:
		        SentimentClass = 'Neutral'
		        data_set.set_value(i, 'SentimentClass', SentimentClass )
		
		# In[7]:

		# Ici est le chemin absolue où sera créé le fichier .csv qui contiendra l'ensemble des données recoltées
		
		data_set.to_csv(".\\"+Mot_cle+"_hashtag_nsat.csv")	
		
		# Extract all hashtags for all tweets

		# In[8]:

		Htag_df = pd.DataFrame()
		j = 0

		for tweet in range(0,len(results)):
		    hashtag = results[tweet].entities.get('hashtags')
		    for i in range(0,len(hashtag)):
		        Htag = hashtag[i]['text'] 
		        Htag_df.set_value(j, 'Hashtag',Htag)
		        j = j+1

		# In[9]:

		Htag_df

		# In[16]:
		# Le chemin absolue où sera créé le fichier .csv qui contiendra l'ensemble des hashtage
		nsat_Hashtag = Htag_df.groupby('Hashtag').size()
		nsat_Hashtag.to_csv(".\\"+Mot_cle+"_search_Htag_nsat.csv")
		
		print( "---------------------------------------------------------------")
		print( "Votre collection des tweets sur " + Mot_cle + " a été effectuee avec succes !")
		
		#Affichage de l'histograme
		
		plt.hist(text, 100)
		plt.title("Histogram de tweet sur "+Mot_cle+" par NSAT SARL", fontsize=10)
		width = 0.05
		plt.savefig("Histogram" +Mot_cle+".png")
		plt.show()
		
		break
	else:
		print(" Le mot_cle ----- "+Mot_cle+" ----- est invalide !")
		print(" Vueillez entrer une chaine de caractère valide ( ex : 'cette chaine est valide...') ")
		break
		
