import json
import logging
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


from movie_rec_system.app.recommenderhelper import (
    content_movie_recommender,
    compute_metrics,
    retrieve_and_transform_data,
    compute_tfidf_vectorization,
)

def get_recommendation(movie: str, num_rec: int = 10, stop_words="english"):
    """
    Generate movie recommendations based on
    content similarity and computes associated metrics.

    This function retrieves movie data,
    calculates cosine similarity between movies using
    TF-IDF vectorization of their combined overview
    and genre, and returns a list of recommended
    movies along with certain metrics
    (popularity, vote average, and vote count RMSE).

    Parameters
    ----------
    movie : str
        The title of the movie for which
        recommendations are to be generated.

    num_rec : int, optional
        The number of movie recommendations
        to generate. Default is 10.

    stop_words : str, optional
        The language of stop words to be
        used when vectorizing the "combined" column.
        Default is "english".

    Returns
    -------
    str
        A JSON-formatted string containing
        the original movie, a list of recommendations,
        and associated metrics
        (popularity, vote average, and vote count RMSE).

    Examples
    --------
    >>> result = get_recommendation("Inception", num_rec=5)
    >>> print(json.loads(result))
    {
        "movie": "Inception",
        "recommendations": [...],
        "metrics": {
            "popularity": ...,
            "vote_avg": ...,
            "vote_count": ...
        }
    }

    """
    # Assertions to check input types and values
    assert isinstance(movie, str), 'movie must be a string'
    assert num_rec > 0, 'num_rec must be greater than 0'
    

    movie = movie.lower()
    df = retrieve_and_transform_data()

    tfidf_matrix = compute_tfidf_vectorization(df, stop_words)
    similarity = cosine_similarity(tfidf_matrix)


    similarity_df = pd.DataFrame(
        similarity, index=df.title.values, columns=df.title.values # type: ignore
    )
    movie_list = similarity_df.columns.values
    recommendations = content_movie_recommender(
        movie, similarity_df, movie_list, num_rec # type: ignore
    )

    if not recommendations:
        return None

    popularity_rmse, vote_avg_rmse, vote_count_rmse = compute_metrics(
        df, movie, recommendations
    )

    result = {
        "movie": movie,
        "recommendations": recommendations,
        "metrics": {
            "popularity": popularity_rmse,
            "vote_avg": vote_avg_rmse,
            "vote_count": vote_count_rmse,
        },
    }

    result_json = json.dumps(result)
    return result_json