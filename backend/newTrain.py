import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import scipy.sparse as sp

def load_data(filename):
    return pd.read_csv(filename, na_values=["", " "])

def preprocess_data(df, feature_columns):
    mlbs = {}
    feature_matrices = []
    
    df["duration"] = df["duration"].str.extract("(\d+)").astype(float)
    df["duration"].fillna(df["duration"].mean(), inplace=True)
    
    for col in feature_columns:
        df[col] = df[col].str.split(',')
        df[col].fillna("", inplace=True)
        mlb = MultiLabelBinarizer()
        encoded_data = mlb.fit_transform(df[col])
        feature_matrices.append(encoded_data)
        mlbs[col] = mlb

    features_matrix = np.hstack(feature_matrices)
    
    return df, features_matrix, mlbs

if __name__ == '__main__':
    filename = "anime_list.csv"
    df = load_data(filename)

    feature_columns = ['genres', 'themes', 'studios', 'allRank']
    df, features_matrix, _ = preprocess_data(df, feature_columns)

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(features_matrix).astype(np.float16)

    # Save the anime DataFrame and cosine similarity matrix
    save_directory = "newModel"
    df.to_pickle(os.path.join(save_directory, "anime_dataframe.pkl"))
    with open(os.path.join(save_directory, "cosine_similarity_matrix.pkl"), 'wb') as f:
        pickle.dump(cosine_sim, f)

    print("Data processed and saved successfully!")