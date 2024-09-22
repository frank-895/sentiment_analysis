import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_headers():
    """Retrieve Reddit API headers to access Reddit data."""
    load_dotenv()
    client_id = os.getenv("CLIENT_ID") # retrieve keys
    client_secret = os.getenv("CLIENT_SECRET")

    url = "https://www.reddit.com/api/v1/access_token" # define the endpoint for access token
    auth = HTTPBasicAuth(client_id, client_secret) # create authentication using client ID and secret
    data = {'grant_type': 'client_credentials'} # define the data for the request    
    headers = {'User-Agent': 'MyRedditApp/1.0 by Prestigious_Monk1227'} # define headers
    response = requests.post(url, auth=auth, data=data, headers=headers) #request the access token

    if response.status_code == 200: # Check for a successful response
        token = response.json().get('access_token')
        headers['Authorization'] = f'bearer {token}' # Use the token to make requests
        return headers
    else:
        raise Exception("Failed to access redit API")      

def retrieve_posts(n, company):
    """
    Retrieves n reddit posts containing name of company. 
    n should be integer between 1 and 100 (inclusive)
    company should be string no greater than 15 characters
    """
    # validate inputs
    if (
        type(n) != int or 
        n <= 0 or 
        n > 100 or
        type(company) != str or 
        len(company) > 30
        ):
        raise ValueError("Ensure inputs are correctly formatted.")
    
    # Define variables
    url = "https://oauth.reddit.com/search"
    params = {
        'q': f'{company} subreddit:unitedkingdom', # query
        'limit': n, # number of queries
        'nsfw':'no'
    }
    headers = get_headers() # get access to API

    response = requests.get(url, headers=headers, params=params).json() # request from reddit API

    post_info = [] # store info from each post
    for post in response['data']['children']: # returns info about each post requested
        post_info.append(post['data']['title'] + post['data']['selftext']) # for each post gather its title and text for analysis
    return post_info

def perform_sentiment_analysis(posts:list[str], company:str):
    """Performs sentiment analysis on each post in posts. Returns the average sentiment and number of posts used for analysis in tuple."""
    
    analyser = SentimentIntensityAnalyzer() # create analyser instance
    
    avg = 0 # track sentiment scores
    failed = 0
    for post in posts: # find sentiment for each posts
        if (company.lower() in post.lower()): # This is a bit inefficient, limited by results from reddit API
            sentiment = analyser.polarity_scores(post) # perform sentiment analysis with VADER
            avg += sentiment['compound'] # compound is overall sentiment between -1 and 1. *note - possible to extract positive, negative and neutral scores too.
        else:
            failed += 1
    
    return (avg/len(posts), len(posts) - failed) # return average sentiment and number of posts checked in tuple

companies = [] # stores company names
with open('companies.txt', 'r') as file: # read in company names for sentiment analysis
        companies = [company.strip() for company in file.readlines()]

# find baseline sentiment for word 'supermarket'
no_to_analyse = 100 # 100 is max no. of posts that can be scraped with reddit API
posts = retrieve_posts(no_to_analyse, 'supermarket')
baseline_sentiment, _ = perform_sentiment_analysis(posts, 'supermarket')

df = pd.DataFrame(columns=['Supermarket', 'Sentiment', 'Deviation', 'n'])
for company in companies:
    posts = retrieve_posts(no_to_analyse, company) # retrieve posts for sentiment analysis
    sentiment, n = perform_sentiment_analysis(posts, company) # for each company attain avg sentiment score
    df.loc[len(df)] = {'Supermarket':company, 'Sentiment': sentiment, 'Deviation': sentiment - baseline_sentiment, 'n':n} # insert relevant stats into df
df = df.sort_values(by='Deviation', ascending=True) # sort dataframe

# Plot deviation from baseline sentiment for each supermarket
plt.figure(figsize=(12,8))
sns.barplot(x='Supermarket', y='Deviation', data=df)
plt.xlabel('Supermarket')
plt.ylabel('Sentiment Deviation from Baseline')
plt.title('Deviation from Baseline Sentiment for UK Supermarkets')
plt.xticks(rotation=45)
plt.show()

# Plot sample size for each supermarket
df = df.sort_values(by='n', ascending=True)
plt.figure(figsize=(12,8))
sns.barplot(x='Supermarket', y='n', data=df)
plt.xlabel('Supermarket')
plt.ylabel('Sample Size')
plt.title('Number of Posts Sentiment Analysed for Each Supermarket')
plt.xticks(rotation=45)
plt.show()