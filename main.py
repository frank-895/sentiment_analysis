import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

def retrieve_posts(n, company, start_date, end_date):
    # Define variables
    url = "https://oauth.reddit.com/search"
    params = {
        'q': company,
        'limit': n,
        'since': start_date,
        'until': end_date
    }
    headers = get_headers()

    # request from reddit API
    response = requests.get(url, headers=headers, params=params).json()

    post_info = []
    for post in response['data']['children']: # returns info about each post requested
        post_info.append(post['data']['title'] + post['data']['selftext'])
    return post_info

def perform_sentiment_analysis():
    pass

posts_2023 = retrieve_posts(10, 'pepsi', '2023-01-01','2024-01-01')
posts_2022 = retrieve_posts(10, 'pepsi', '2022-01-01','2023-01-01')

analyser = SentimentIntensityAnalyzer() # create analyser instance
for post in posts_2023:
    print(analyser.polarity_scores(post))