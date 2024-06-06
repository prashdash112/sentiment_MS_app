'''

Problem Statement
You are asked to design and develop a small microservice application offering a 
RESTful API that identifies if comments on a given subfeddit or category are positive or negative.

Given the name of a subfeddit the application should return:
A list of the most recent comments. Suppose a limit of 25 comments.
For each comment:
The unique identifier of the comment
The text of the comment

The polarity score and the classification of the comment (positive, or negative) based on 
that score.

Optionally, you should allow the user to modify the query as follows:
Filter comments by a specific time range 
Sort the results by the comments polarity score.
Define a GitHub workflow to run linting checks and tests for the built RESTful API

'''

# Author: Prashant Singh
# Date: 5th June, 2024

import datetime
import requests
from textblob import TextBlob
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_api_response_requests(url):

    '''
    
    Function to accept a url and returns a response in JSON format
    
    Args: url (str)
    
    Returns: JSON object

    '''

    try:
        response = requests.get(url,timeout=20)
        # Raise an HTTPError for bad responses
        response.raise_for_status()
        # Parse the response as JSON
        response_json = response.json()

        return response_json

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def analyze_sentiment(text):

    '''

    Function to analyze the sentiment of the text using textblob library

    Args: text (str) 
    
    Returns: float, string

    '''

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

# Function to convert Unix timestamp to 'YYYYMMDD' format
def convert_timestamp_to_text(timestamp):

    '''
    
    Function converts a unix timestamp into a datetime object with format: YYYY-MM-DD
    
    Args: Timestamp object
    
    Returns: Timestamp object

    '''

    date_time = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    formatted_date = date_time.strftime('%Y%m%d')
    return formatted_date

#URL
url_subfeddit_names = "http://localhost:8080/api/v1/subfeddits/?skip=0"
response_subfeddit_names = get_api_response_requests(url_subfeddit_names)

# Access the list of subfeddits
subfeddits = response_subfeddit_names['subfeddits']
# Mapping subfeddit names to ids:
usernames = [subfeddit['username'] for subfeddit in subfeddits]
ids = {subfeddit["username"]:subfeddit['id'] for subfeddit in subfeddits }


@app.route("/polarity/<subfeddit>",methods=['GET'])
def polarity_scores(subfeddit):

    '''

    Retrieve and analyze the sentiment of comments from a specified subfeddit.

    This endpoint fetches comments from a subfeddit, analyzes their sentiment,
    and returns the comments along with their sentiment scores and metadata.

    Args:
        subfeddit (str): The identifier of the subfeddit to analyze.

    Query Parameters:
        sort (str, optional): The order to sort the results by polarity score. 
                              Use any number for ascending and 'desc' for descending.

        limit (int, optional): The maximum number of comments to return.

        date_range (str, optional): The date range to filter comments in the format 'YYYYMMDD,YYYYMMDD'.

    Returns:
        Response: A JSON response containing a list of comments with their UID, text, polarity score,
                  sentiment classification, and creation date.
    
    '''

    # URL
    url_subfeddit_comments = f"http://localhost:8080/api/v1/comments/?subfeddit_id={ids[subfeddit]}&skip=0&limit=22000"
    response_subfeddit_comments = get_api_response_requests(url_subfeddit_comments)

    # Creating querry parameters for the comments
    sort = request.args.get("sort")
    limit = request.args.get("limit")
    date_range = request.args.get('date_range', '')

    # Sort the 'comments' list to extract the recent comments
    response_subfeddit_comments['comments'].sort(key=lambda comment: comment['created_at'], reverse=True)

    comments  = response_subfeddit_comments['comments']
    recent_comment_text = [comment_text['text'] for comment_text in comments]
    recent_comment_id = [comment_id['id'] for comment_id in comments]
    created_at_comment = [comment_created['created_at'] for comment_created in comments]
    formatted_date = [convert_timestamp_to_text(timestamp) for timestamp in created_at_comment]

    polarity_scores = []
    sentiment_vals = []
    for comment in recent_comment_text:
        polarity, sentiment = analyze_sentiment(comment)
        polarity_scores.append(polarity)
        sentiment_vals.append(sentiment)

    final_results = []
    for comment, comment_id, polarity_score, sentiment_val, date in zip(recent_comment_text,recent_comment_id,polarity_scores, sentiment_vals,formatted_date):
        vals_dict = {"UID_comment": comment_id,
                    "text_comment": comment,
                    "polarity_score":polarity_score,
                    "sentiment_class": sentiment_val,
                    "date": date
                    }
        final_results.append(vals_dict)

    # Slicing the comments data using the date range
    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(',')
            print("Dates string:",start_date_str,end_date_str)
            final_results = [item for item in final_results if start_date_str <= item['date'] <= end_date_str]
        except ValueError:
            return jsonify({'error': 'Invalid date_range format. Use YYYYMMDD,YYYYMMDD format'}), 400

    if limit:
        final_results = final_results[:int(limit)]
    if sort:
        final_results.sort(key = lambda item: item["polarity_score"], reverse = sort=="desc")

    # Print the extracted ids and final results on terminal
    print(ids)
    print('\n')
    print("Final Results:\n\n", final_results)

    return jsonify(final_results)

if __name__ == "__main__":
    app.run(debug=True)