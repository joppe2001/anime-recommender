
# Anime Recommendation Service - Detailed Documentation

## Introduction

This document provides a detailed overview of the Flask-based web application designed for anime recommendations. It explains the functionality and the rationale behind various components and functions used in the application.

## Setup and Configuration

### Flask Application and CORS

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "https://localhost:3000"}})
```

The Flask application is set up with Cross-Origin Resource Sharing (CORS) to handle requests from a web frontend, specifically from `localhost:3000`.

## Google Cloud Storage Integration

### Configuration

```python
from google.cloud import storage

BUCKET_NAME = '007-model'
storage_client = storage.Client()
```

Google Cloud Storage is used for storing and retrieving large datasets like anime databases and similarity matrices. `storage.Client()` initializes the connection to the storage service.

## Data Handling Functions

### Load Data from GCS

```python
def load_from_gcs(file_path):
    """Loads data from Google Cloud Storage."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_path)
    data = blob.download_as_bytes()
    return pickle.loads(data)
```

This function downloads and deserializes data from Google Cloud Storage. `pickle.loads` is used to convert the byte stream back into a Python object.

### Anime Recommendation Logic

#### Core Recommendation Function

```python
def recommend_anime(df, cosine_sim, user_history, N=20):
    """Generates anime recommendations based on user history."""
    # ... function details ...
```

The `recommend_anime` function processes the user's anime history to provide personalized recommendations. It uses cosine similarity scores to find anime similar to those the user has already watched.

#### Helper Functions

1. **Finding User Anime Indices**

   Identifies the indices in the DataFrame corresponding to the anime titles in the user's history.

2. **Calculating Recommendations**

   - `cosine_sim[user_anime_indices].mean(axis=0)`: Computes the average cosine similarity scores for each anime in the database relative to the user's history.
   - `df["score"].fillna(0) / max_score`: Normalizes the anime scores to ensure they contribute appropriately to the final recommendation score.
   - `combined_scores.argsort()[-N-1:-1][::-1]`: Ranks the anime based on the combined scores and selects the top N recommendations. `argsort()` is used for sorting indices based on score.

3. **Excluding Anime from User's History**

   Removes any anime from the recommendations that the user has already watched, ensuring new recommendations.

## Flask Route Definitions

### Home Route

Simple route to confirm that the application is running.

### Recommendation Route

Endpoint for fetching anime recommendations based on user history. Uses the `recommend_anime` function.

### Version Route

A route to check the current version of the application.

## Main Application Entry Point

```python
if __name__ == '__main__':
    app.run(debug=True, port=3000, ssl_context=('localhost.pem', 'localhost-key.pem'))
```

The entry point for running the Flask application, with SSL context for HTTPS and port configuration.

