import streamlit as st
import pickle
import numpy as np
import os
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine, text

# ---------------------------------------------------
# LOAD ENV
# ---------------------------------------------------
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

# ---------------------------------------------------
# DATABASE (SAFE MODE: works local + docker)
# ---------------------------------------------------
engine = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)

    def init_db():
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS recommendation_logs (
                    id SERIAL PRIMARY KEY,
                    selected_song VARCHAR(255),
                    recommended_song VARCHAR(255),
                    similarity FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()

    init_db()

# ---------------------------------------------------
# SPOTIFY CLIENT (SAFE)
# ---------------------------------------------------
sp = None

if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        )
    )

# ---------------------------------------------------
# LOAD ARTIFACTS
# ---------------------------------------------------
@st.cache_resource
def load_artifacts():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    artifacts_path = os.path.join(BASE_DIR, "artifacts")

    df = pickle.load(open(os.path.join(artifacts_path, "df.pkl"), "rb"))
    final_matrix = pickle.load(open(os.path.join(artifacts_path, "final_matrix.pkl"), "rb"))
    final_matrix = final_matrix.tocsr()
    return df, final_matrix

df, final_matrix = load_artifacts()

# ---------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------
st.title("🎵 Spotify AI Recommendation System")
st.caption("Hybrid ML + Spotify Integration + Docker + PostgreSQL")

# ---------------------------------------------------
# CONTROLS
# ---------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    selected_song = st.selectbox("🎵 Select Song", df["track_name"].unique())

with col2:
    alpha = st.slider("⚖ AI Balance", 0.0, 1.0, 0.8)

with col3:
    mood_filter = st.selectbox("🎭 Mood", ["All"] + sorted(df["mood"].unique()))

# ---------------------------------------------------
# RECOMMENDATION LOGIC
# ---------------------------------------------------
def recommend(song, top_n=6):
    idx = df[df["track_name"] == song].index[0]
    sim_scores = cosine_similarity(final_matrix[idx], final_matrix).flatten()

    blended = alpha * sim_scores + (1 - alpha) * df["pop_score"]

    temp = df.copy()
    temp["score"] = blended
    temp["similarity"] = sim_scores

    if mood_filter != "All":
        temp = temp[temp["mood"] == mood_filter]

    temp = temp.sort_values("score", ascending=False)
    temp = temp[temp["track_name"] != song]

    return temp.head(top_n)

# ---------------------------------------------------
# SPOTIFY HELPER
# ---------------------------------------------------
def get_spotify_info(track, artist):
    if not sp:
        return None, None, None

    try:
        result = sp.search(
            q=f"track:{track} artist:{artist}",
            type="track",
            limit=1,
            market="US"
        )
        item = result["tracks"]["items"][0]
        return (
            item["album"]["images"][0]["url"],
            item["preview_url"],
            item["external_urls"]["spotify"]
        )
    except:
        return None, None, None

# ---------------------------------------------------
# GENERATE BUTTON
# ---------------------------------------------------
if st.button("✨ Generate AI Recommendations"):

    recs = recommend(selected_song)

    st.subheader("🎶 Recommended Tracks")

    # ---- DB LOGGING (ONLY IF ENGINE EXISTS)
    if engine:
        with engine.connect() as conn:
            for _, row in recs.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO recommendation_logs 
                        (selected_song, recommended_song, similarity)
                        VALUES (:selected, :recommended, :sim)
                    """),
                    {
                        "selected": selected_song,
                        "recommended": row["track_name"],
                        "sim": float(row["similarity"])
                    }
                )
            conn.commit()

    # ---- DISPLAY RESULTS
    for _, row in recs.iterrows():

        st.markdown("---")

        st.markdown(f"### {row['track_name']}")
        st.write(f"Artist: {row['artist_name']}")
        st.write(f"Similarity: {round(row['similarity']*100,2)}%")
        st.write(f"Popularity: {row['track_popularity']}")

        image, preview, link = get_spotify_info(
            row["track_name"],
            row["artist_name"]
        )

        if image:
            st.image(image, width=250)

        if preview:
            st.audio(preview)

        if link:
            st.markdown(f"[Open in Spotify]({link})")

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
st.subheader("📊 Music Analytics")

colA, colB = st.columns(2)

with colA:
    mood_chart = px.pie(df, names="mood", title="Mood Distribution")
    st.plotly_chart(mood_chart, width="stretch")

with colB:
    pop_chart = px.histogram(df, x="track_popularity", title="Popularity Spread")
    st.plotly_chart(pop_chart, width="stretch")