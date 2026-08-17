# SMARTREC: Your Career Compass

SmartRec is an intelligent, personalized career-discovery platform designed to help users navigate their career path by matching their skills and preferences with relevant job opportunities. 

This platform serves as a modern, data-driven career assistant, moving away from standard static dashboards to deliver a rich, interactive, and visually stunning product experience suitable for portfolio display and industry presentations.

---

## 🌟 Key Features

1. **🧭 Career Compass Dashboard**: A visual entry point showing the user's current skills, their strongest match role ("Career Match"), alternative directions ("Next Best Matches"), and an interactive visual SVG map of career pathways.
2. **🎯 Discover Jobs**: The primary recommendation page where users can specify skills, roles, and preferred job categories to get a ranked list of the top 10 recommended jobs.
3. **✦ SmartRec Guide (Chatbot)**: A dedicated career recommendation chatbot that extracts skills, roles, and categories from natural language queries and displays job matches directly in the chat interface.
4. **🔎 Explore Opportunities**: A complete search engine to search by title, skills, filter by category, and sort by relevance or alphabetical criteria.
5. **♡ Opportunity Vault**: A personalized folder to save and manage promising opportunities.
6. **📊 Career Insights**: Interactive, custom SVG charts showing real statistics of the dataset, including category distributions and common titles.
7. **👤 My Career Profile**: Profile editor feeding directly into the recommendation engine.
8. **⚙️ Settings & Security**: Fully implemented authentication state (Sign In, Sign Up, Logout) and options to reset the profile, clear saved vault, or reset chat history.

---

## 🤖 Machine Learning Pipeline & Algorithm

SmartRec uses a pre-trained **Content-Based Recommendation System** trained and validated on the job dataset.

### Pipeline Structure:
```
[User Skills + Preferred Role + Preferred Category]
                       ↓
              Create User Profile
                       ↓
              Count Vectorizer
                       ↓
               Cosine Similarity
                       ↓
            Rank & Recommend Jobs
```

### Technical Details:
* **Feature Extraction**: Count Vectorization (compares frequency counts of terms in titles, descriptions, and skillsets).
* **Similarity Metric**: Cosine Similarity (measures the angle between query and document vectors in a 10,000-dimensional space).
* **Evaluation Metric**: Precision@5.
* **Accuracy**: The chosen Count Vectorizer + Cosine Similarity model achieved a **Precision@5 score of 88%**, outperforming TF-IDF and Linear Kernel configurations.

---

## 📂 Project Structure

```
SmartRec/
├── count_vectorizer.pkl    # Fitted CountVectorizer vocabulary weights
├── job_data.pkl            # Unserialized job records DataFrame
├── job_matrix.pkl          # Serialized sparse job matrix (CSR matrix)
├── app.py                  # Main Streamlit application with custom styling
├── requirements.txt        # Package dependencies list
└── README.md               # Project documentation (this file)
```

---

## ⚙️ Installation & Usage

### Prerequisites
Make sure Python 3.11+ is installed.

### Setup Instructions
1. Clone or copy the project directory to your local workspace.
2. Open a terminal (e.g., PowerShell) and navigate to the project directory:
   ```bash
   cd SmartRec
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

---

## 👨‍💻 Tech Stack
* **Frontend UI**: Streamlit 1.60+ augmented with custom Glassmorphism CSS styling.
* **Data Processing**: Standard library `struct` and `pickle` for optimized, safe, zero-dependency model decoding.
* **Vector Computations**: Pure Python cosine similarity and CountVectorizer token matching (bypasses OS/WDAC DLL execution blocks).
