## Sentiment Analysis of UK Supermarkets on Reddit

**Overview**

This project aims to analyse the sentiment of Reddit posts mentioning a specific company over time. Using the VADER sentiment analysis model, we will retrieve posts from Reddit, evaluate their sentiment, and visualize the changes in sentiment for the selected company.

**Key References**

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

**Retrieve Reddit Posts:**  

We utilize the Reddit API to fetch up to 100 posts for each supermarket and the general term "supermarket" as a baseline. A `.env` file is used to store authentication details (client ID and client secret) securely.
   
**Sentiment Analysis:**  

The Vader Sentiment Analyzer processes the textual data from the posts, returning a compound score for each. These sentiment scores are averaged for each supermarket and compared to the baseline sentiment for the term "supermarket."

**Data Manipulation:**  

A pandas DataFrame is used to store the sentiment scores and the number of posts used for analysis. The sentiment deviation from the baseline is computed and visualized using seaborn bar plots.

**Code Execution**

*Retrieving Posts*
```
def retrieve_posts(n, company):
    """
    Retrieves n Reddit posts mentioning the company.
    n should be an integer between 1 and 100.
    company should be a string with max 30 characters.
    """
```

*Sentiment Analysis*
```
def perform_sentiment_analysis(posts, company):
    """
    Performs sentiment analysis using Vader and returns average sentiment.
    """
```

*Data Manipulation*
```
df = pd.DataFrame(columns=['Supermarket', 'Sentiment', 'Deviation', 'n'])
```

*Visualisation*
```
plt.figure(figsize=(12,8))
sns.barplot(x='Supermarket', y='Deviation', data=df)
plt.show()
```

**Results**

The results reveal deviations in sentiment for each supermarket compared to the baseline. The sentiment data is visualized in two main graphs:

*Deviation from Baseline Sentiment:*

This chart shows how the sentiment for each supermarket compares to the average sentiment for the general term "supermarket." Supermarkets like Aldi and Lidl show positive deviations, suggesting they are viewed more favorably, while Tesco and Sainsbury demonstrate negative deviations.

*Sample Size for Each Supermarket:*

This chart shows the number of Reddit posts analyzed for each supermarket. It indicates how much data was available, which can influence the sentiment scores due to sample size variability.

**Results**

*Sentiment Deviation from Baseline*
The first plot visualizes how the sentiment for each supermarket deviates from the baseline sentiment of the general term "supermarket." A positive deviation suggests that the supermarket has a more favorable public sentiment compared to the overall sentiment for supermarkets, while a negative deviation suggests a less favorable sentiment.

Key Findings:
- Aldi, Lidl, and Iceland have positive sentiment deviations, indicating they are perceived more favorably than the average supermarket.
- Tesco has the most negative sentiment deviation, suggesting it is viewed less favorably compared to the baseline.
- ASDA and Sainsbury also exhibit slightly negative sentiment deviations, though not as pronounced as Tesco.

*Sample Size of Posts Analysed*
The second plot displays the number of Reddit posts analyzed for each supermarket. This is important to assess how representative the sentiment scores are, as supermarkets with a larger sample size might have more reliable sentiment data.

Key Findings:
- Tesco has the highest number of posts analyzed (around 100), which means its sentiment score is based on more data and may be more reliable.
- Lidl has the smallest sample size (around 70 posts), which means the sentiment score may be less reliable due to fewer data points.
- Most supermarkets have between 80 and 100 posts analyzed, giving a reasonable range of sentiment data across the dataset.

**Limitations**

- Reddit API Limitations:The Reddit API limits post retrieval to 100 per query, which constrains the data available for sentiment analysis. Additionally, the API does not support retrieving historical data, preventing analysis of sentiment trends over time.
- Query Relevance: The quality of the Reddit posts retrieved is variable. Some posts do not directly relate to the intended supermarket, reducing the effective dataset even further. This may skew results, as not all posts contribute meaningful sentiment.
- Data Granularity: Without the ability to fetch a larger number of posts or specify posts from a certain date range, the analysis lacks depth and historical context. This limits the accuracy of sentiment predictions over time.

**Lessons Learnt**

- Using APIs: I learned how to read API documentation, retrieve access tokens using OAuth, and handle requests to extract data from Reddit.
- Environment Management with `.env`: Using a `.env` file to securely store sensitive information, such as API keys, helped keep the project secure while maintaining functionality.
- Sentiment Analysis: I gained experience using the Vader SentimentIntensityAnalyzer to analyze social media posts and extract sentiment scores from text data.
- Data Manipulation: Working with pandas DataFrames to clean and manipulate data before visualizing it with seaborn has been a valuable experience in data analysis.
- Plotting Data: I learned to use matplotlib and seaborn to visualize data effectively, which is crucial for interpreting results and presenting findings.

**Potential Improvements and Future Work**

- Incorporating More Data: The project would benefit from accessing a larger dataset. This could be achieved by scraping multiple sources or finding a way to bypass the Reddit API's 100-post limit.
- Sentiment Over Time: A future improvement would involve plotting sentiment trends over time, giving insight into how public opinion of supermarkets changes over months or years. This would require API support for historical data, which is currently lacking.
- Query Refinement: Improving the relevance of posts by refining queries (e.g., by using advanced filtering or including/excluding certain subreddits) would enhance the quality of the dataset, ensuring the posts analyzed are truly relevant to the supermarket in question.
- Multilingual Sentiment Analysis: Expanding the project to analyze posts in multiple languages could make it more globally applicable, particularly for companies operating internationally.
- Advanced Sentiment Scoring: While Vader is effective, exploring other sentiment analysis libraries, such as TextBlob or transformer-based models like BERT, could lead to more nuanced and accurate sentiment analysis results.


**Setup**

1. Clone the repository.
2. Create a `.env` file with your Reddit API credentials:
3. Reddit API Credentials:
Create a Reddit application to get your CLIENT_ID and CLIENT_SECRET.
Store these credentials in a .env file:
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```
4. Install the necessary libraries using `pip`:
```
pip install requests pandas matplotlib seaborn vaderSentiment dotenv
```
5. Run the script and visualize the results!
