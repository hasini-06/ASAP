import streamlit as st
from pdf_qa import retrieve, ask_llm


def render_qa_page(text, chunks, index):
    """Render the Q&A page"""
    st.title("Q&A with PDF")
    
    query = st.text_input("Ask a question:")
    if st.button("Get Answer") and query:
        top_chunks = retrieve(query, chunks, index, k=3)
        context = " ".join(top_chunks)
        answer = ask_llm(f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:")
        st.session_state.qa_history.append({"q": query, "a": answer})

    if st.session_state.qa_history:
        for item in reversed(st.session_state.qa_history):
            st.write(f"**Q:** {item['q']}")
            st.write(f"**A:** {item['a']}")
            st.markdown("---")
