# 🎵 Spotify AI Recommendation System

<p align="center">
  <img src="assets/homepage.png" width="800">
</p>

<p align="center">
  <b>Hybrid Machine Learning + Spotify API + PostgreSQL + Docker</b>
</p>

---

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![ML](https://img.shields.io/badge/Machine%20Learning-Recommendation-green)

## 📌 Overview

This project is a production-ready hybrid music recommendation engine built using content-based filtering with cosine similarity, enhanced by popularity blending and real-time Spotify API integration.

The system provides:

- 🎧 Intelligent song recommendations
- 🎵 Spotify album cover + audio preview
- 📊 Real-time analytics dashboard
- 🗄 PostgreSQL logging of recommendation history
- 🐳 Full Docker multi-container deployment

## 🏗 Architecture

User
  ↓
Streamlit App (Docker Container)
  ↓
ML Recommendation Engine
  ↓
Spotify Web API
  ↓
PostgreSQL (Docker Container)

## 🎧 Application Interface

### 🏠 Homepage

<p align="center">
  <img src="assets/homepage.png" width="800">
</p>

---

### 🤖 AI Recommendations

<p align="center">
  <img src="assets/recommendations.png" width="800">
</p>

---

### 📊 Analytics Dashboard

<p align="center">
  <img src="assets/dashboard.png" width="800">
</p>

-- Installation:

## 🛠 Local Setup
git clone https://github.com/yourusername/spotify-ai-recommendation-system.git
cd spotify-ai-recommendation-system
pip install -r requirements.txt
streamlit run app/app.py

## 🐳 Docker Deployment
docker-compose up --build
http://localhost:8501

## 🔐 Environment Variables
SPOTIFY_CLIENT_ID=your_id
SPOTIFY_CLIENT_SECRET=your_secret

## 🗄 Database Logging
docker exec -it spotify_db psql -U postgres
\c spotifydb
SELECT * FROM recommendation_logs;

## 🧠 ML Strategy
Similarity Score = Cosine Similarity (TF-IDF features)

Final Ranking Score =
α * Similarity + (1 - α) * Popularity Score

## 🧪 Tech Stack

Python

Streamlit

Scikit-learn

Spotipy

SQLAlchemy

PostgreSQL

Docker

Docker Compose

Plotly

## 🚀 Future Improvements

Collaborative filtering

Matrix factorization

Neural embeddings

User authentication

FastAPI backend

CI/CD pipeline

## 📑 Table of Contents
- Overview
- Architecture
- Features
- Demo
- Installation
- Docker Deployment
- Environment Variables
- ML Strategy
- Tech Stack
- Future Improvements