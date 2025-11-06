import streamlit as st


def render_history_page():
    """Render the Q&A History page"""
    st.title("Q&A History")
    
    if st.session_state.qa_history:
        for item in reversed(st.session_state.qa_history):
            st.write(f"**Q:** {item['q']}")
            st.write(f"**A:** {item['a']}")
            st.markdown("---")
    else:
        st.info("No history yet. Ask some questions first!")
