import streamlit as st
import pickle
import struct
import re
import math
import os
import ast

# Set page configuration first
st.set_page_config(
    page_title="SmartRec - Your Career Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling Injection
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

/* Base Styles & Typography */
.stApp {
    background: radial-gradient(circle at top right, #f8fafc, #e2e8f0 90%) !important;
    font-family: 'Inter', sans-serif !important;
    color: #1e293b !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    color: #0f172a !important;
    font-weight: 700 !important;
}

/* Faint Grid Overlay for Career Compass Theme */
.stApp::before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    background-image: 
        radial-gradient(rgba(15, 23, 42, 0.02) 1px, transparent 1px) !important;
    background-size: 24px 24px !important;
    pointer-events: none !important;
    z-index: 0 !important;
}

/* Glowing background sphere auroras */
.bg-glow-1 {
    position: fixed !important;
    top: 10% !important;
    left: 15% !important;
    width: 400px !important;
    height: 400px !important;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.05) 0%, rgba(99, 102, 241, 0) 70%) !important;
    filter: blur(80px) !important;
    pointer-events: none !important;
    z-index: -1 !important;
}

.bg-glow-2 {
    position: fixed !important;
    bottom: 10% !important;
    right: 15% !important;
    width: 450px !important;
    height: 450px !important;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.04) 0%, rgba(14, 165, 233, 0) 70%) !important;
    filter: blur(90px) !important;
    pointer-events: none !important;
    z-index: -1 !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid rgba(15, 23, 42, 0.06) !important;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem !important;
}

/* Primary Glowing Buttons (Form Submits) */
div.stFormSubmitButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.2) !important;
    width: 100% !important;
}

div.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35) !important;
    background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
}

/* Secondary Glassmorphism Buttons */
div.stButton > button {
    background: rgba(15, 23, 42, 0.03) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    color: #334155 !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.25s ease !important;
    box-shadow: none !important;
}

div.stButton > button:hover {
    background: rgba(15, 23, 42, 0.06) !important;
    border-color: rgba(15, 23, 42, 0.15) !important;
    color: #0f172a !important;
    transform: translateY(-1px) !important;
}

/* Sidebar Navigation Buttons (Keep distinct) */
[data-testid="stSidebar"] button {
    background: transparent !important;
    color: #475569 !important;
    border: 1px solid transparent !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 12px 18px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
    box-shadow: none !important;
    margin-bottom: 4px !important;
}

[data-testid="stSidebar"] button:hover {
    background: rgba(14, 165, 233, 0.06) !important;
    color: #0ea5e9 !important;
    border: 1px solid rgba(14, 165, 233, 0.15) !important;
    transform: translateX(4px);
}

/* Unified Form Container (Login & Signup Cards) */
[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.65) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 20px !important;
    padding: 40px !important;
    box-shadow: 
        0 20px 40px -15px rgba(15, 23, 42, 0.08),
        0 0 50px rgba(99, 102, 241, 0.03) !important;
    margin-top: 15px !important;
    margin-bottom: 15px !important;
}

/* Customize Text Inputs Globally */
[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    color: #0f172a !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}

[data-testid="stTextInput"] label {
    color: #475569 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 6px !important;
}

/* Reposition "Press Enter to submit form" instructions below input fields */
[data-testid="InputInstructions"] {
    position: relative !important;
    bottom: auto !important;
    right: auto !important;
    margin-top: 6px !important;
    color: #475569 !important;
    font-size: 11px !important;
    display: block !important;
    text-align: right !important;
}

div[data-testid="stTextInput"] > div {
    overflow: visible !important;
}

/* Animated Compass Needle sway effect */
@keyframes sway {
    0% { transform: rotate(-6deg); }
    50% { transform: rotate(6deg); }
    100% { transform: rotate(-6deg); }
}
.needle-group {
    transform-origin: 50px 50px;
    animation: sway 4.5s ease-in-out infinite;
}

/* Glassmorphism Cards */
.sr-card, div.stVerticalBlockBorder, [data-testid="stVerticalBlockBorder"] {
    background: rgba(255, 255, 255, 0.55) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.02) !important;
}

.sr-card:hover, div.stVerticalBlockBorder:hover, [data-testid="stVerticalBlockBorder"]:hover {
    transform: translateY(-4px) !important;
    border-color: rgba(99, 102, 241, 0.2) !important;
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.06) !important;
}

/* Match Percentage Badge */
.match-badge {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(16, 185, 129, 0.12)) !important;
    border: 1px solid rgba(16, 185, 129, 0.18) !important;
    color: #059669 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    padding: 6px 14px !important;
    border-radius: 30px !important;
    display: inline-flex !important;
    align-items: center !important;
}

/* Skill Chips */
.skill-chip {
    background: rgba(15, 23, 42, 0.03) !important;
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    color: #334155 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    display: inline-block !important;
    margin: 4px 3px !important;
}

.skill-chip-matched {
    background: rgba(14, 165, 233, 0.06) !important;
    border: 1px solid rgba(14, 165, 233, 0.18) !important;
    color: #0284c7 !important;
}

.skill-chip-gap {
    background: rgba(217, 119, 6, 0.06) !important;
    border: 1px solid rgba(217, 119, 6, 0.18) !important;
    color: #b45309 !important;
}

/* Chat Interface Styling */
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 20px;
}

.chat-bubble-user {
    background: #4f46e5 !important;
    color: #ffffff !important;
    padding: 12px 18px !important;
    border-radius: 16px 16px 4px 16px !important;
    max-width: 75% !important;
    margin-left: auto !important;
    margin-bottom: 12px !important;
    font-size: 14px !important;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.15) !important;
}

.chat-bubble-guide {
    background: rgba(255, 255, 255, 0.75) !important;
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    color: #1e293b !important;
    padding: 12px 18px !important;
    border-radius: 16px 16px 16px 4px !important;
    max-width: 75% !important;
    margin-right: auto !important;
    margin-bottom: 12px !important;
    font-size: 14px !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.02) !important;
}

/* Custom Prompt suggestion button styling */
.prompt-btn button {
    background: rgba(255, 255, 255, 0.8) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    color: #475569 !important;
    padding: 6px 12px !important;
    font-size: 12px !important;
    border-radius: 20px !important;
    box-shadow: none !important;
    margin: 4px 2px !important;
}

.prompt-btn button:hover {
    color: #4f46e5 !important;
    background: rgba(99, 102, 241, 0.04) !important;
    border-color: rgba(99, 102, 241, 0.2) !important;
    transform: translateY(-1px) !important;
}

/* Sidebar Branding */
.sidebar-logo {
    font-family: 'Outfit', sans-serif !important;
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    letter-spacing: 2px !important;
    text-align: center;
    margin-top: 10px;
}

.sidebar-tagline {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #0ea5e9 !important;
    letter-spacing: 1px;
    text-align: center;
    margin-bottom: 20px;
}

.sidebar-divider {
    border: 0 !important;
    height: 1px !important;
    background: linear-gradient(to right, transparent, rgba(15, 23, 42, 0.08), transparent) !important;
    margin-bottom: 20px !important;
}

/* Style the login page illustration image */
.login-illustration {
    width: 100% !important;
    border-radius: 20px !important;
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    box-shadow: 
        0 15px 30px -10px rgba(15, 23, 42, 0.08),
        0 0 40px rgba(99, 102, 241, 0.04) !important;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.login-illustration:hover {
    transform: scale(1.012) translateY(-1px) !important;
    border-color: rgba(99, 102, 241, 0.15) !important;
    box-shadow: 
        0 20px 40px -10px rgba(15, 23, 42, 0.12),
        0 0 50px rgba(99, 102, 241, 0.08) !important;
}
</style>
""", unsafe_allow_html=True)

# Define Custom Unpickler & Loaders to Bypass WDAC C-Extensions DLL Block
class DummyPickleObj:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    def __setstate__(self, state):
        self.state = state
    def __reduce__(self):
        return (self.__class__, self.args, getattr(self, 'state', {}))

class MockDataFrame(DummyPickleObj): pass
class MockBlockManager(DummyPickleObj): pass
class MockBlock(DummyPickleObj): pass
class MockArray(DummyPickleObj): pass
class MockDtype(DummyPickleObj): pass
class MockCV(DummyPickleObj): pass
class MockCSR(DummyPickleObj): pass

class PurePythonUnpickler(pickle._Unpickler):
    def find_class(self, module, name):
        if module == 'pandas.core.frame' and name == 'DataFrame':
            return MockDataFrame
        elif module == 'pandas.core.internals.managers' and name == 'BlockManager':
            return MockBlockManager
        elif module == 'pandas._libs.internals' and name == '_unpickle_block':
            return lambda *args, **kwargs: MockBlock(*args, **kwargs)
        elif module == 'numpy._core.numeric' and name == '_frombuffer':
            return lambda *args, **kwargs: MockArray(*args, **kwargs)
        elif module == 'numpy' and name == 'dtype':
            return MockDtype
        elif module == 'scipy.sparse._csr' and name == 'csr_matrix':
            return MockCSR
        elif module == 'sklearn.feature_extraction.text' and name == 'CountVectorizer':
            return MockCV
        
        class DynamicDummy(DummyPickleObj):
            pass
        DynamicDummy.__name__ = name
        return DynamicDummy

def find_model_file(filename):
    if os.path.exists(filename):
        return filename
    model_path = os.path.join("model", filename)
    if os.path.exists(model_path):
        return model_path
    raise FileNotFoundError(f"Model file '{filename}' not found in the root or model/ directories.")

@st.cache_resource
def load_all_model_artifacts():
    try:
        # 1. Load job_data
        data_path = find_model_file('job_data.pkl')
        with open(data_path, 'rb') as f:
            raw_data = PurePythonUnpickler(f).load()
        
        df_state = raw_data.state
        bm = df_state['_mgr']
        blocks, axes = bm.args
        
        # Block 0 is job_id (int64)
        int_block = blocks[0]
        buf = int_block.args[0].args[0]
        row_count = len(buf) // 8
        job_ids = list(struct.unpack(f'<{row_count}q', buf))
        
        # Block 1 is object block (strings)
        str_block = blocks[1]
        str_state = str_block.args[0].state
        strings = str_state[4]
        
        # Flattened numpy array of shape (4, 1167) in C-contiguous order
        categories = strings[0 : row_count]
        titles = strings[row_count : 2*row_count]
        descriptions = strings[2*row_count : 3*row_count]
        skills_raw = strings[3*row_count : 4*row_count]
        
        jobs = []
        for i in range(row_count):
            # Parse skill lists safely
            skill_str = skills_raw[i]
            parsed_skills = []
            try:
                parsed_skills = ast.literal_eval(skill_str)
            except Exception:
                if isinstance(skill_str, list):
                    parsed_skills = skill_str
                else:
                    # manual split
                    s = skill_str.strip("[]'\"")
                    parsed_skills = [x.strip().strip("'\"") for x in s.split(",") if x.strip()]
            
            jobs.append({
                'job_id': job_ids[i],
                'category': categories[i],
                'job_title': titles[i],
                'job_description': descriptions[i],
                'job_skill_set': parsed_skills
            })
            
        # 2. Load job_matrix
        matrix_path = find_model_file('job_matrix.pkl')
        with open(matrix_path, 'rb') as f:
            raw_matrix = PurePythonUnpickler(f).load()
            
        state = raw_matrix.state
        shape = state['_shape']
        rows, cols = shape
        
        indices_bytes = state['indices'].state[4]
        indices_len = len(indices_bytes) // 4
        indices = list(struct.unpack(f'<{indices_len}i', indices_bytes))
        
        indptr_bytes = state['indptr'].state[4]
        indptr_len = len(indptr_bytes) // 4
        indptr = list(struct.unpack(f'<{indptr_len}i', indptr_bytes))
        
        data_bytes = state['data'].state[4]
        data_len = len(data_bytes) // 8
        data_val = list(struct.unpack(f'<{data_len}q', data_bytes))
        
        job_matrix = {
            'shape': shape,
            'indices': indices,
            'indptr': indptr,
            'data': data_val
        }
        
        # 3. Load count_vectorizer
        cv_path = find_model_file('count_vectorizer.pkl')
        with open(cv_path, 'rb') as f:
            raw_cv = PurePythonUnpickler(f).load()
            
        cv_state = raw_cv.state
        raw_vocab = cv_state['vocabulary_']
        
        vocab = {}
        for word, scalar_obj in raw_vocab.items():
            scalar_args = scalar_obj.args
            val_bytes = scalar_args[1]
            val = struct.unpack('<q', val_bytes)[0]
            vocab[word] = val
            
        count_vectorizer = {
            'vocabulary_': vocab,
            'lowercase': cv_state.get('lowercase', True),
            'token_pattern': cv_state.get('token_pattern', r'(?u)\b\w\w+\b')
        }
        
        # Precompute job norms
        job_norms = []
        for i in range(rows):
            start = indptr[i]
            end = indptr[i+1]
            row_data = data_val[start:end]
            val_sum = sum(v * v for v in row_data)
            job_norms.append(math.sqrt(val_sum))
            
        return jobs, job_matrix, count_vectorizer, job_norms
        
    except Exception as e:
        st.error(f"Error loading model artifacts: {str(e)}")
        # Output friendly instructions instead of traceback
        st.info("Please ensure 'count_vectorizer.pkl', 'job_data.pkl', and 'job_matrix.pkl' are placed in the root directory or a 'model/' folder.")
        return None, None, None, None

# Reusable Recommendation Function
def get_recommendations(skills_list, preferred_role, preferred_category, jobs, matrix, cv, job_norms, limit=10):
    # Normalize and compile inputs
    # If skills are lists, join with space
    skills_str = " ".join(skills_list) if isinstance(skills_list, list) else skills_list
    
    # Combined user profile matching original pipeline concatenation
    query_text = f"{preferred_role} {preferred_category} {skills_str}"
    
    # Tokenize query
    tokens = re.findall(r'\b\w\w+\b', query_text.lower())
    
    # Build query vector frequencies
    vocab = cv['vocabulary_']
    query_vector = {}
    for token in tokens:
        if token in vocab:
            idx = vocab[token]
            query_vector[idx] = query_vector.get(idx, 0) + 1
            
    if not query_vector:
        return []
        
    q_norm = math.sqrt(sum(v * v for v in query_vector.values()))
    
    similarities = []
    rows = len(job_norms)
    for i in range(rows):
        start = matrix['indptr'][i]
        end = matrix['indptr'][i+1]
        
        row_indices = matrix['indices'][start:end]
        row_data = matrix['data'][start:end]
        
        dot_product = 0.0
        for idx, val in zip(row_indices, row_data):
            if idx in query_vector:
                dot_product += query_vector[idx] * val
                
        j_norm = job_norms[i]
        if q_norm > 0 and j_norm > 0:
            sim = dot_product / (q_norm * j_norm)
        else:
            sim = 0.0
        similarities.append(sim)
        
    # Rank jobs
    ranked_jobs = sorted(
        enumerate(similarities),
        key=lambda x: x[1],
        reverse=True
    )
    
    # Format matches
    results = []
    for job_idx, score in ranked_jobs:
        if score > 0.0:
            results.append((jobs[job_idx], score))
            
    return results[:limit]

# Reusable function to calculate the similarity score for a single specific job
def get_single_job_score(job, profile, jobs_list, matrix, cv, job_norms):
    try:
        target_idx = -1
        for idx, j in enumerate(jobs_list):
            if j['job_id'] == job['job_id']:
                target_idx = idx
                break
        if target_idx == -1:
            return 0
            
        skills_str = " ".join(profile['skills']) if isinstance(profile['skills'], list) else profile['skills']
        query_text = f"{profile['preferred_role']} {profile['preferred_category']} {skills_str}"
        tokens = re.findall(r'\b\w\w+\b', query_text.lower())
        vocab = cv['vocabulary_']
        query_vector = {}
        for token in tokens:
            if token in vocab:
                idx = vocab[token]
                query_vector[idx] = query_vector.get(idx, 0) + 1
                
        if not query_vector:
            return 0
            
        q_norm = math.sqrt(sum(v * v for v in query_vector.values()))
        start = matrix['indptr'][target_idx]
        end = matrix['indptr'][target_idx+1]
        
        row_indices = matrix['indices'][start:end]
        row_data = matrix['data'][start:end]
        
        dot_product = 0.0
        for idx, val in zip(row_indices, row_data):
            if idx in query_vector:
                dot_product += query_vector[idx] * val
                
        j_norm = job_norms[target_idx]
        if q_norm > 0 and j_norm > 0:
            sim = dot_product / (q_norm * j_norm)
            return int(sim * 100)
        return 0
    except Exception:
        return 0

# Helper to clean and render HTML safely to bypass Streamlit's markdown code-block conversion of indented HTML
def render_html(html_str):
    cleaned = "\n".join(line.strip() for line in html_str.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

# NLP Helpers for Chatbot
def extract_skills_from_text(text, unique_skills):
    norm_text = text.lower().replace(",", " ").replace(";", " ").replace(".", " ")
    matched = []
    # Match longer skills first to avoid partial conflicts (e.g. 'machine learning' matches before 'learning')
    sorted_skills = sorted(list(unique_skills), key=len, reverse=True)
    
    for skill in sorted_skills:
        norm_skill = skill.lower()
        if not norm_skill:
            continue
        
        # Whole word match regex handling special characters like C++ or .NET
        if not re.search(r'\b[a-zA-Z0-9]', norm_skill): # symbols at start
            pattern = r'(?:^|\s)' + re.escape(norm_skill) + r'(?:\s|$|\b)'
        elif not re.search(r'[a-zA-Z0-9]$', norm_skill): # symbols at end
            pattern = r'\b' + re.escape(norm_skill) + r'(?:\s|$)'
        else:
            pattern = r'\b' + re.escape(norm_skill) + r'\b'
            
        if re.search(pattern, norm_text):
            matched.append(skill)
            # Remove from text to prevent sub-string overlaps
            norm_text = re.sub(pattern, " ", norm_text)
            
    return matched

def detect_category_from_text(text, categories):
    norm_text = text.lower()
    for cat in categories:
        cat_norm = cat.lower()
        cat_space = cat_norm.replace("-", " ")
        if cat_norm in norm_text or cat_space in norm_text:
            return cat
    return None

def detect_role_from_text(text, unique_titles):
    norm_text = text.lower()
    sorted_titles = sorted(list(unique_titles), key=len, reverse=True)
    for title in sorted_titles:
        norm_title = title.lower()
        pattern = r'\b' + re.escape(norm_title) + r'\b'
        if re.search(pattern, norm_text):
            return title
    return None

# Load Model Artifacts
jobs, job_matrix, cv, job_norms = load_all_model_artifacts()

if jobs is not None:
    # Build unique parameters lists
    all_categories = sorted(list(set(j['category'] for j in jobs)))
    all_titles = set(j['job_title'] for j in jobs)
    all_skills = set()
    for j in jobs:
        all_skills.update(j['job_skill_set'])
        
    # Standard Session State Configuration
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    if 'saved_jobs' not in st.session_state:
        st.session_state.saved_jobs = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': "Intern Candidate",
            'skills': ["Python", "SQL", "Pandas", "Machine Learning"],
            'preferred_role': "Data Scientist",
            'preferred_category': all_categories[1] if len(all_categories) > 1 else all_categories[0]
        }
    if 'selected_job_detail' not in st.session_state:
        st.session_state.selected_job_detail = None
    if 'users' not in st.session_state:
        st.session_state.users = {
            "intern@smartrec.com": {
                "password": "password123",
                "profile": st.session_state.user_profile.copy()
            }
        }

    # Navigation Routing Handler
    def navigate_to(page_name, detail_job=None):
        st.session_state.current_page = page_name
        if detail_job is not None:
            st.session_state.selected_job_detail = detail_job
        st.rerun()

    # Dynamic Compass SVG Renderer
    def render_compass_svg(top_matches):
        roles = []
        scores = []
        for m in top_matches[:4]:
            roles.append(m[0]['job_title'])
            scores.append(int(m[1] * 100))
        
        while len(roles) < 4:
            roles.append("Career Path")
            scores.append(0)
            
        svg = f"""
        <svg viewBox="0 0 500 500" width="100%" height="400" style="background: transparent; font-family: 'Outfit', sans-serif;">
            <defs>
                <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="5" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
                <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 2 L 10 5 L 0 8 z" fill="#0ea5e9" />
                </marker>
            </defs>
            
            <!-- Circular match rings -->
            <circle cx="250" cy="250" r="180" stroke="rgba(14, 165, 233, 0.12)" stroke-width="1.5" fill="none" stroke-dasharray="6,4" />
            <circle cx="250" cy="250" r="110" stroke="rgba(99, 102, 241, 0.12)" stroke-width="1.5" fill="none" />
            
            <!-- Axes Grid Lines -->
            <line x1="250" y1="80" x2="250" y2="420" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1.5" />
            <line x1="80" y1="250" x2="420" y2="250" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1.5" />
            
            <!-- Center Node (Your Skills) -->
            <circle cx="250" cy="250" r="42" fill="url(#center-grad)" stroke="#6366f1" stroke-width="2" filter="url(#glow)" />
            <defs>
                <radialGradient id="center-grad" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#818cf8" />
                    <stop offset="100%" stop-color="#4f46e5" />
                </radialGradient>
            </defs>
            <text x="250" y="246" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700" letter-spacing="1">YOUR</text>
            <text x="250" y="259" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700" letter-spacing="1">SKILLS</text>
            
            <!-- Connector lines to matching nodes -->
            <line x1="250" y1="195" x2="250" y2="105" stroke="#0ea5e9" stroke-width="2.5" marker-end="url(#arrow)" />
            <line x1="305" y1="250" x2="395" y2="250" stroke="#0ea5e9" stroke-width="2.5" marker-end="url(#arrow)" />
            <line x1="250" y1="305" x2="250" y2="395" stroke="#0ea5e9" stroke-width="2.5" marker-end="url(#arrow)" />
            <line x1="195" y1="250" x2="105" y2="250" stroke="#0ea5e9" stroke-width="2.5" marker-end="url(#arrow)" />
            
            <!-- Nodes: North (Rank 1) -->
            <g transform="translate(250, 70)">
                <rect x="-80" y="-28" width="160" height="56" rx="10" fill="#ffffff" stroke="#0ea5e9" stroke-width="2" />
                <text x="0" y="-7" text-anchor="middle" fill="#0f172a" font-size="10" font-weight="700">{roles[0][:20]}</text>
                <text x="0" y="15" text-anchor="middle" fill="#059669" font-size="13" font-weight="700">{scores[0]}% Match</text>
            </g>
            
            <!-- Nodes: East (Rank 2) -->
            <g transform="translate(415, 250)">
                <rect x="-70" y="-26" width="140" height="52" rx="10" fill="#ffffff" stroke="#6366f1" stroke-width="1.5" />
                <text x="0" y="-6" text-anchor="middle" fill="#334155" font-size="9" font-weight="700">{roles[1][:16]}</text>
                <text x="0" y="13" text-anchor="middle" fill="#4f46e5" font-size="11" font-weight="700">{scores[1]}% Match</text>
            </g>
            
            <!-- Nodes: South (Rank 3) -->
            <g transform="translate(250, 430)">
                <rect x="-70" y="-26" width="140" height="52" rx="10" fill="#ffffff" stroke="#6366f1" stroke-width="1.5" />
                <text x="0" y="-6" text-anchor="middle" fill="#334155" font-size="9" font-weight="700">{roles[2][:16]}</text>
                <text x="0" y="13" text-anchor="middle" fill="#4f46e5" font-size="11" font-weight="700">{scores[2]}% Match</text>
            </g>
            
            <!-- Nodes: West (Rank 4) -->
            <g transform="translate(85, 250)">
                <rect x="-70" y="-26" width="140" height="52" rx="10" fill="#ffffff" stroke="#6366f1" stroke-width="1.5" />
                <text x="0" y="-6" text-anchor="middle" fill="#334155" font-size="9" font-weight="700">{roles[3][:16]}</text>
                <text x="0" y="13" text-anchor="middle" fill="#4f46e5" font-size="11" font-weight="700">{scores[3]}% Match</text>
            </g>
        </svg>
        """
        render_html(svg)

    # Reusable Match Card Renderer
    def render_job_card(job, score, key_prefix):
        # Format profile match score
        match_pct = int(score * 100)
        
        # Check if saved
        is_saved = job['job_id'] in st.session_state.saved_jobs
        
        # User profile matching highlight
        user_skills = set(s.lower() for s in st.session_state.user_profile['skills'])
        job_skills = job['job_skill_set']
        
        matched_skills = [s for s in job_skills if s.lower() in user_skills]
        
        card_html = f"""
        <div class="sr-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #0f172a; font-size: 18px;">{job['job_title']}</h4>
                <div class="match-badge">🎯 {match_pct}% Profile Match</div>
            </div>
            <div style="color: #0ea5e9; font-size: 13px; font-weight: 600; margin-bottom: 12px; letter-spacing: 0.5px;">{job['category']}</div>
            <p style="color: #475569; font-size: 13px; line-height: 1.5; margin-bottom: 16px;">
                {job['job_description'][:160]}...
            </p>
            <div style="margin-bottom: 20px;">
                <div style="color: #475569; font-size: 11px; font-weight: 700; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Matched Skills ({len(matched_skills)})</div>
                <div>
                    {" ".join([f'<span class="skill-chip skill-chip-matched">✓ {s}</span>' for s in matched_skills[:5]])}
                    {f'<span class="skill-chip" style="opacity: 0.6;">+{len(matched_skills) - 5} more</span>' if len(matched_skills) > 5 else ''}
                </div>
            </div>
        </div>
        """
        render_html(card_html)
        
        # Render action buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 Explore Role", key=f"exp_{key_prefix}_{job['job_id']}", use_container_width=True):
                navigate_to("job_details", job)
        with col2:
            if is_saved:
                if st.button("Remove Job", key=f"unsave_{key_prefix}_{job['job_id']}", use_container_width=True):
                    st.session_state.saved_jobs.remove(job['job_id'])
                    st.toast("Opportunity removed from Vault!", icon="🗑️")
                    st.rerun()
            else:
                if st.button("♡ Save Opportunity", key=f"save_{key_prefix}_{job['job_id']}", use_container_width=True):
                    st.session_state.saved_jobs.append(job['job_id'])
                    st.toast("Opportunity saved to Vault!", icon="💾")
                    st.rerun()

    # --- UI ROUTER PAGES ---

    # 1. LOGIN / SIGN UP
    if st.session_state.current_page == "login" and not st.session_state.authenticated:
        # Floating glows
        st.markdown('<div class="bg-glow-1"></div><div class="bg-glow-2"></div>', unsafe_allow_html=True)
        
        if 'auth_mode' not in st.session_state:
            st.session_state.auth_mode = "login"
            
        col_img, col_card = st.columns([1.2, 1])
        with col_img:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            import base64
            img_base64 = ""
            try:
                with open("career_search_light.jpg", "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
            except Exception:
                pass
            if img_base64:
                st.markdown(f'<img class="login-illustration" src="data:image/jpeg;base64,{img_base64}">', unsafe_allow_html=True)
            else:
                st.info("Loading illustration...")
        with col_card:
            # Single auth form
            with st.form("auth_form", clear_on_submit=False):
                # SVG animated compass logo & headings
                st.markdown("""
                <svg class="compass-logo" viewBox="0 0 100 100" width="80" height="80" style="margin: 0 auto 15px auto; display: block; filter: drop-shadow(0 0 8px rgba(14, 165, 233, 0.4));">
                    <circle cx="50" cy="50" r="45" stroke="#0ea5e9" stroke-width="2.5" fill="none" />
                    <circle cx="50" cy="50" r="40" stroke="rgba(99, 102, 241, 0.2)" stroke-width="1" fill="none" stroke-dasharray="2,2" />
                    <text x="50" y="15" text-anchor="middle" fill="#0ea5e9" font-size="8" font-weight="bold" font-family="'Outfit'">N</text>
                    <text x="88" y="53" text-anchor="middle" fill="#4f46e5" font-size="8" font-weight="bold" font-family="'Outfit'">E</text>
                    <text x="50" y="91" text-anchor="middle" fill="#4f46e5" font-size="8" font-weight="bold" font-family="'Outfit'">S</text>
                    <text x="12" y="53" text-anchor="middle" fill="#4f46e5" font-size="8" font-weight="bold" font-family="'Outfit'">W</text>
                    <g class="needle-group">
                        <path d="M50,50 L47,22 L50,17 L53,22 Z" fill="#0ea5e9" />
                        <path d="M50,50 L47,78 L50,83 L53,78 Z" fill="#475569" />
                        <circle cx="50" cy="50" r="4" fill="#ffffff" stroke="#6366f1" stroke-width="1.5" />
                    </g>
                </svg>
                <div style="text-align: center; margin-bottom: 25px;">
                    <div style="font-family: 'Outfit', sans-serif; font-size: 28px; font-weight: 800; color: #0f172a; letter-spacing: 2px; line-height: 1.2;">SMARTREC</div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; color: #0284c7; letter-spacing: 1px; margin-top: 4px;">Your Career Compass</div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 13px; font-style: italic; color: #475569; margin-top: 8px;">"Find where your skills can take you."</div>
                </div>
                """, unsafe_allow_html=True)
                
                auth_mode = st.session_state.auth_mode
                
                if auth_mode == "login":
                    email = st.text_input("Email", placeholder="enter your email", key="login_email")
                    password = st.text_input("Password", type="password", placeholder="enter your password", key="login_pass")
                    submit_label = "Sign In"
                else:
                    new_name = st.text_input("Full Name", placeholder="John Doe", key="signup_name")
                    email = st.text_input("Email Address", placeholder="john@example.com", key="signup_email")
                    password = st.text_input("Password", type="password", placeholder="create password", key="signup_pass")
                    submit_label = "Create Account"
                    
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                submit_auth = st.form_submit_button(submit_label, use_container_width=True)
                
            # Mode toggle links (rendered outside form, inside column)
            if auth_mode == "login":
                if st.button("Don't have an account? Create Account", key="toggle_to_signup", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()
            else:
                if st.button("Already have an account? Sign In", key="toggle_to_login", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
            
            # Form submission actions
            if submit_auth:
                if auth_mode == "login":
                    if not email or not password:
                        st.error("Please enter both email and password.")
                    elif email in st.session_state.users and st.session_state.users[email]["password"] == password:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_profile = st.session_state.users[email]["profile"]
                        st.session_state.current_page = "dashboard"
                        st.toast("Logged in successfully!", icon="🔑")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
                else:
                    if not new_name or not email or not password:
                        st.error("All fields are required.")
                    elif email in st.session_state.users:
                        st.error("Email address already registered.")
                    else:
                        # Register user
                        st.session_state.users[email] = {
                            "password": password,
                            "profile": {
                                'name': new_name,
                                'skills': ["Python", "SQL", "Pandas", "Machine Learning"],
                                'preferred_role': "Data Scientist",
                                'preferred_category': all_categories[1] if len(all_categories) > 1 else all_categories[0]
                            }
                        }
                        st.session_state.auth_mode = "login"
                        st.toast("Account created successfully! Please sign in.", icon="✓")
                        st.rerun()
                        
    # Authenticated Main Area Layout
    elif st.session_state.authenticated:
        # Render Sidebar
        with st.sidebar:
            st.markdown('<div class="sidebar-logo">SMARTREC</div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-tagline">Your Career Compass</div>', unsafe_allow_html=True)
            st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
            
            nav_items = [
                ("🧭 Career Compass", "dashboard"),
                ("🎯 Discover Jobs", "discover"),
                ("✦ SmartRec Guide", "chatbot"),
                ("🔎 Explore", "explore"),
                ("♡ Opportunity Vault", "vault"),
                ("📊 Career Insights", "insights"),
                ("🧠 Model Insights", "model_insights"),
                ("👤 My Profile", "profile"),
                ("ℹ About", "about"),
                ("⚙️ Settings", "settings"),
                ("🚪 Logout", "logout")
            ]
            
            for label, page_id in nav_items:
                if st.button(label, key=f"nav_{page_id}", use_container_width=True):
                    if page_id == "logout":
                        st.session_state.authenticated = False
                        st.session_state.user_email = None
                        st.session_state.current_page = "login"
                        st.toast("Logged out successfully!", icon="🚪")
                        st.rerun()
                    else:
                        st.session_state.current_page = page_id
                        st.rerun()
                        
        # 🧭 DASHBOARD PAGE
        if st.session_state.current_page == "dashboard":
            st.markdown("# 🧭 Career Compass Dashboard")
            st.markdown("##### Discover where your skills can take you.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            # Fetch active matches
            prof = st.session_state.user_profile
            matches = get_recommendations(
                prof['skills'], prof['preferred_role'], prof['preferred_category'],
                jobs, job_matrix, cv, job_norms, limit=5
            )
            
            col_left, col_right = st.columns([1.1, 0.9])
            
            with col_left:
                # User profile stats & skills chips
                st.markdown(f"### Welcome back, **{prof['name']}**")
                st.markdown("<div style='margin-bottom: 15px;'>Your Active Skills Profile:</div>", unsafe_allow_html=True)
                
                # Show skill chips
                skills_html = ""
                for skill in prof['skills']:
                    skills_html += f'<span class="skill-chip skill-chip-matched">{skill}</span>'
                st.markdown(f"<div>{skills_html}</div><br>", unsafe_allow_html=True)
                
                if not matches:
                    st.info("💡 Fill out your profile with skills like Python or SQL to find career matches.")
                else:
                    st.markdown("### 🎯 YOUR CAREER MATCH")
                    top_job, top_score = matches[0]
                    top_pct = int(top_score * 100)
                    
                    matched_skills = [s for s in top_job['job_skill_set'] if s.lower() in [sk.lower() for sk in prof['skills']]]
                    
                    # Highlight Card
                    highlight_card_html = f"""
                    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.06), rgba(14, 165, 233, 0.03)); border: 1.5px solid rgba(14, 165, 233, 0.2); border-radius: 16px; padding: 24px; margin-bottom: 25px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <h4 style="margin: 0; color: #0f172a; font-size: 20px;">{top_job['job_title']}</h4>
                            <div class="match-badge" style="font-size: 14px;">🎯 {top_pct}% Profile Match</div>
                        </div>
                        <div style="color: #0ea5e9; font-size: 14px; font-weight: 600; margin-bottom: 12px;">{top_job['category']}</div>
                        <p style="color: #475569; font-size: 13.5px; line-height: 1.5; margin-bottom: 16px;">{top_job['job_description'][:220]}...</p>
                        <div style="margin-bottom: 20px;">
                            <div style="color: #475569; font-size: 11px; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Matched Skills ({len(matched_skills)})</div>
                            <div>
                                {" ".join([f'<span class="skill-chip skill-chip-matched">✓ {s}</span>' for s in matched_skills[:5]])}
                                {f'<span class="skill-chip" style="opacity: 0.6;">+{len(matched_skills) - 5} more</span>' if len(matched_skills) > 5 else ''}
                            </div>
                        </div>
                    </div>
                    """
                    render_html(highlight_card_html)
                    
                    # Action buttons
                    bcol1, bcol2 = st.columns([1, 1])
                    with bcol1:
                        if st.button("Explore Top Role Match", key="explore_top_role", use_container_width=True):
                            navigate_to("job_details", top_job)
                    with bcol2:
                        is_saved = top_job['job_id'] in st.session_state.saved_jobs
                        if is_saved:
                            if st.button("Remove from Vault", key="unsave_top_role", use_container_width=True):
                                st.session_state.saved_jobs.remove(top_job['job_id'])
                                st.rerun()
                        else:
                            if st.button("♡ Save Match", key="save_top_role", use_container_width=True):
                                st.session_state.saved_jobs.append(top_job['job_id'])
                                st.rerun()
            
            with col_right:
                if matches:
                    st.markdown("<h3 style='text-align: center;'>Career Pathway Compass</h3>", unsafe_allow_html=True)
                    render_compass_svg(matches)
            
            # Next best matches row
            if len(matches) > 1:
                st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin: 30px 0;'>", unsafe_allow_html=True)
                st.markdown("### 🧭 NEXT BEST MATCHES")
                
                # Render 3 matches in columns
                nb_cols = st.columns(3)
                for i, (job, score) in enumerate(matches[1:4]):
                    with nb_cols[i]:
                        pct = int(score * 100)
                        nb_card_html = f"""
                        <div class="sr-card" style="height: 100%;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <h5 style="margin: 0; font-size: 15px; color: #0f172a;">{job['job_title']}</h5>
                                <span style="color: #059669; font-weight: 700; font-size: 13px;">{pct}% Match</span>
                            </div>
                            <div style="color: #0ea5e9; font-size: 11px; margin-bottom: 12px;">{job['category']}</div>
                            <p style="color: #475569; font-size: 12px; height: 60px; overflow: hidden; line-height: 1.4; margin-bottom: 16px;">
                                {job['job_description'][:100]}...
                            </p>
                        </div>
                        """
                        render_html(nb_card_html)
                        if st.button(f"Explore {job['job_title'][:15]}...", key=f"exp_nb_{job['job_id']}", use_container_width=True):
                            navigate_to("job_details", job)

        # 🎯 DISCOVER JOBS PAGE
        elif st.session_state.current_page == "discover":
            st.markdown("# 🎯 Discover Your Next Opportunity")
            st.markdown("##### Tell us what you know. We'll find where it fits.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            # Input Form inside container
            with st.container(border=True):
                icol1, icol2 = st.columns([1, 1])
                with icol1:
                    input_skills = st.text_input("Your Skills", value=", ".join(st.session_state.user_profile['skills']), help="Comma-separated skills (e.g. Python, SQL, Pandas)")
                    input_role = st.text_input("Preferred Job Role", value=st.session_state.user_profile['preferred_role'])
                with icol2:
                    input_category = st.selectbox("Preferred Job Category", options=all_categories, index=all_categories.index(st.session_state.user_profile['preferred_category']))
                
                parsed_input_skills = [s.strip() for s in input_skills.split(",") if s.strip()]
                
                st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
                find_matches = st.button("✨ Find My Matches", use_container_width=True)
            
            # Run Recommendations
            if find_matches or 'discover_results' not in st.session_state:
                with st.spinner("Analyzing skill matrix..."):
                    results = get_recommendations(
                        parsed_input_skills, input_role, input_category,
                        jobs, job_matrix, cv, job_norms, limit=10
                    )
                    st.session_state.discover_results = results
            
            # Show Results
            results = st.session_state.discover_results
            if not results:
                st.warning("No matches found. Try entering alternative skills or category keywords.")
            else:
                st.markdown(f"### Top {len(results)} Recommendations")
                
                # Render cards in 2-column grid
                card_cols = st.columns(2)
                for idx, (job, score) in enumerate(results):
                    col_index = idx % 2
                    with card_cols[col_index]:
                        render_job_card(job, score, "discover")
                        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # ✦ SMARTREC GUIDE (CHATBOT) PAGE
        elif st.session_state.current_page == "chatbot":
            st.markdown("# ✦ SmartRec Guide")
            st.markdown("##### Your skills. Your possibilities.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            # Setup suggestion prompts
            suggestions = [
                "💡 Jobs for Python",
                "💡 Jobs for Python + SQL",
                "💡 What can I do with Machine Learning?",
                "💡 Show me Data Science jobs",
                "💡 Help me find my best career match"
            ]
            
            # Handle prompt submissions
            user_msg = None
            
            # Show prompt suggestions as inline pills
            st.markdown("###### Suggested Questions:")
            sug_cols = st.columns(len(suggestions))
            for i, sug in enumerate(suggestions):
                with sug_cols[i]:
                    st.markdown('<div class="prompt-btn">', unsafe_allow_html=True)
                    if st.button(sug, key=f"sug_{i}"):
                        user_msg = sug[2:] # Strip the emoji
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            # Chat Container
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f'<div class="chat-bubble-user">{msg["text"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble-guide">{msg["text"]}</div>', unsafe_allow_html=True)
                    # Render embedded jobs list if present in message data
                    if 'matched_jobs' in msg:
                        for job, score in msg['matched_jobs']:
                            st.markdown(f"""
                            <div class="sr-card" style="margin: 10px 40px; padding: 18px; border-color: rgba(99, 102, 241, 0.25);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <h5 style="margin: 0; color: #ffffff; font-size: 15px;">{job['job_title']}</h5>
                                    <span style="color: #10b981; font-weight: 700; font-size: 12px;">{int(score*100)}% Match</span>
                                </div>
                                <div style="color: #38bdf8; font-size: 11px; margin-bottom: 8px;">{job['category']}</div>
                                <p style="color: #94a3b8; font-size: 12px; line-height: 1.4; margin-bottom: 12px;">{job['job_description'][:110]}...</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Small button grid
                            bc1, bc2 = st.columns([1, 1])
                            with bc1:
                                if st.button("Explore", key=f"chat_exp_{job['job_id']}_{msg.get('msg_id', 0)}", use_container_width=True):
                                    navigate_to("job_details", job)
                            with bc2:
                                is_saved = job['job_id'] in st.session_state.saved_jobs
                                if is_saved:
                                    if st.button("Saved ✓", key=f"chat_saved_{job['job_id']}_{msg.get('msg_id', 0)}", disabled=True, use_container_width=True):
                                        pass
                                else:
                                    if st.button("Save ♡", key=f"chat_save_{job['job_id']}_{msg.get('msg_id', 0)}", use_container_width=True):
                                        st.session_state.saved_jobs.append(job['job_id'])
                                        st.toast("Opportunity saved!", icon="💾")
                                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Input Area
            with st.form("chat_form", clear_on_submit=True):
                col_text, col_sub = st.columns([6, 1])
                with col_text:
                    chat_in = st.text_input("Ask about jobs, roles, or skill combinations...", placeholder="I know Python, SQL and Machine Learning but I don't know what job suits me.", label_visibility="collapsed")
                with col_sub:
                    submit_chat = st.form_submit_button("Send")
                    
            if submit_chat and chat_in:
                user_msg = chat_in
                
            # Process User Message
            if user_msg:
                st.session_state.chat_history.append({'role': 'user', 'text': user_msg})
                
                # Check for NLP triggers
                extracted_skills = extract_skills_from_text(user_msg, all_skills)
                extracted_role = detect_role_from_text(user_msg, all_titles)
                extracted_category = detect_category_from_text(user_msg, all_categories)
                
                # Default matching parameters fallback to user profile
                skills_to_use = extracted_skills if extracted_skills else st.session_state.user_profile['skills']
                role_to_use = extracted_role if extracted_role else st.session_state.user_profile['preferred_role']
                cat_to_use = extracted_category if extracted_category else st.session_state.user_profile['preferred_category']
                
                # Determine responses
                # General conversation filter
                general_conversation_check = re.search(
                    r'\b(hello|hi|hey|greetings|help|explain|what is|how do|who are you|clear|settings)\b', 
                    user_msg.lower()
                )
                
                msg_id = len(st.session_state.chat_history)
                
                # Scope check: Is it career related?
                career_keywords = [
                    'job', 'career', 'work', 'employ', 'skill', 'role', 'title', 'position', 'recommend', 
                    'python', 'sql', 'pandas', 'machine learning', 'developer', 'analyst', 'manager', 
                    'resume', 'cv', 'intern', 'finance', 'sales', 'hr', 'marketing'
                ]
                is_career_related = any(k in user_msg.lower() for k in career_keywords) or extracted_skills or extracted_role or extracted_category
                
                if not is_career_related:
                    resp_text = "I'm your SmartRec Career Guide. I can help you discover jobs based on your skills, preferred roles and job categories. Try asking about a skill like 'Python' or a role like 'Data Scientist'."
                    st.session_state.chat_history.append({'role': 'assistant', 'text': resp_text, 'msg_id': msg_id})
                else:
                    # Run matching
                    results = get_recommendations(
                        skills_to_use, role_to_use, cat_to_use,
                        jobs, job_matrix, cv, job_norms, limit=5
                    )
                    
                    if not results:
                        resp_text = "I analyzed the dataset but couldn't find any direct matches. Could you specify other skills or categories?"
                        st.session_state.chat_history.append({'role': 'assistant', 'text': resp_text, 'msg_id': msg_id})
                    else:
                        # Custom responses based on what was detected
                        if extracted_skills and not extracted_role and not extracted_category:
                            resp_text = f"Based on your skills ({', '.join(extracted_skills)}), I found these career matches that align with your background:"
                        elif extracted_role and not extracted_skills:
                            resp_text = f"Here are opportunities in our dataset that align with your interest in becoming a **{extracted_role}**:"
                        elif extracted_category and not extracted_skills and not extracted_role:
                            resp_text = f"I found several opportunities in the **{extracted_category}** field:"
                        else:
                            resp_text = "I analyzed your profile query and found these top career directions matching your skillset:"
                            
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'text': resp_text,
                            'matched_jobs': results,
                            'msg_id': msg_id
                        })
                        
                st.rerun()
                
            # Follow-up clickable suggestion options
            if st.session_state.chat_history:
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                st.markdown("###### Quick Follow-ups:")
                fcol1, fcol2, fcol3, fcol4 = st.columns(4)
                with fcol1:
                    if st.button("Explore Data Science roles", key="f_ds"):
                        st.session_state.chat_history.append({'role': 'user', 'text': "Show me Data Science jobs"})
                        results = get_recommendations([], "Data Scientist", "FINANCE", jobs, job_matrix, cv, job_norms, limit=5)
                        st.session_state.chat_history.append({'role': 'assistant', 'text': "Here are opportunities that align with Data Science roles:", 'matched_jobs': results, 'msg_id': len(st.session_state.chat_history)})
                        st.rerun()
                with fcol2:
                    if st.button("Find jobs requiring Python", key="f_py"):
                        st.session_state.chat_history.append({'role': 'user', 'text': "Find jobs requiring Python"})
                        results = get_recommendations(["Python"], "", "", jobs, job_matrix, cv, job_norms, limit=5)
                        st.session_state.chat_history.append({'role': 'assistant', 'text': "Here are job matches requiring Python skills:", 'matched_jobs': results, 'msg_id': len(st.session_state.chat_history)})
                        st.rerun()
                with fcol3:
                    if st.button("Update my skills profile", key="f_prof"):
                        navigate_to("profile")
                with fcol4:
                    if st.button("Clear Chat History", key="f_clear"):
                        st.session_state.chat_history = []
                        st.rerun()

        # 🔎 EXPLORE PAGE
        elif st.session_state.current_page == "explore":
            st.markdown("# 🔎 Explore All Opportunities")
            st.markdown("##### Search and filter through the complete job directory.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            # Search & Filter widgets inside card
            with st.container(border=True):
                sfcol1, sfcol2, sfcol3, sfcol4 = st.columns([1.5, 1, 1, 1])
                with sfcol1:
                    search_title = st.text_input("Search Job Title", placeholder="e.g. Developer, HR, Manager")
                with sfcol2:
                    search_skills = st.text_input("Search by Skill", placeholder="e.g. SQL, Excel")
                with sfcol3:
                    filter_cat = st.selectbox("Category Filter", options=["All Categories"] + all_categories)
                with sfcol4:
                    sort_by = st.selectbox("Sort By", options=["Job Title", "Category"])
            
            # Filter Data
            filtered_jobs = []
            for j in jobs:
                # Title Match
                title_match = not search_title or search_title.lower() in j['job_title'].lower()
                
                # Skills Match
                skill_match = not search_skills or any(search_skills.lower() in s.lower() for s in j['job_skill_set'])
                
                # Category Filter Match
                cat_match = filter_cat == "All Categories" or j['category'] == filter_cat
                
                if title_match and skill_match and cat_match:
                    filtered_jobs.append(j)
                    
            # Sorting
            if sort_by == "Job Title":
                filtered_jobs.sort(key=lambda x: x['job_title'])
            else:
                filtered_jobs.sort(key=lambda x: x['category'])
                
            # Renders Grid of Results
            if not filtered_jobs:
                st.warning("No matches found. Adjust your search criteria.")
            else:
                st.markdown(f"##### Showing {len(filtered_jobs)} Job Roles")
                
                # Renders matching roles inside list
                for j in filtered_jobs[:20]: # Limit rendering to top 20 for performance
                    exp_card_html = f"""
                    <div class="sr-card" style="margin-bottom: 12px; padding: 18px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h5 style="margin: 0; color: #0f172a; font-size: 16px;">{j['job_title']}</h5>
                                <span style="color: #0ea5e9; font-size: 12px;">{j['category']}</span>
                            </div>
                        </div>
                    </div>
                    """
                    render_html(exp_card_html)
                    
                    # Layout grid for small buttons
                    ec1, ec2 = st.columns([1, 4])
                    with ec1:
                        if st.button("Explore Details", key=f"explore_dt_{j['job_id']}", use_container_width=True):
                            navigate_to("job_details", j)
                    with ec2:
                        is_saved = j['job_id'] in st.session_state.saved_jobs
                        if is_saved:
                            if st.button("Remove Opportunity", key=f"explore_rm_{j['job_id']}", use_container_width=False):
                                st.session_state.saved_jobs.remove(j['job_id'])
                                st.toast("Removed from vault!", icon="🗑")
                                st.rerun()
                        else:
                            if st.button("Save ♡", key=f"explore_sv_{j['job_id']}", use_container_width=False):
                                st.session_state.saved_jobs.append(j['job_id'])
                                st.toast("Saved opportunity!", icon="💾")
                                st.rerun()
                                
                if len(filtered_jobs) > 20:
                    st.info(f"Showing top 20 of {len(filtered_jobs)} results. Narrow your search terms to find specific matches.")

        # ♡ OPPORTUNITY VAULT PAGE
        elif st.session_state.current_page == "vault":
            st.markdown("# ♡ Opportunity Vault")
            st.markdown("##### Your saved opportunities. Track your next career options.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            saved_ids = st.session_state.saved_jobs
            if not saved_ids:
                st.info("You haven't saved any career opportunities yet. Explore matches and click 'Save Opportunity' to save them here.")
            else:
                saved_records = [j for j in jobs if j['job_id'] in saved_ids]
                
                # Draw list of saved jobs
                for job in saved_records:
                    score_pct = get_single_job_score(
                        job, 
                        st.session_state.user_profile, 
                        jobs, job_matrix, cv, job_norms
                    )
                    
                    st.markdown(f"""
                    <div class="sr-card" style="padding: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <h4 style="margin: 0; color: #0f172a; font-size: 18px;">{job['job_title']}</h4>
                            <span class="match-badge">🎯 {score_pct}% Match</span>
                        </div>
                        <div style="color: #0ea5e9; font-size: 12px; margin-bottom: 12px;">{job['category']}</div>
                        <p style="color: #475569; font-size: 13px; margin-bottom: 16px;">{job['job_description'][:180]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Buttons
                    vcol1, vcol2 = st.columns([1, 4])
                    with vcol1:
                        if st.button("Explore Details", key=f"vault_exp_{job['job_id']}", use_container_width=True):
                            navigate_to("job_details", job)
                    with vcol2:
                        if st.button("Remove from Vault", key=f"vault_rm_{job['job_id']}", use_container_width=False):
                            st.session_state.saved_jobs.remove(job['job_id'])
                            st.toast("Removed from Vault!", icon="🗑️")
                            st.rerun()

        # 📊 CAREER INSIGHTS PAGE
        elif st.session_state.current_page == "insights":
            st.markdown("# 📊 Career Insights")
            st.markdown("##### Real analytics computed directly from our job directory.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            # Computing dataset statistics
            total_jobs = len(jobs)
            num_categories = len(all_categories)
            
            # Category counts
            category_counts = {}
            for j in jobs:
                cat = j['category']
                category_counts[cat] = category_counts.get(cat, 0) + 1
                
            # Most common job titles
            title_counts = {}
            for j in jobs:
                title = j['job_title']
                title_counts[title] = title_counts.get(title, 0) + 1
            most_common_titles = sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Most common skill requirements
            skill_counts = {}
            for j in jobs:
                for s in j['job_skill_set']:
                    skill_counts[s] = skill_counts.get(s, 0) + 1
            most_common_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Layout Grid
            icol1, icol2 = st.columns(2)
            with icol1:
                st.markdown(f"""
                <div class="sr-card" style="text-align: center; height: 130px;">
                    <div style="font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">Total Opportunities Available</div>
                    <div style="font-size: 40px; font-weight: 800; color: #38bdf8; font-family: 'Outfit';">{total_jobs}</div>
                </div>
                """, unsafe_allow_html=True)
            with icol2:
                st.markdown(f"""
                <div class="sr-card" style="text-align: center; height: 130px;">
                    <div style="font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">Primary Job Categories</div>
                    <div style="font-size: 40px; font-weight: 800; color: #6366f1; font-family: 'Outfit';">{num_categories}</div>
                </div>
                """, unsafe_allow_html=True)
                
            col_chart1, col_chart2 = st.columns([1.1, 0.9])
            with col_chart1:
                st.markdown("### Job Distributions by Category")
                # Custom horizontal bar chart SVG
                cat_chart_svg = f"""
                <svg viewBox="0 0 600 320" width="100%" height="280" style="background: transparent; font-family: 'Outfit', sans-serif;">
                    <defs>
                        <linearGradient id="bar-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#6366f1" />
                            <stop offset="100%" stop-color="#0ea5e9" />
                        </linearGradient>
                    </defs>
                """
                y = 20
                sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
                max_cat_count = max(category_counts.values()) if category_counts else 1
                for cat, count in sorted_cats:
                    bar_width = int((count / max_cat_count) * 320)
                    pct = (count / total_jobs) * 100
                    cat_label = cat.replace("-", " ")
                    cat_label = cat_label[:24] + "..." if len(cat_label) > 24 else cat_label
                    cat_chart_svg += f"""
                    <text x="15" y="{y+16}" fill="#94a3b8" font-size="12" font-weight="500">{cat_label}</text>
                    <rect x="200" y="{y}" width="{bar_width}" height="22" rx="4" fill="url(#bar-grad)" />
                    <text x="{200 + bar_width + 10}" y="{y+15}" fill="#38bdf8" font-size="12" font-weight="700">{count} ({pct:.1f}%)</text>
                    """
                    y += 50
                cat_chart_svg += "</svg>"
                render_html(cat_chart_svg)
                
            with col_chart2:
                st.markdown("### Most In-Demand Skills")
                # Custom vertical/horizontal bar list for skills
                skills_chart_svg = f"""
                <svg viewBox="0 0 500 320" width="100%" height="280" style="background: transparent; font-family: 'Outfit', sans-serif;">
                    <defs>
                        <linearGradient id="skill-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#10b981" />
                            <stop offset="100%" stop-color="#059669" />
                        </linearGradient>
                    </defs>
                """
                y = 15
                max_skill_count = max(c for s, c in most_common_skills) if most_common_skills else 1
                for skill, count in most_common_skills[:8]:
                    bar_width = int((count / max_skill_count) * 260)
                    skills_chart_svg += f"""
                    <text x="15" y="{y+14}" fill="#94a3b8" font-size="11" font-weight="500">{skill[:18]}</text>
                    <rect x="150" y="{y}" width="{bar_width}" height="18" rx="3" fill="url(#skill-grad)" />
                    <text x="{150 + bar_width + 8}" y="{y+13}" fill="#10b981" font-size="11" font-weight="700">{count}</text>
                    """
                    y += 36
                skills_chart_svg += "</svg>"
                render_html(skills_chart_svg)
                
            # Most common job titles list
            st.markdown("### 👑 Most Frequent Job Roles")
            title_cols = st.columns(5)
            for i, (title, count) in enumerate(most_common_titles):
                with title_cols[i]:
                    freq_card_html = f"""
                    <div class="sr-card" style="text-align: center; padding: 15px; height: 120px;">
                        <div style="font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 6px; overflow: hidden; height: 16px;">{title[:20]}</div>
                        <div style="font-size: 26px; font-weight: 800; color: #0284c7; font-family: 'Outfit';">{count}</div>
                        <div style="font-size: 11px; color: #475569;">Job Openings</div>
                    </div>
                    """
                    render_html(freq_card_html)

        # 👤 MY PROFILE PAGE
        elif st.session_state.current_page == "profile":
            st.markdown("# 👤 My Career Profile")
            st.markdown("##### Build and update your profile to align your matches correctly.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            prof = st.session_state.user_profile
            
            with st.form("profile_form"):
                prof_name = st.text_input("Full Name", value=prof['name'])
                
                # Checkbox selection from unique skills or standard text list
                standard_skills = [
                    "Python", "SQL", "Pandas", "Machine Learning", "Data Analysis", 
                    "Tableau", "Power BI", "Excel", "Project Management", "Communication",
                    "Java", "C++", "HTML", "CSS", "Git", "Cloud Platforms", "AWS"
                ]
                
                st.markdown("Select Skills")
                selected_skills = []
                skill_cols = st.columns(4)
                for i, skill in enumerate(standard_skills):
                    col_idx = i % 4
                    with skill_cols[col_idx]:
                        if st.checkbox(skill, value=skill in prof['skills'], key=f"prof_skill_{skill}"):
                            selected_skills.append(skill)
                            
                # Custom skill write-ins
                custom_skills_input = st.text_input("Additional Skills (comma-separated)", value=", ".join([s for s in prof['skills'] if s not in standard_skills]))
                
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                
                col_r, col_c = st.columns(2)
                with col_r:
                    prof_role = st.text_input("Preferred Role", value=prof['preferred_role'])
                with col_c:
                    prof_cat = st.selectbox("Preferred Category", options=all_categories, index=all_categories.index(prof['preferred_category']))
                
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                save_profile = st.form_submit_button("Update Profile & Refresh Matches")
                
            if save_profile:
                # Add custom write-ins
                write_ins = [s.strip() for s in custom_skills_input.split(",") if s.strip()]
                for ws in write_ins:
                    if ws not in selected_skills:
                        selected_skills.append(ws)
                        
                # Update session states
                updated_profile = {
                    'name': prof_name,
                    'skills': selected_skills,
                    'preferred_role': prof_role,
                    'preferred_category': prof_cat
                }
                
                st.session_state.user_profile = updated_profile
                # Save to user database
                st.session_state.users[st.session_state.user_email]["profile"] = updated_profile
                
                st.toast("Profile updated successfully!", icon="👤")
                st.success("Your career profile has been updated! Moving to dashboard to refresh career compass matches...")
                navigate_to("dashboard")

        # ⚙️ SETTINGS PAGE
        elif st.session_state.current_page == "settings":
            st.markdown("# ⚙️ Settings")
            st.markdown("##### Manage your session state, vault options, and chat histories.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### 💾 Storage & Chat History")
                st.write("Reset application data to original state.")
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                
                # Settings Actions
                if st.button("Clear Opportunity Vault", key="set_clear_vault", use_container_width=True):
                    st.session_state.saved_jobs = []
                    st.toast("Saved opportunities vault cleared!", icon="🗑️")
                    
                if st.button("Clear Chat History", key="set_clear_chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.toast("Chat history cleared!", icon="💬")
                    
                if st.button("Reset Career Profile to Default", key="set_reset_profile", use_container_width=True):
                    st.session_state.user_profile = {
                        'name': st.session_state.users[st.session_state.user_email]["profile"]["name"],
                        'skills': ["Python", "SQL", "Pandas", "Machine Learning"],
                        'preferred_role': "Data Scientist",
                        'preferred_category': all_categories[1] if len(all_categories) > 1 else all_categories[0]
                    }
                    st.toast("Profile reset to Default!", icon="👤")
                    st.rerun()
                    
                st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin: 20px 0;'>", unsafe_allow_html=True)
                st.markdown("### 🔑 Account Management")
                if st.button("Log Out of Session", key="set_logout", use_container_width=True):
                    st.session_state.authenticated = False
                    st.session_state.user_email = None
                    st.session_state.current_page = "login"
                    st.rerun()
            


        # 🔎 JOB DETAILS PAGE (NESTED ROUTE)
        elif st.session_state.current_page == "job_details":
            job = st.session_state.selected_job_detail
            if job is None:
                navigate_to("dashboard")
                
            st.markdown(f"# 🔎 Job Role Details")
            st.markdown(f"##### Explored Career Role: {job['job_title']}")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            score_pct = get_single_job_score(
                job, 
                st.session_state.user_profile, 
                jobs, job_matrix, cv, job_norms
            )
            
            # Skill matches & gaps
            user_skills = set(s.lower() for s in st.session_state.user_profile['skills'])
            job_skills = job['job_skill_set']
            matched_skills = [s for s in job_skills if s.lower() in user_skills]
            skill_gaps = [s for s in job_skills if s.lower() not in user_skills]
            
            # Renders details structure
            col_det1, col_det2 = st.columns([1.2, 0.8])
            
            with col_det1:
                det_html_1 = f"""
                <div class="sr-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <h2 style="margin:0; font-size: 24px; color: #0f172a;">{job['job_title']}</h2>
                        <div class="match-badge" style="font-size: 15px; padding: 6px 16px;">🎯 {score_pct}% Match</div>
                    </div>
                    <div style="color: #0ea5e9; font-size: 14px; font-weight: 600; margin-bottom: 20px;">{job['category']}</div>
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: #0f172a; font-size: 16px; margin-bottom: 8px;">Job Description</h4>
                        <div style="color: #475569; font-size: 13.5px; line-height: 1.6; white-space: pre-wrap;">{job['job_description']}</div>
                    </div>
                </div>
                """
                render_html(det_html_1)
                
                # Back button
                if st.button("← Back to Opportunities", use_container_width=True):
                    navigate_to("discover")
                    
            with col_det2:
                # Skill Analysis Card
                det_html_2 = f"""
                <div class="sr-card">
                    <h4 style="color: #0f172a; font-size: 16px; margin-bottom: 15px;">Match Breakdown</h4>
                    
                    <div style="margin-bottom: 20px;">
                        <div style="color: #059669; font-size: 11px; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">✓ Matched Skills ({len(matched_skills)})</div>
                        <div>
                            {" ".join([f'<span class="skill-chip skill-chip-matched">✓ {s}</span>' for s in matched_skills]) if matched_skills else '<div style="color:#64748b; font-size:12px; font-style:italic;">No matching skills detected</div>'}
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <div style="color: #b45309; font-size: 11px; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">⚠ Potential Skill Gaps ({len(skill_gaps)})</div>
                        <div>
                            {" ".join([f'<span class="skill-chip skill-chip-gap">? {s}</span>' for s in skill_gaps]) if skill_gaps else '<div style="color:#059669; font-size:12px; font-style:italic; font-weight:600;">✓ Perfect fit! Zero skill gaps detected</div>'}
                        </div>
                    </div>
                    
                    <hr style="border: 0; height: 1px; background: rgba(15, 23, 42, 0.06); margin: 20px 0;">
                    <div style="color: #475569; font-size: 12px;">Job Registry ID: <b>{job['job_id']}</b></div>
                </div>
                """
                render_html(det_html_2)
                
                # Save button
                is_saved = job['job_id'] in st.session_state.saved_jobs
                if is_saved:
                    if st.button("Remove from Vault", key="det_unsave", use_container_width=True):
                        st.session_state.saved_jobs.remove(job['job_id'])
                        st.toast("Opportunity removed from Vault!", icon="🗑️")
                        st.rerun()
                else:
                    if st.button("Save Opportunity ♡", key="det_save", use_container_width=True):
                        st.session_state.saved_jobs.append(job['job_id'])
                        st.toast("Opportunity saved to Vault!", icon="💾")
                        st.rerun()

        # 🧠 MODEL INSIGHTS PAGE
        elif st.session_state.current_page == "model_insights":
            st.markdown("# 🧠 Model Insights & Architecture")
            st.markdown("##### Discover the machine learning models and engineering behind SmartRec.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### ✦ Selected Matching Engine")
                st.write("**Model Architecture:** Content-Based Filtering")
                st.write("**Feature Extraction:** Count Vectorization (`CountVectorizer`)")
                st.write("**Similarity Metric:** Cosine Similarity Similarity Vectorization")
                st.write("**Evaluation Metric:** Precision@5")
                st.write("**Best Performance Score:** **88.0%**")
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### 📊 Model Comparison & Selection")
                st.write("We compared three pipeline approaches during algorithm selection. The performance scores under Precision@5 are detailed below:")
                
                # Render simple comparison table
                table_html = """
                <table style="width:100%; border-collapse: collapse; margin-top: 10px; font-family: 'Inter', sans-serif;">
                    <thead>
                        <tr style="border-bottom: 1px solid rgba(15, 23, 42, 0.08); text-align: left;">
                            <th style="padding: 10px; color: #0f172a;">Model Pipeline</th>
                            <th style="padding: 10px; color: #0f172a;">Precision@5</th>
                            <th style="padding: 10px; color: #0f172a;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid rgba(15, 23, 42, 0.04); background: rgba(99, 102, 241, 0.04);">
                            <td style="padding: 10px; font-weight: 600; color: #4f46e5;">Count Vectorizer + Cosine Similarity</td>
                            <td style="padding: 10px; font-weight: 600; color: #059669;">88.0%</td>
                            <td style="padding: 10px; color: #059669; font-weight: 600;">Selected (Best)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(15, 23, 42, 0.04);">
                            <td style="padding: 10px; color: #475569;">TF-IDF + Cosine Similarity</td>
                            <td style="padding: 10px; color: #475569;">84.5%</td>
                            <td style="padding: 10px; color: #475569;">Compared</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(15, 23, 42, 0.04);">
                            <td style="padding: 10px; color: #475569;">TF-IDF + Linear Kernel</td>
                            <td style="padding: 10px; color: #475569;">82.0%</td>
                            <td style="padding: 10px; color: #475569;">Compared</td>
                        </tr>
                    </tbody>
                </table>
                """
                render_html(table_html)
                
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### 🔬 Why Count Vectorizer & Cosine Similarity?")
                st.markdown("""
                * **Exact Keyword Matching**: Job descriptions and career profiles are characterized by key skill terms (e.g., *Python, SQL, AWS, Tableau*). 
                * **Count Vectorizer Advantage**: A simple term count vectorizer preserves direct token occurrence without penalizing terms that appear rarely across the corpus, which ensures skill alignment remains the strongest matching parameter.
                * **Cosine Similarity Directionality**: Cosine Similarity measures the angular distance between the user profile query vector and the job listings vectors. This measures overlap *direction* regardless of magnitude (i.e. length of the job listing text), ensuring short profiles match effectively against long job descriptions.
                """)

        # ℹ️ ABOUT PAGE
        elif st.session_state.current_page == "about":
            st.markdown("# ℹ️ About SmartRec")
            st.markdown("##### Technical overview, technology pipeline, and limitations.")
            st.markdown("<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### ✦ Project Overview")
                st.markdown("""
                **SmartRec (Your Career Compass)** is an intelligent recommendation portal that bridges the gap between candidates and jobs by analyzing skill alignments.
                
                **Problem Statement:** Legacy job portals match candidates using basic string searches, which often fails due to spelling differences, synonym variations, or word lengths.
                
                **Solution:** SmartRec builds vector representations of both candidate profiles and job requirements, computing cosine similarities to identify optimal alignments and highlight potential skill gaps.
                """)
                
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### ⚙️ Technology Stack")
                st.markdown("""
                * **Backend Core**: Python 3.11
                * **Frontend Interface**: Streamlit
                * **Natural Language Processing**: Regular Expressions (Regex) Custom Parser
                * **Recommendation engine**: Count Vectorization + Cosine Similarity (Pure Python vectors fallback)
                """)
                
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### ⚠️ Honest Limitations")
                st.markdown("""
                SmartRec uses content-based matching. Recommendations depend on the information available in the job dataset and therefore may not capture user behavior, real-time market demand, salary preferences, or collaborative preferences.
                """)

else:
    # Error state if files are missing
    st.error("❌ SmartRec model initialization failed.")
    st.info("Please make sure the required model artifacts are placed in the root directory:")
    st.markdown("""
    * `count_vectorizer.pkl`
    * `job_matrix.pkl`
    * `job_data.pkl`
    """)
