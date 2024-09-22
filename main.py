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
    """Performs sentiment analysis on each post in posts, and returns the average"""
    
    analyser = SentimentIntensityAnalyzer() # create analyser instance
    
    avg = 0 # track sentiment scores
    failed = 0
    for post in posts: # find sentiment for each posts
        if (company.lower() in post.lower()):
            sentiment = analyser.polarity_scores(post)
            avg += sentiment['compound'] # compound is overall sentiment between -1 and 1. *note - possible to extract positive, negative and neutral scores too.
        else:
            failed += 1
    print('total failed for', company, ': ', failed)
    print('total checked for', company, ': ', len(posts))
    return avg/len(posts) # return average sentiment

def read_companies():
    """Reads in company names for sentiment analysis from text file  labbeled companies.txt"""
    companies = 'companies.txt' # contains companies to analyse
    with open(companies) as file:
        company_list = file.readlines() # returns array
    clean_company_list = []
    for company in company_list:
        clean_company_list.append(company.strip()) # remove newlines and extra spaces
    return clean_company_list

companies = read_companies() # array of companies to analyse

no_to_analyse = 100
company_sentiments = {}
for company in companies:
    posts = retrieve_posts(no_to_analyse, company)
    company_sentiments[company] = perform_sentiment_analysis(posts, company)

# find baseline sentiment for word 'supermarket'
posts = retrieve_posts(no_to_analyse, 'supermarket')
baseline_sentiment = perform_sentiment_analysis(posts, 'supermarket')

print("Baseline sentiment: ", baseline_sentiment)
print(company_sentiments)