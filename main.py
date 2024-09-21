import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

def get_headers():
    """Retrieve Reddit API headers to access Reddit data."""
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Define the endpoint for access token
    url = "https://www.reddit.com/api/v1/access_token"

    # Create authentication using your client ID and secret
    auth = HTTPBasicAuth(client_id, client_secret)

    # Define the data for the request
    data = {
        'grant_type': 'client_credentials'
    }

    # Define headers
    headers = {
        'User-Agent': 'MyRedditApp/1.0 by Prestigious_Monk1227'  # Replace with a descriptive user agent
    }

    # Request the access token
    response = requests.post(url, auth=auth, data=data, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        token = response.json().get('access_token')

        # Use the token to make requests
        headers['Authorization'] = f'bearer {token}'
        return headers
    else:
        raise Exception("Failed to access redit API")      

# Define variables
url = f"https://oauth.reddit.com/search"
params = {
    'q': "Facebook",
    'limit': 10
}
headers = get_headers()

response = requests.get(url, headers=headers, params=params).json()

for post in response['data']['children']: # returns info about each post requested
    print(post['data']['title'],'\n')
    print(post['data']['selftext'],'\n')
    print("***********************")
