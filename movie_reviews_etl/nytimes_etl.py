import pandas as pd
import requests
from datetime import datetime
import json
import os
import s3fs

def load_config():
    # Load configuration data from a JSON file
    with open('config.json') as f:  # Open the config.json file
        return json.load(f)  # Parse and return the JSON data as a dictionary

def run_nytimes_etl():
    # Main function to run the ETL process

    config = load_config()  # Load the configuration data
    api_key = config['NYT_API_KEY']  # Retrieve the API key from the config
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'  # Base URL for the NYT API

    # Parameters for the API request
    params = {
        'api-key': api_key,  # Include the API key
        'fq': 'section_name: ("Movies") AND type_of_material:("Review")',  # Filter for movie reviews
    }

    # Make the GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
    else:
        print(f"Error: {response.status_code}")  # Print error message if the request failed

    movies_list = []  # Initialize an empty list to store movie data

    # Data is the parsed JSON response
    articles = data['response']['docs']  # Extract articles from the response
    print(f"Number of articles retrieved: {len(articles)}")  # Print the number of retrieved articles (for debugging)

    # Loop through each article and extract relevant information
    for article in articles:
        refined_movies = {
            "title": article.get('headline', {}).get('main', 'No Title'),  # Get the title, default to 'No Title'
            "abstract": article.get('abstract', 'No Abstract'),  # Get the abstract, default to 'No Abstract'
            "web_url": article.get('web_url', 'No URL'),  # Get the article URL, default to 'No URL'
            "snippet": article.get('snippet', 'No Snippet'),  # Get the snippet, default to 'No Snippet'
            "lead_paragraph": article.get('lead_paragraph', 'No Lead Paragraph'),  # Get the lead paragraph, default to 'No Lead Paragraph'
            "print_section": article.get('print_section', 'No Section')  # Get the print section, default to 'No Section'
        }
        
        movies_list.append(refined_movies)  # Append the refined movie data to the list

    # Create a DataFrame from the movies_list
    df = pd.DataFrame(movies_list)

    # Get current date and format it as YYYY-MM-DD
    today = datetime.today().strftime('%Y-%m-%d')  

    # Define the S3 path where the CSV will be saved
    s3_path = f's3://xxxxxxxxxxxx/xxxxxxxxxxxxxxxxx/movies_reviews_{today}.csv'

    # Attempt to save the DataFrame as a CSV file in the specified S3 path
    try:
        df.to_csv(s3_path)  # Write the DataFrame to a CSV file
        print("CSV file created successfully.")  # Print success message
    except Exception as e:
        print(f"Error creating CSV file: {e}")  # Print error message if the file creation fails
