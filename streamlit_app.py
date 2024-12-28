import streamlit as st
from pymongo import MongoClient
# Use Streamlit secret
connection_string = st.secrets["MONGO_URI"]
client = MongoClient(connection_string)
db = client['quiz-db']
collection = db['quizcollect']

# Streamlit UI
st.title("Interactive Quiz")

# Input for Quiz ID
quiz_id = st.text_input("Enter Quiz ID:")

if st.button("Load Quiz"):
    # Fetch quiz data from MongoDB
    quiz = collection.find_one({"quiz_id": quiz_id})
    
    if quiz:
        st.subheader(quiz['title'])
        st.write(quiz['description'])
        
        # Store user answers
        user_answers = {}
        questions = quiz['questions'][:5]  # Limit to 5 questions
        
        for question in questions:
            st.write(f"Q{question['question_id']}: {question['question_text']}")
            # Display options using radio buttons
            user_answers[question['question_id']] = st.radio(
                f"Options for Q{question['question_id']}:",
                [option['option_text'] for option in question['options']],
                key=question['question_id']
            )
        
        # Submit button
        if st.button("Submit Quiz"):
            # Evaluate answers
            correct_count = 0
            for question in questions:
                correct_option = next(
                    option['option_text'] for option in question['options'] if option['is_correct']
                )
                if user_answers[question['question_id']] == correct_option:
                    correct_count += 1
            
            # Display score
            st.success(f"You scored {correct_count}/{len(questions)}!")
    else:
        st.error("Quiz not found!")



