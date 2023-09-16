import requests
from dotenv import load_dotenv
import json
import tempfile
import duckdb
import os
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)


# Load API key from .env file
load_dotenv(".env")
api_key = os.getenv('API_KEY')


def extract_movies(api_key=api_key, lang='en'):
    """
    Extracts movies from TheMovieDB API and returns the data as a JSON object.

    Args:
        api_key (str): The API key for accessing TheMovieDB.
        lang (str, optional): The language code for movie data. Defaults to 'en'.

    Returns:
        dict: A JSON object containing the API response.
    """
    # Construct URL
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&with_original_language={lang}"  # noqa E501
    # Make a request
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred during the request:", e)
        return {}
    # Transform content to JSON
    return res.json()


def extract_genre(api_key=api_key, lang='en'):
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
        logging.error("An error occurred during the request:", e)
        return {}
    # Transform content to JSON
    return res.json()


# Initialize connection path
duckdb_file_path = "movies_data.duckdb"
conn = duckdb.connect(duckdb_file_path, read_only=False)


def write_json_to_temp_file(json_data):
    """
    Writes the provided JSON data to a temporary file and returns the file's name.

    Args:
        json_data (dict): The JSON data to write to the file.

    Returns:
        str: The name of the temporary file containing the JSON data, or None if an error occurs.
    """
    # Write JSON string to a temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            json.dump(json_data, temp_file)
            return temp_file.name
    except Exception as e:
        logging.error(f"An error occurred while writing the JSON file: {e}")
        return None


def create_table(conn, table_name, temp_file_path, drop=False):
    """
    Creates a new table in DuckDB if it does not already exist, or inserts data into an existing table.
    Optionally drops the table if it already exists.

    Args:
        conn: The DuckDB connection object.
        table_name (str): The name of the table to create or update.
        temp_file_path (str): The path to the temporary file containing the JSON data to populate the table.
        drop (bool, optional): Whether to drop the table if it already exists. Defaults to False.

    Returns:
        None
    """
    # If table do NOT exists create a new one, else insert data
    try:

        if drop:
            conn.execute(f'DROP TABLE IF EXISTS {table_name}')

        tables = conn.execute("SHOW TABLES;").fetchall()

        if (f"{table_name}",) not in tables:
            conn.execute(
                f"CREATE TABLE {table_name} AS SELECT * FROM read_json_auto('{temp_file_path}')")
        else:
            conn.execute(
                f"INSERT INTO {table_name} SELECT * FROM read_json_auto('{temp_file_path}')")
    except Exception as e:
        logging.error(f"An error occurred while creating the table: {e}")
        return


def init_duck_db_movies(conn=conn, json_data=None, table_name='movies', drop=False):
    '''
    Initilizes the 'movies' table and populates it with JSON data

    Args:
        conn : The DuckDB connection object.
        json_data (dict, optional) : The JSON data to populate the table with. If None, data will be extracted
        using the extract_movies function. Defaults to None. 
        table_name (str, optional): The name of the table to initialize. Defaults to 'movies'.
        drop (bool, optional): Whether to drop the table if it already exists. Defaults to False.

    Returns:
        None
    '''
    # Extract movies data
    if json_data is None:
        json_data = extract_movies()

    # Write JSON string to a temporary file
    if json_data:
        temp_file_path = write_json_to_temp_file(json_data)

        # If table do NOT exists create a new one, else insert data
        if temp_file_path:
            create_table(conn, table_name, temp_file_path, drop)
            conn.close()
            os.remove(temp_file_path)
            logging.info(
                f"Successfully initialized and populated the table {table_name}.")


def init_duck_db_genres(conn=conn, json_data=None, table_name='genres', drop=False):
    '''
    Initilizes the 'genres' table and populates it with JSON data

    Args:
        conn : The DuckDB connection object.
        path (str, optional) : The path to the DuckDB file. Defaults to "movies_data.duckdb".
        json_data (dict, optional) : The JSON data to populate the table with. If None, data will be extracted
        table_name (str, optional): The name of the table to initialize. Defaults to 'genres'.
        drop (bool, optional): Whether to drop the table if it already exists. Defaults to False.

    Returns:
        None
    '''
    # Extract genre data
    if json_data is None:
        json_data = extract_genre()

    # Write JSON string to a temporary file
    if json_data:
        temp_file_path = write_json_to_temp_file(json_data)

        # If table do NOT exists create a new one, else insert data
        if temp_file_path:
            create_table(conn, table_name, temp_file_path, drop)
            conn.close()
            os.remove(temp_file_path)
            logging.info(
                f"Successfully initialized and populated the table {table_name}.")
