from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import storage
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "https://recommending-ai.netlify.app"}})

# Initialize Google Cloud Storage client
storage_client = storage.Client()

BUCKET_NAME = '007-model'

print("Starting the updated version of the app...")


def load_from_gcs(file_path):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_path)
    data = blob.download_as_bytes()
    return pickle.loads(data)

df = pickle.load(open("anime_dataframe.pkl", "rb"))
cosine_sim = load_from_gcs("cosine_similarity_matrix.pkl")

# sdfhghjashghd
def recommend_anime(df, cosine_sim, user_history, N=10):
    user_anime_indices = []
    for title in user_history:
        matching_anime = df[(df['engName'].str.lower() == title.lower()) | (
            df['synonymsName'].str.contains(title, case=False, na=False))]
        if matching_anime.empty:
            print(f"Warning: Anime titled '{title}' not found in the dataset.")
        else:
            user_anime_indices.append(matching_anime.index[0])

    avg_sim_scores = cosine_sim[user_anime_indices].mean(axis=0)
    max_score = df["score"].max()
    normalized_scores = df["score"].fillna(0) / max_score
    combined_scores = avg_sim_scores + normalized_scores
    top_indices = combined_scores.argsort()[-N-1:-1][::-1]
    recommended_anime = df.iloc[top_indices][['engName', 'score', 'url', 'genres', 'themes', 'producer', 'studios']]

    for title in user_history:
        matching_indices = recommended_anime[recommended_anime['engName'].str.contains(
            title, case=False)].index
        if len(matching_indices) > 2:
            drop_indices = matching_indices[2:]
            recommended_anime.drop(drop_indices, inplace=True)
            
    return recommended_anime

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    # Get user history from POST request
    user_history = request.json.get('user_history', [])

    recommendations = recommend_anime(df, cosine_sim, user_history)
    result = [{"name": name, "score": score, "url": url, "genres": genres, "themes": themes, "producer": producer, "studios": studios}
              for name, score, url, genres, themes, producer, studios in recommendations.values]
    return jsonify(result)

@app.route('/version')
def version():
    return 'Version 2'


if __name__ == '__main__':
    app.run(debug=True, port=3000, ssl_context=('localhost.pem', 'localhost-key.pem'))