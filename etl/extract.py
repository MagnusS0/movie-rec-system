import requests
from dotenv import load_dotenv
import duckdb
import os

# Load API key from .env file
load_dotenv(".env")
api_key = os.getenv('API_KEY')


def extract_movies (api_key = api_key, lang = 'en'):
    """
    Extracts movies from TheMovieDB API and returns the data as a JSON object.

    Args:
        api_key (str): The API key for accessing TheMovieDB.
        lang (str, optional): The language code for movie data. Defaults to 'en'.

    Returns:
        dict: A JSON object containing the API response.
    """
    # Construct URL
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&with_original_language={lang}" # noqa E501
    # Make a request
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
        return {}
    # Transform content to JSON
    return res.json()



def extract_genre (api_key = api_key, lang = 'en'):
    """
    Extracts movie genres from TheMovieDB API and returns the data as a JSON object.

    Args:
        api_key (str): The API key for accessing TheMovieDB.
        lang (str, optional): The language code for genre data. Defaults to 'en'.

    Returns:
        dict: A JSON object containing the API response.
    """
    # Construct URL
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&with_original_language={lang}"  # noqa E501
    # Make a request
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
        return {}
    # Transform content to JSON
    return res.json()

