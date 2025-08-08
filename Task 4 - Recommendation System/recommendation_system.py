import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- Load datasets ---
kdrama = pd.read_csv("kdrama.csv")
bollywood = pd.read_csv("Data for repository.csv")

# --- Rename columns to unify ---
kdrama = kdrama.rename(columns={"Name": "Title", "Cast": "Actors"})
bollywood = bollywood.rename(columns={"Movie Name": "Title", "New Actor": "Actors"})

# Add identifier
kdrama["Source"] = "Kdrama"
bollywood["Source"] = "Bollywood"

# Add missing column to Bollywood
bollywood["Number of Episodes"] = ""

# Select relevant columns
kdrama = kdrama[["Title", "Genre", "Actors", "Number of Episodes", "Source"]]
bollywood = bollywood[["Title", "Genre", "Actors", "Number of Episodes", "Source"]]

# Combine both datasets
df = pd.concat([kdrama, bollywood], ignore_index=True)
df.fillna("", inplace=True)

# --- Create combined content for similarity comparison ---
df["content"] = df["Genre"] + " " + df["Actors"]

# --- Vectorize content using TF-IDF ---
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["content"])

# --- Calculate cosine similarity ---
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# --- Helper: Normalize titles (remove punctuation, lowercase) ---
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text

# --- Recommendation function ---
def recommend(user_input, cosine_sim=cosine_sim):
    df["Title_normalized"] = df["Title"].apply(normalize)
    input_norm = normalize(user_input)

    if input_norm not in df["Title_normalized"].values:
        return "❌ Title not found. Please check spelling or try another."

    idx = df[df["Title_normalized"] == input_norm].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    indices = [i[0] for i in sim_scores]

    recommendations = []
    for i in indices:
        title = df.iloc[i]["Title"]
        genre = df.iloc[i]["Genre"]
        episodes = df.iloc[i]["Number of Episodes"]
        source = df.iloc[i]["Source"]

        info = f"{title} | Genre: {genre}"
        if source == "Kdrama":
            info += f" | Episodes: {episodes}"
        recommendations.append(info)

    return recommendations

# --- Run the program ---
user_input = input("🎬 Enter the last movie or drama you watched: ")
results = recommend(user_input)

print("\n✨ Recommended titles for you:\n")
if isinstance(results, list):
    for i, rec in enumerate(results, 1):
        print(f"{i}. {rec}")
else:
    print(results)



