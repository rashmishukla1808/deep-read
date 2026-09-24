import streamlit as st

from quiz_engine import generate_quiz


st.title("Deep Read 📖")

st.write("Test whether you actually understood what you read.")

passage = st.text_area(
    "Paste a passage below 👇",
    height=250
)

if st.button("Generate Quiz"):
    if passage.strip():
        quiz = generate_quiz(passage)

        st.session_state.quiz = quiz

    else:
        st.warning("Please paste a passage first.")


if "quiz" in st.session_state:

    quiz = st.session_state.quiz

    st.divider()
    st.header("Your Quiz")

    answers = []

    for i, question in enumerate(quiz.questions):

        st.subheader(f"Question {i + 1}")

        st.write(question.question)

        answer = st.radio(
            "Choose an answer:",
            question.options,
            key=f"question_{i}"
        )

        answers.append(question.options.index(answer))

    if st.button("Submit Quiz"):

        score = 0

        for i, question in enumerate(quiz.questions):

            if answers[i] == question.correct_answer:
                score += 1

        st.divider()
        st.header("Your Results")

        st.write(f"Your score: **{score}/{len(quiz.questions)}**")
