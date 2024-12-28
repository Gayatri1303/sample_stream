import streamlit as st
from pymongo import MongoClient

# MongoDB connection
connection_string = st.secrets["MONGO_URI"]
client = MongoClient(connection_string)
db = client['quiz-db']
collection = db['quizcollect']

# Streamlit UI
st.title("Interactive Quiz")

# Input for Quiz ID
quiz_id = st.text_input("Enter Quiz ID:")

# Load Quiz Button
if st.button("Load Quiz"):
    quiz = collection.find_one({"quiz_id": quiz_id})
    if quiz:
        # Save quiz data in session state
        st.session_state['quiz'] = quiz
        st.session_state['submitted'] = False
    else:
        st.error("Quiz not found!")

# Display Quiz if Loaded
if 'quiz' in st.session_state:
    quiz = st.session_state['quiz']
    st.subheader(quiz['title'])
    st.write(quiz['description'])

    # Store user answers
    user_answers = {}
    for question in quiz['questions'][:5]:  # Limit to 5 questions
        user_answers[question['question_id']] = st.radio(
            f"Q{question['question_id']}: {question['question_text']}",
            [option['option_text'] for option in question['options']],
            key=f"question_{question['question_id']}"
        )

    # Submit Quiz Button
    if st.button("Submit Quiz") and not st.session_state.get('submitted', False):
        # Evaluate answers
        correct_count = 0
        for question in quiz['questions'][:5]:
            correct_option = next(
                option['option_text'] for option in question['options'] if option['is_correct']
            )
            if st.session_state[f"question_{question['question_id']}"] == correct_option:
                correct_count += 1

        # Display score and prevent multiple submissions
        st.success(f"You scored {correct_count}/5!")
        st.session_state['submitted'] = True
