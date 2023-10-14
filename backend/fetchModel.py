# # standalone_downloader.py
# import firebase_admin
# from firebase_admin import credentials, storage

# def download_saved_data():
#     # Initialize Firebase
#     cred = credentials.Certificate("C:/Users/joppe/machine-learning/serviceAccountKey.json")
#     firebase_admin.initialize_app(cred, {
#         'storageBucket': 'my-anime-guide.appspot.com'
#     })

#     # Download anime_dataframe.pkl
#     bucket = storage.bucket()
#     blob_df = bucket.blob('anime_dataframe.pkl')
#     blob_df.download_to_filename('model/anime_dataframe.pkl')

#     # Download cosine_similarity_matrix.pkl
#     blob_cosine = bucket.blob('cosine_similarity_matrix.pkl')
#     blob_cosine.download_to_filename('model/cosine_similarity_matrix.pkl')

#     print("Download complete. Files are now stored locally.")

# if __name__ == '__main__':
#     download_saved_data()
