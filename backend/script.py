from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import storage
import pickle

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
    popularity_factor = df["members"].fillna(0) / df["members"].max()
    
    combined_scores = avg_sim_scores + normalized_scores + popularity_factor
    top_indices = combined_scores.argsort()[-N*2:][::-1]  # Fetching more indices to filter out already watched anime
    
    recommended_anime = df.iloc[top_indices][
        ['engName', 'score', 'url', 'genres']
    ]

    # Remove anime already seen by the user
    for title in user_history:
        matching_indices = recommended_anime[recommended_anime['engName'].str.contains(
            title, case=False)].index
        recommended_anime.drop(matching_indices, inplace=True)

    return recommended_anime.head(N)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    # Get user history from POST request
    user_history = request.json.get('user_history', [])

    recommendations = recommend_anime(df, cosine_sim, user_history)
    result = [{"name": name, "score": score, "url": url, "genres": genres}
              for name, score, url, genres in recommendations.values]
    return jsonify(result)

@app.route('/version')
def version():
    return 'Version 2'


if __name__ == '__main__':
    app.run(debug=True, port=3000, ssl_context=('localhost.pem', 'localhost-key.pem'))