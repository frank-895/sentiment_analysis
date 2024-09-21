import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

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
    Retrieves n reddit posts containing name of company from start_date to end_date. 
    n should be integer between 1 and 100 (inclusive)
    company should be string no greater than 15 characters
    Dates should be supplied in format 'YYYY-MM-DD'
    """
    
    # validate inputs
    if (
        type(n) != int or 
        n <= 0 or 
        n > 100 or
        type(company) != str or 
        len(company) > 15
        ):
        raise ValueError("Ensure inputs are correctly formatted.")
    
    # Define variables
    url = "https://oauth.reddit.com/search"
    params = {
        'q': company, # query
        'limit': n, # number of queries
    }
    headers = get_headers() # get access to API

    response = requests.get(url, headers=headers, params=params).json() # request from reddit API

    post_info = [] # store info from each post
    for post in response['data']['children']: # returns info about each post requested
        post_info.append(post['data']['title'] + post['data']['selftext']) # for each post gather its title and text for analysis
    return post_info

def perform_sentiment_analysis(post:str):
    """Performs sentiment analysis on 'post'"""
    analyser = SentimentIntensityAnalyzer() # create analyser instance
    sentiment = analyser.polarity_scores(post) # sentiment scores.
    return sentiment['compound'] # compound is overall sentiment between -1 and 1. *note - possible to extract positive, negative and neutral scores too.




pepsi_posts = retrieve_posts(500, 'pepsi')

pepsi_avg = 0
for post in pepsi_posts:
    pepsi_avg += perform_sentiment_analysis(post)
pepsi_avg = pepsi_avg/len(pepsi_posts)

print("pepsi average is: ", pepsi_avg)