from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import storage
import pickle
import pandas as pd

# Configuration and initialization
app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "*"}})


# Google Cloud Storage setup
BUCKET_NAME = '007-model'
storage_client = storage.Client()

# Functions for data handling
def load_from_gcs(file_path):
    """Loads data from Google Cloud Storage."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_path)
    data = blob.download_as_bytes()
    return pickle.loads(data)

def recommend_anime(df, cosine_sim, user_history, N=20): # N is the number of recommendations
    """Generates anime recommendations based on user history."""
    user_anime_indices = _get_user_anime_indices(df, user_history)
    recommended_anime = _get_recommendations(df, cosine_sim, user_anime_indices, N*2) # Fetch twice the needed recommendations
    recommended_anime = _exclude_user_history(recommended_anime, user_history)
    return recommended_anime.head(N) # Return only top N recommendations

def _get_user_anime_indices(df, user_history):
    """Finds indices in the DataFrame corresponding to the user's anime history."""
    indices = []
    for title in user_history:
        matching_anime = df[(df['engName'].str.lower() == title.lower()) | 
                            (df['synonymsName'].str.contains(title, case=False, na=False))]
        if matching_anime.empty:
            print(f"Warning: Anime titled '{title}' not found in the dataset.")
        else:
            indices.append(matching_anime.index[0])
    return indices

def _get_recommendations(df, cosine_sim, indices, N):
    """Calculates and returns top N anime recommendations."""
    avg_sim_scores = cosine_sim[indices].mean(axis=0)
    max_score = df["score"].max()
    normalized_scores = df["score"].fillna(0) / max_score
    combined_scores = avg_sim_scores + normalized_scores
    top_indices = combined_scores.argsort()[-N*2-1:-1][::-1]  # Fetch twice the needed recommendations
    recommended = df.iloc[top_indices][['engName', 'score', 'url', 'genres', 'themes', 'producer', 'studios', 'allRank']]
    recommended['similarity_percentage'] = (avg_sim_scores[top_indices] * 100).tolist()

    # Remove duplicates based on the main title of 'engName'
    recommended['main_title'] = recommended['engName'].apply(lambda x: x.split(' ')[0])
    recommended.drop_duplicates(subset='main_title', keep='first', inplace=True)
    recommended.drop(columns='main_title', inplace=True)

    return recommended.head(N)  # Return only top N recommendations

def _exclude_user_history(recommended, user_history):
    """Excludes anime from the recommendations that are in the user's history."""
    for title in user_history:
        main_title = title.split(' ')[0]
        matching_indices = recommended[recommended['engName'].str.contains(main_title, case=False)].index
        recommended.drop(matching_indices, inplace=True)
    return recommended

# Data loading
df = pickle.load(open("anime_dataframe.pkl", "rb"))
cosine_sim = load_from_gcs("cosine_similarity_matrix.pkl")

# Route definitions
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    """Endpoint for fetching anime recommendations."""
    user_history = request.json.get('user_history', [])
    recommendations = recommend_anime(df, cosine_sim, user_history)
    result = [{"name": name, "score": score, "url": url, "genres": genres, "themes": themes, "producer": producer, "studios": studios, "allRank": allRank, "similarity_percentage": similarity_percentage}
              for name, score, url, genres, themes, producer, studios, allRank, similarity_percentage in recommendations.values]
    return jsonify(result)

@app.route('/version')
def version():
    return 'Version 2'

# Main application entry point
if __name__ == '__main__':
    app.run(debug=True, port=3000, ssl_context=('localhost.pem', 'localhost-key.pem'))
