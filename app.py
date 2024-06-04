'''

Problem Statement
You are asked to design and develop a small microservice application offering a RESTful API that identifies if comments on a given subfeddit or category are positive or negative.

Given the name of a subfeddit the application should return:
A list of the most recent comments. Suppose a limit of 25 comments.
For each comment:
The unique identifier of the comment
The text of the comment
The polarity score and the classification of the comment (positive, or negative) based on that score.

Optionally, you should allow the user to modify the query as follows:
Filter comments by a specific time range 
Sort the results by the comments polarity score.
Define a GitHub workflow to run linting checks and tests for the built RESTful API

'''

# Author: Prashant Singh
# Date: 4th June, 2024

import requests
from textblob import TextBlob 


def get_api_response_requests(url):
    '''
    Function to accept a url and returns a response in JSON format

    '''

    try:
        # make the GET request
        response = requests.get(url)
        
        # Raise an HTTPError for bad responses
        response.raise_for_status()
        
        # Parse the response as JSON
        response_json = response.json()
        return response_json
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def analyze_sentiment(text):
    # Create a textblob object
    blob = TextBlob(text)
    
    # Get the polarity score
    polarity = blob.sentiment.polarity
    
    # Classify the sentiment as positive or negative
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return polarity, sentiment

# URLs
url_subfeddit_names = "http://localhost:8080/api/v1/subfeddits/?skip=0&limit=10"
url_subfeddit_comments = "http://localhost:8080/api/v1/comments/?subfeddit_id=3&skip=0&limit=10"


response_subfeddit_names = get_api_response_requests(url_subfeddit_names)
response_subfeddit_comments = get_api_response_requests(url_subfeddit_comments)
# print(response_subfeddit_names)
# print('\n')
# print(response_subfeddit_comments)

# Access the list of subfeddits
subfeddits = response_subfeddit_names['subfeddits']
# Extract usernames and ids using list comprehension
usernames = [subfeddit['username'] for subfeddit in subfeddits]
ids = [subfeddit['id'] for subfeddit in subfeddits] 
# Print the extracted usernames
print(usernames)
print(ids)

# Sort the 'comments' list to extract the recent comments 
response_subfeddit_comments['comments'].sort(key=lambda comment: comment['created_at'], reverse=True)
print('\n')
#print(response_subfeddit_comments)
comments  = response_subfeddit_comments['comments'] 
recent_comment_text = [comment_text['text'] for comment_text in comments]
recent_comment_id = [comment_id['id'] for comment_id in comments]

comment  = recent_comment_text[0]
polarity_scores = []
sentiment_vals = []
for comment in recent_comment_text:
    polarity, sentiment = analyze_sentiment(comment)
    polarity_scores.append(polarity)
    sentiment_vals.append(sentiment)


final_results = []
for comment, comment_id, polarity_score, sentiment_val in zip(recent_comment_text,recent_comment_id, polarity_scores, sentiment_vals):
    vals_dict = {"Unique_identifier_of_comment": comment_id,
                 "text_comment": comment,
                 "polarity_score":polarity_score,
                 "sentiment_class": sentiment_val
                }
    final_results.append(vals_dict)

print(recent_comment_text)           
print("Final Results:\n\n", final_results) 

    


