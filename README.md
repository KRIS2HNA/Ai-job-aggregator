# 🚀 AI-Powered Job Aggregation & Intelligence System

An end-to-end ML-powered job intelligence platform that aggregates job data, extracts skills using NLP, generates semantic embeddings using transformers, provides recommendations, analytics, and is fully containerized for cloud deployment.

---

## 📌 Project Overview

This project is a scalable backend-driven job aggregation system built using:

- FastAPI – REST API framework  
- PostgreSQL – Relational database  
- SQLAlchemy ORM – Database abstraction  
- spaCy – NLP skill extraction  
- Sentence Transformers (MiniLM) – Semantic embeddings  
- Docker – Containerization  
- Streamlit – Interactive dashboard  

The system performs:

- Job ingestion  
- Automated skill extraction  
- Relational filtering  
- Analytics generation  
- Semantic job recommendations  
- Cloud-ready deployment  

---

## 🏗 System Architecture
Streamlit Dashboard
↓
FastAPI REST API
↓
Service Layer (Business Logic)
↓
ORM Layer (SQLAlchemy)
↓
PostgreSQL Database
↓
NLP + Transformer ML Layer


---

## 📂 Project Structure

ai-job-system/
│
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── job_service.py
│ ├── skill_extractor.py
│ ├── analytics.py
│ └── recommender.py
│
├── streamlit_app.py
├── Dockerfile
├── requirements.txt
└── README.md
