# + tags=["parameters"]
# declare a list tasks whose products you want to use as inputs
upstream = None

# -

import requests
from dotenv import load_dotenv
import json
import tempfile
import duckdb
import os
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)


def extract_movies(api_key=None, lang='en', num_movies=100, conn=None, drop=False):
    """
    Extracts movies from TheMovieDB API and populates the DuckDB database.

    Args:
        api_key (str): The API key for accessing TheMovieDB.
        lang (str, optional): The language code for movie data. Defaults to 'en'.
        num_movies (int, optional): The number of movies to extract. Defaults to 100.
        conn: The DuckDB connection object.
        drop (bool, optional): Whether to drop the existing table before insertion. Defaults to False.

    Returns:
        None
    """
    movies = 0
    page = 1

    # Drop table if drop = True
    drop_table(conn, drop=drop, table_name='movies')

    while movies < num_movies:
        # Update the URL with the new page number
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&with_original_language={lang}&page={page}"

        # Make a request
        try:
            res = requests.get(url)
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred during the request: {e}")
            break

        if res.status_code != 200:
            logging.error(f"Received non-200 status code: {res.status_code}")
            break

        # Transform content to JSON
        json_data = res.json()

        # Initialize or update the database
        init_duck_db_movies(conn, json_data, table_name='movies')

        # Log progress
        movies += len(json_data.get('results', []))
        logging.info(f"Extracted {movies} out of {num_movies} movies.")

        page += 1


def extract_genre(api_key=None, lang='en', drop=False, conn=None):
    """
    Extracts movie genres from TheMovieDB API and returns the data as a JSON object.

    Args:
        api_key (str): The API key for accessing TheMovieDB.
        lang (str, optional): The language code for genre data. Defaults to 'en'.
        conn: The DuckDB connection object.

    Returns:
        dict: A JSON object containing the API response.
    """
    # Drop table if drop = True
    drop_table(conn, drop=drop, table_name='genres')

    # Construct URL
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&with_original_language={lang}"  # noqa E501
    # Make a request
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred during the request:", e)
        return {}

    # Transform content to JSON
    json_data = res.json()

    # Initialize or update the database
    init_duck_db_genres(conn, json_data, table_name='genres')



def drop_table(conn, drop=False, table_name=None):
    '''
    Drops table in DuckDB if it does exist

    Args:
        conn: The DuckDB connection object.
        table_name (str): The name of the table to create or update.
        drop (bool, optional): Whether to drop the table if it already exists. Defaults to False.

    Returns:
        None
    '''
    # If drop flag is True, drop the existing table
    if drop:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        logging.info(f'Sucessfully dropped {table_name}')


def write_json_to_temp_file(json_data, json_key):
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
            # Get the correct key so that only the results are written to the file
            json.dump(json_data[f'{json_key}'], temp_file) 
            return temp_file.name
    except Exception as e:
        logging.error(f"An error occurred while writing the JSON file: {e}")
        return None


def create_table(conn, table_name, temp_file_path):
    """
    Creates a new table in DuckDB if it does not already exist, or inserts data into an existing table.
    Optionally drops the table if it already exists.

    Args:
        conn: The DuckDB connection object.
        table_name (str): The name of the table to create or update.
        temp_file_path (str): The path to the temporary file containing the JSON data to populate the table.

    Returns:
        None
    """
    # If table do NOT exists create a new one, else insert data
    try:
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


def init_duck_db_movies(conn, json_data=None, table_name='movies'):
    '''
    Initilizes the 'movies' table and populates it with JSON data

    Args:
        conn : The DuckDB connection object.
        json_data (dict, optional) : The JSON data to populate the table with. If None, data will be extracted
        using the extract_movies function. Defaults to None. 
        table_name (str, optional): The name of the table to initialize. Defaults to 'movies'.

    Returns:
        None
    '''

    # Write JSON string to a temporary file
    if json_data:
        temp_file_path = write_json_to_temp_file(json_data, json_key='results')

        # If table do NOT exists create a new one, else insert data
        if temp_file_path:
            create_table(conn, table_name, temp_file_path)
            os.remove(temp_file_path)
            logging.info(
                f"Successfully initialized and populated the table {table_name}.")


def init_duck_db_genres(conn, json_data=None, table_name='genres'):
    '''
    Initilizes the 'genres' table and populates it with JSON data

    Args:
        conn : The DuckDB connection object.
        path (str, optional) : The path to the DuckDB file. Defaults to "movies_data.duckdb".
        json_data (dict, optional) : The JSON data to populate the table with. If None, data will be extracted
        table_name (str, optional): The name of the table to initialize. Defaults to 'genres'.

    Returns:
        None
    '''

    # Write JSON string to a temporary file
    if json_data:
        temp_file_path = write_json_to_temp_file(json_data, json_key='genres')

        # If table do NOT exists create a new one, else insert data
        if temp_file_path:
            create_table(conn, table_name, temp_file_path)
            os.remove(temp_file_path)
            logging.info(
                f"Successfully initialized and populated the table {table_name}.")


if __name__ == "__main__":
    # Parameter to get 1000 English movies
    language_count = {"en": 1000,}

    # Load API key from .env file
    load_dotenv(".env")
    api_key = os.getenv('API_KEY')

    conn = None

    # Initialize connection path
    duckdb_file_path = "movies_data.duckdb"
    try:
        conn = duckdb.connect(duckdb_file_path, read_only=False)
        logging.info('Connection opened')
        
        for key in language_count:
        # print(key,language_count[key])
            print("Downloading", key, end=": ")
            movies = extract_movies(api_key, key, language_count[key],conn,drop=True)  # noqa E501
            genres = extract_genre(api_key, key,drop=True, conn=conn)

    except Exception as e:
        logging.error(f'An error occurred: {e}')

    finally:
        if conn:
            conn.close()
            logging.info('Connection closed')
