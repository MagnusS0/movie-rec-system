# Movie Recommendation System
This is a Python project to build a movie recommendation system using data extracted from a movie database API. <br>
The project follows the guided blueprint provided by [Ploomber](https://github.com/ploomber/sql/tree/main), focusing on writing professional, modular, and well-documented code with thorough docstrings and exception handling within an OOP framework.
## Description
The project involves the following components:

- Extracting movie data by calling [TheMovieDB API](https://developer.themoviedb.org/docs/getting-started)
- Storing the data in a DuckDB database
- Performing exploratory data analysis with SQL in Jupyter Notebooks
- Developing a movie recommendation system that uses TF-IDF and cosine similarity to generate reccomendations
- Takes a movie title as input and returns similar movie recommendations
- Packaging the notebooks and Python scripts into an end-to-end workflow using Ploomber
- Building a FastAPI web application to serve the recommendation results via API
- Dockerizing the application for easy deployment

## Requirements
- Python 3.10+
- Poetry
- DuckDB
- Jupyter
- Pandas
- Scikit-Learn
- FastAPI
- Docker
> See the `pyproject.toml` file for the full list of dependencies.

## Data
The data is extracted from TheMovieDB API and stored in a DuckDB database movies_data.duckdb. It contains information on movies like title, overview, genres, ratings, etc.

The main tables are:

- **movies** - contains movie info
- **genres** - contains genre definitions
- **movie_genre_data** - joins movies and genres into a single table

## Recommendation Methodology

The movie recommendation system is built using TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity. <br>
TF-IDF is used to convert the movie `(overviews+ (genres*2))` into numerical vectors, representing the significance of specific terms in each movie’s overview. 
Then, cosine similarity is computed between these vectors to determine the similarity between different movies. 
Based on this similarity score, the system recommends movies that are most similar to the given input movie title.

## Modules
- `app/app.py` - contains the FastAPI application code
- `app/recommender.py` - generates movie recommendations
- `app/recommenderhelper.py` - contains helper functions for the recommender
- `etl/extract.py` - extracts data from API
- `etl/eda.ipynb` - notebook for exploratory data analysis
- `products/` - contains notebooks packaged by Ploomber
- `tests/` - contains tests for the application

## Results
Running the application provides movie recommendations in JSON format for a given movie title. It also returns metrics on the popularity, ratings, and vote count of the recommendations.

Sample Output:
```json
{
  "movie": "oppenheimer",
  "recommendations": [
    "schindler's list",
    "resistance",
    "to end all war: oppenheimer & the atomic bomb",
    "midway",
    "1917",
    "emancipation",
    "13 hours: the secret soldiers of benghazi",
    "defiance",
    "the imitation game",
    "hacksaw ridge"
  ],
  "metrics": {
    "popularity": 373.829,
    "vote_avg": 0.834,
    "vote_count": 6699.44
  }
}
```

## Usage
To run the project locally:

1. Clone the repository
```
git clone https://github.com/MagnusS0/movie-rec-system.git
```
2. Navigate to the directory where you downloaded the repository
``` bash
cd movie_rec_system
```
3. Make sure you have `Poetry` innstalled in your enviornment
```
pip install poetry
```
4. Install dependencies
```
poetry install
```
5. Build the pipline with `Ploomber` build
```
ploomber build
```
6. Run the app (make sure you are in the right dir)
```
 uvicorn app.app:app
```
