import streamlit as st
from pdf_qa import ask_llm


def render_study_plan_page(text):
    """Render the Study Plan page"""
    st.title("Personalized Study Plan")
    
    time_input = st.text_input("Available time (e.g., '2 hours', '3 days')")
    if st.button("Generate Plan") and time_input:
        plan = ask_llm(
            f"Create a detailed study plan based on this content:\n\n{text[:3000]}\n\nTime available: {time_input}\n\nStudy Plan:"
        )
        st.session_state.study_plan = plan

    if st.session_state.study_plan:
        st.write("### Study Plan:")
        st.write(st.session_state.study_plan)
