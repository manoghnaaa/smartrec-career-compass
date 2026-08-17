# SMARTREC — Your Career Compass

An intelligent career-discovery and job recommendation platform powered by Data Science and Machine Learning.

---

## 1. Overview
SmartRec is a professional job recommendation and career navigation platform designed for data science portfolios. It aligns candidate skills with active job registries to map out viable career pathways.

## 2. Problem Statement
Job seekers struggle to identify relevant positions because traditional search engines rely on rigid keyword matches. Variations in spellings, acronyms, or role titles lead to poor alignment and hidden skill gaps.

## 3. Solution
SmartRec solves this by vectorizing job profiles and candidate attributes, using cosine similarity to calculate numeric alignment rankings, and delivering a personal career recommendation bot.

## 4. Features
* **Career Compass Dashboard**: A dynamic visual representation of career alignments based on your skillset.
* **Discover Jobs**: Filter, rank, and explore top recommendations.
* **SmartRec Guide**: Interactive advisor chatbot utilizing the recommendation engine.
* **Explore Directory**: Search, sort, and query the entire career directory.
* **Opportunity Vault**: Save and manage promising job opportunities.
* **Career Insights**: Visualization of dataset statistics.

## 5. Dataset
The dataset comprises 1,167 active job registry records with attributes: `job_id`, `category`, `job_title`, `job_description`, and `job_skill_set`.

## 6. Data Science Workflow
1. **Data Ingestion**: Deserialize binary records from serialized formats.
2. **Text Processing**: Tokenize, normalize, and lowercase skills, roles, and descriptions.
3. **Feature Extraction**: Transform text into high-dimensional frequency vectors.
4. **Similarity Computation**: Compute numeric similarity metrics between user queries and job records.
5. **Ranking**: Sort and return the highest-scoring records.

## 7. Model Selection
We compared three different recommendation pipelines during validation:
1. **Count Vectorizer + Cosine Similarity** (Selected)
2. TF-IDF + Cosine Similarity
3. TF-IDF + Linear Kernel

## 8. Evaluation
The performance of each configuration was evaluated using **Precision@5** (accuracy of the top 5 recommended roles). The **Count Vectorizer + Cosine Similarity** model achieved the highest score of **88%**.

## 9. Recommendation Algorithm
Candidate vectors are created by tokenizing user skills and preferred roles. Cosine similarity calculates the angle against the pre-computed CSR (Compressed Sparse Row) job matrix:
$$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

## 10. Chatbot
The **SmartRec Guide** is an NLP-driven chatbot. It extracts skill sets and role preferences using regex parsers and generates top 5 recommendations dynamically inside the chat window.

## 11. Career Compass
The dashboard visualizes career directions as an interactive SVG map representing North, East, South, and West directions matching the top 4 recommended job categories and similarity percentages.

## 12. Technology Stack
* **UI Framework**: Streamlit
* **Styling**: Modern Glassmorphic CSS Theme
* **Math & Decoding**: Pure-Python Vector computation (bypasses numpy C-extensions restrictions)

## 13. Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 14. Usage
Run the Streamlit application:
```bash
streamlit run app.py
```

## 15. Project Structure
* `app.py` — Main Streamlit application
* `job_data.pkl` — Job listings data
* `job_matrix.pkl` — Vectorized CSR matrix
* `count_vectorizer.pkl` — Vocabulary mappings
* `requirements.txt` — Package requirements
* `README.md` — Project documentation

## 16. Limitations
SmartRec uses content-based matching. Recommendations depend on the information available in the job dataset and therefore may not capture user behavior, real-time market demand, salary preferences, or collaborative preferences.

## 17. Future Improvements
* Add collaborative filtering model pathways.
* Integrate dynamic real-time job scraping.
* Support PDF resume parser inputs.
