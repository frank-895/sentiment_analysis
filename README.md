## Sentiment Analysis of Company Mentions on Reddit

**Overview**

This project aims to analyse the sentiment of Reddit posts mentioning a specific company over time. Using the VADER sentiment analysis model, we will retrieve posts from Reddit, evaluate their sentiment, and visualize the changes in sentiment for the selected company.

**Key References**

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

**Libraries Used**

- Requests: For making HTTP requests to the Reddit API.
- VADER Sentiment Analysis: For performing sentiment analysis on the retrieved posts.
- Dotenv: For loading environment variables.

**Setup**

Install Required Libraries: You can install the required libraries using pip:
```pip install requests python-dotenv vaderSentiment```

Reddit API Credentials:
Create a Reddit application here to get your CLIENT_ID and CLIENT_SECRET.
Store these credentials in a .env file:

```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

**Code Structure**

Functions
get_headers(): Retrieves the necessary headers for accessing the Reddit API.
retrieve_posts(n, company, start_date, end_date): Fetches a specified number of Reddit posts mentioning a given company within a date range.
perform_sentiment_analysis(): Placeholder function to perform sentiment analysis. We use the normalized, weighted composite score called 'compound' to judge the sentiment of each post.
