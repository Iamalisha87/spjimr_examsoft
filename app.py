import streamlit as st
import pandas as pd
from fuzzywuzzy import process

# Load the CSV file containing issues and solutions
file_path = 'data.csv'
data = pd.read_csv(file_path)

# Define the fuzzy matching search function
def find_solution(issue_query):
    # Get a list of all issues from the dataset
    issues_list = data['issues'].tolist()
    
    # Use fuzzy matching to find the closest match to the user's query
    closest_match, score = process.extractOne(issue_query, issues_list, score_cutoff=60)
    
    if closest_match:
        # Return the corresponding solution for the closest matching issue
        solution = data[data['issues'] == closest_match]['solutions'].values[0]
        return closest_match, solution
    else:
        return None, "Sorry, I couldn't find a solution for that issue. Please contact support."

# Streamlit app with enhanced UI
def main():
    st.set_page_config(page_title="Exemplify Exam Support Bot", layout="centered", initial_sidebar_state="auto")
    
    # Customizing the UI style
    st.markdown("""
        <style>
        .reportview-container {
            background: #f0f2f6;
        }
        .sidebar .sidebar-content {
            background: #4b4b4b;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        }
        .stTextInput>div>input {
            font-size: 18px;
            padding: 10px;
            border-radius: 5px;
        }
        .solution-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Exemplify Support")
    st.subheader("Resolve your exam issues with ease")

    st.write("Please describe the problem you're facing, and we'll provide the closest solution.")

    # User input for the issue
    issue_query = st.text_input("Enter your issue:")

    # Submit button to find a solution
    if st.button("Find Solution"):
        if issue_query:
            closest_match, solution = find_solution(issue_query)
            
            if closest_match:
                st.write(f"**Closest match found:** {closest_match}")
            else:
                st.write("**No close match found, showing default suggestion**")
            
            # Display the solution in a styled box
            st.markdown(f"<div class='solution-box'><h4>Solution:</h4><p>{solution}</p></div>", unsafe_allow_html=True)
        else:
            st.write("Please enter an issue to search for a solution.")

if __name__ == '__main__':
    main()
