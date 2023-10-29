# Anime Recommendation System

This document explains a function that recommends anime titles based on user's watched history.

## Overview

The function is an anime recommendation system. Given a user's history of watched anime, it will suggest new anime titles based on similarities.

## Function Breakdown

### 1. Inputs

The function takes four inputs:
- `df`: A table of anime details.
- `cosine_sim`: A grid that tells how similar each anime is to every other anime.
- `user_history`: A list of anime the user has watched.
- `N`: How many anime you want to recommend. By default, it's 20.

### 2. Finding User's Anime in the List

```python
user_anime_indices = []
for title in user_history:
    ...
```

This part looks for each anime in the user's list inside our big anime table. If it can't find one, it gives a warning.

### 3. Calculating Average Similarity

```python
avg_sim_scores = cosine_sim[user_anime_indices].mean(axis=0)
```

For each anime in our big list, this finds out how similar it is to the anime the user has watched, on average.

### 4. Making Scores Between 0 and 1

```python
max_score = df["score"].max()
normalized_scores = df["score"].fillna(0) / max_score
```

This takes the scores of all anime and changes them to be between 0 and 1. This makes combining scores easier later.

### 5. Combining Scores Together

```python
combined_scores = avg_sim_scores + normalized_scores
```

This adds together the similarity scores and the scores of the anime, so each anime gets one combined score.

### 6. Picking the Top Anime

```python
top_indices = combined_scores.argsort()[-N-1:-1][::-1]
```

This step picks the top `N` anime based on their combined scores.

### 7. Getting Details of Top Anime

```python
recommended_anime = df.iloc[top_indices][...]
```

This step grabs all the details of those top `N` anime, like their names, scores, and more.

### 8. Showing How Similar the Anime Are

```python
similarity_percentages = (avg_sim_scores[top_indices] * 100).tolist()
recommended_anime['similarity_percentage'] = similarity_percentages
```

This calculates and shows how similar each recommended anime is to the user's watched list.

### 9. Making Sure Recommendations are Unique

```python
for title in user_history:
    ...
```

If any recommended anime is too similar to what the user has already watched, this step removes the extra ones.

### 10. Giving the Recommendations

```python
return recommended_anime
```

Lastly, the function gives back the recommended anime list.

---

Feel free to copy the above markdown content and use it as needed!