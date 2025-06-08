# Graph-Augmented Course Recommendation System with Explainable AI
This project presents a Graph Neural Network (GNN)-based Course Recommendation Decision Support System (DSS) that predicts suitable university courses for students based on academic history, peer trajectories, prerequisite structures, and skill alignment. It incorporates Explainable AI (XAI) techniques to provide transparent reasoning behind each recommendation and is deployed via a clean Streamlit interface with a MongoDB backend.

This project is a Decision Support System that recommends university courses to students based on their academic history, interests, credit requirements, and preferences. It features a clean Streamlit-based UI and uses MongoDB as the backend for storing student and course data.

---

## 📁 Project Structure & Code Flow

```
📁 DSS/
├── app.py                    # 🌐 Streamlit-based UI for user interaction
├── gnn_model.py              # 🤖 GNN training and inference (GraphSAGE)
├── graph_builder.py          # 🧱 Constructs heterogeneous graph from data
├── explain_module.py         # 🔍 XAI utilities for generating explanations
├── insertsampledata.py       # 📥 Sample synthetic data generation script
├── connection.py             # 🔗 MongoDB connection helper
├── recommend_engine.py       # 🧠 Fallback rule-based engine
├── requirements.txt          # 📦 Python dependencies

```

app.py: Streamlit web app to collect student input and visualize course recommendations with explanations.

gnn_model.py: Trains and applies the GraphSAGE model to learn node embeddings and predict course links.

graph_builder.py: Constructs a heterogeneous graph with student, course, and skill nodes connected by various edge types.

explain_module.py: Generates human-readable explanations using graph attribution and node similarity.

recommend_engine.py: Provides fallback rule-based logic (for baseline or comparison).

insertsampledata.py: Populates MongoDB with synthetic academic records (students, courses, skills).

MongoDB: Stores all data, including graph metadata and user inputs, using MongoDB Atlas.

---

## 🛠️ Setup Instructions

### 1. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate   # Windows
```

### 2. Install Dependencies

```bash
pip install streamlit pymongo pandas numpy scikit-learn matplotlib networkx torch torch-geometric

```

---

## ☁️ Synthetic Data & MongoDB Setup

To populate the database with synthetic records:


Use:

```bash
python insertsampledata.py
```

This script generates:

1,000+ synthetic student profiles

200+ course nodes with prerequisite and skill metadata

Skill mappings and simulated enrollments

---

## 🚀 Run the Web App

```bash
streamlit run app.py
```

App runs at:

```
http://localhost:8501
```

---

## ✨ Key Features
🔗 GNN-based course recommendations using GraphSAGE on a heterogeneous graph

🔍 Explainable AI outputs with justifications (skill alignment, peer similarity, prerequisites)

🧪 Synthetic data simulation for student-course-skill relationships

🗃️ MongoDB backend for scalable graph and user data storage

🖥️ Interactive Streamlit UI with filters for credits, interests, and exclusions

📅 Visualized weekly schedule builder and dynamic course set selection



---

## ✅ Sample Test Case

Roll Number: S1001  
Name: Alice  
Major: Computer Science

---

## 📌 Notes

The system uses a hybrid architecture, combining rule-based logic with GNN predictions for fallback or evaluation.

Designed for research and deployment prototypes in educational technology and personalized learning.

---

## 🙌 Contributors

Built with ♥ using PyTorch Geometric, MongoDB, Streamlit, and NetworkX.
Research and modeling guided by academic supervision in intelligent systems and recommender design.