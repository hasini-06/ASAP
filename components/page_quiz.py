import streamlit as st
import json
from pdf_qa import ask_llm


def render_quiz_page(text):
    """Render the Quiz Generator page"""
    st.title("Quiz Generator")

    # Step 1: Inputs
    num_qs = st.number_input("Number of questions", min_value=1, max_value=10, value=3, step=1)
    difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])

    st.markdown(f"**Difficulty Selected:** {difficulty}")

    # Step 2: Generate Quiz
    if st.button("Create Quiz"):
        quiz_prompt = f"""
        Generate {num_qs} multiple-choice quiz questions based ONLY on the PDF content below.
        The questions should be of **{difficulty.lower()}** difficulty level.

        Difficulty Guide:
        - Easy: Direct factual questions.
        - Medium: Conceptual or reasoning-based questions.
        - Hard: Analytical or multi-step reasoning questions.

        Each question must have:
        - "question": string
        - "options": list of 4 strings
        - "answer": the correct option
        - "explanation": short reason why it's correct

        Return ONLY a valid JSON array.
        Content: {text[:3000]}
        """

        quiz_text = ask_llm(quiz_prompt, temperature=0.5)

        try:
            start = quiz_text.find("[")
            end = quiz_text.rfind("]") + 1
            quiz_json = quiz_text[start:end]
            quiz = json.loads(quiz_json)
        except Exception as e:
            st.error(f"Failed to parse quiz: {e}")
            quiz = []

        st.session_state.quiz = quiz
        st.session_state.user_answers = [None] * len(quiz)
        st.session_state.quiz_submitted = False

    # Step 3: Display Quiz
    if st.session_state.quiz:
        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.quiz):
                st.subheader(f"Q{i+1}: {q['question']}")
                st.session_state.user_answers[i] = st.radio(
                    "Choose an option:",
                    q["options"],
                    index=None,
                    key=f"q{i}"
                )
                st.markdown("---")

            submitted = st.form_submit_button("Submit All")

        # Step 4: Evaluation
        if submitted:
            if None in st.session_state.user_answers:
                st.warning("Please answer all questions before submitting.")
            else:
                st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:
            score = 0
            for i, q in enumerate(st.session_state.quiz):
                user_ans = st.session_state.user_answers[i]
                correct = q["answer"]

                # Normalize answers before comparing
                user_ans_clean = user_ans.strip().lower().replace(".", "")
                correct_clean = correct.strip().lower().replace(".", "")

                if user_ans_clean == correct_clean:
                    st.success(f"Q{i+1}: Correct — {correct}")
                    score += 1
                else:
                    st.error(f"Q{i+1}: Wrong — You chose: {user_ans}. Correct: {correct}")
                
                st.caption(f"Why: {q.get('explanation','No explanation provided')}")
                st.markdown("---")

            st.info(f"Final Score: {score}/{len(st.session_state.quiz)}")
