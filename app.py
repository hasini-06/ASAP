import streamlit as st
from pdf_qa import extract_text_from_pdf, chunk_text, build_faiss
from components.page_qa import render_qa_page
from components.page_study_plan import render_study_plan_page
from components.page_quiz import render_quiz_page
from components.page_history import render_history_page

# Page configuration
st.set_page_config(page_title="Smart PDF Assistant", layout="wide")

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    if "study_plan" not in st.session_state:
        st.session_state.study_plan = None
    if "quiz" not in st.session_state:
        st.session_state.quiz = []

init_session_state()

# Sidebar - PDF Upload
st.sidebar.title("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")

# Sidebar - Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Q&A", "Study Plan", "Quiz", "History"])

# Main application logic
if uploaded_file:
    with st.spinner("Reading and indexing PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        index, embeddings = build_faiss(chunks)
        st.sidebar.success("PDF processed")

    # Route to appropriate page
    if page == "Q&A":
        render_qa_page(text, chunks, index)
    elif page == "Study Plan":
        render_study_plan_page(text)
    elif page == "Quiz":
        render_quiz_page(text)
    elif page == "History":
        render_history_page()
else:
    st.warning("Please upload a PDF to get started.")