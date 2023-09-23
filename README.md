# Movie Recommendation System
![image](https://github.com/MagnusS0/movie-rec-system/assets/97634880/39e354c0-41cb-4318-a4e2-ab26b7a9bd86)


This is a Python project to build a movie recommendation system using data extracted from a movie database API. <br>
The project follows the guided blueprint provided by [Ploomber](https://github.com/ploomber/sql/tree/main), focusing on writing professional, modular, and well-documented code with thorough docstrings and exception handling within an OOP framework.

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [How to Run it](#how-to-run-it-)
    - [With Docker](#run---with-docker-)
    - [Locally](#run---locally-)
- [Data](#data-)
- [Recommendation Methodology](#recommendation-methodology-)
- [Modules](#modules)
- [Results](#results)
- [Credits](#credits-)
- [License](#license-)

## Description
The project involves the following components:

- 🎬 Extracting movie data by calling [TheMovieDB API](https://developer.themoviedb.org/docs/getting-started)
- 💾 Storing the data in a DuckDB database 
- 📊 Performing exploratory data analysis with SQL in Jupyter Notebooks 
- 🤖 Developing a movie recommendation system that uses TF-IDF and cosine similarity to generate reccomendations 
- 🎞️ Takes a movie title as input and returns similar movie recommendations 
- ⚙️ Packaging the notebooks and Python scripts into an end-to-end workflow using Ploomber 
- ⚡ Building a FastAPI web application to serve the recommendation results via API 
- 🐳 Dockerizing the application for easy deployment 

## Requirements
- Python 3.10+ 🐍
- Poetry 📦
- DuckDB 🦆
- Jupyter 💻
- Pandas 🐼
- Scikit-Learn 🔬
- FastAPI ⚡️
- Docker 🐳
> See the [`pyproject.toml`](pyproject.toml) file for the full list of dependencies.

## How to Run it 🛫
<details open>
  <summary>Click me</summary>

Clone the repository
```sh
git clone https://github.com/MagnusS0/movie-rec-system.git
```
Navigate to the directory where you downloaded the repository
``` sh
cd movie_rec_system
```

### Run - with Docker 🐳

```sh
docker build --build-arg API_KEY=your_api_key -t movie_rec_system:latest -f Dockerfile .
docker run -e API_KEY=your_api_key -p 8000:8000 movie_rec_system:latest
```

### Run - locally 💻
> Remember to add your own API key to .env
1. Make sure you have `Poetry` innstalled in your enviornment
```sh
pip install poetry
```
2. Install dependencies
```sh
poetry lock
poetry install
```
3. Build the pipline with `Ploomber` build
```sh
poetry run ploomber build
```
4. Run the app (make sure you are in the right dir)
```sh
 uvicorn app.app:app
```
</details>

## Data 📊
The data is extracted from TheMovieDB API and stored in a DuckDB database movies_data.duckdb. It contains information on movies like title, overview, genres, ratings, etc.

The main tables are:

- **movies** - contains movie info
- **genres** - contains genre definitions
- **movie_genre_data** - joins movies and genres into a single table

## Recommendation Methodology 🤖

The movie recommendation system is built using TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity. Essentily building a **content filtering** reccomendation system. <br>
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
## Credits 👏
This project was created by [@MagnusS0](https://github.com/MagnusS0)

**Guided by:**
[Ploomber's Movie Recommendation Project](https://ploomber-sql.readthedocs.io/en/latest/mini-projects/recommendation-system/introduction.html)

**Powered by:**

[TheMovieDB API](https://www.themoviedb.org/) <br>
[Ploomber](https://ploomber.io/) <br>
[FastAPI](https://fastapi.tiangolo.com/) <br>
[DuckDB](https://duckdb.org/) <br>
[Poetry](https://python-poetry.org/) <br>
[Docker](https://www.docker.com/) 

## License 📄
This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

I have modified the original code/structure from Ploomber's blueprint, while keeping some parts the same. Thank you to Ploomber for making their blueprint openly available!
