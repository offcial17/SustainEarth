import pandas as pd
import streamlit as st
from prompt import evaluate_idea

def main():
    # Title with green strip background
    title_html = """
        <style>
            .title-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #4CAF50; /* Green background color */
                padding: 10px;
                margin-bottom: 20px; /* Added margin for separation */
            }
            .title-text {
                color: white;
            }
        </style>
        <div class="title-container">
            <div class="title-text">
                <h1>ECOLOOP MAVEN</h1>
                <p>Your Business Idea Evaluator</p>
            </div>
        </div>
    """
    st.markdown(title_html, unsafe_allow_html=True)

    # Allow user to upload a CSV file
    st.subheader("Upload a CSV File with the Following Format:")
    st.markdown("Ensure your CSV file has three columns: **ID**, **Problem**, and **Solution**.")
    st.markdown("Example:")
    st.code("ID, Problem, Solution\n1, Your problem statement 1, Your solution 1\n2, Your problem statement 2, Your solution 2\n...")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Use st.empty() to create an empty placeholder for the "OR" text
    or_text_placeholder = st.empty()

    # Check if a file is uploaded
    if uploaded_file is not None:
        try:
            # Load the CSV file into a DataFrame with the first column as the index
            df = pd.read_csv(uploaded_file, encoding='latin1', index_col=0)

            # Check for errors in file format
            if len(df.columns) != 2 or not df.index.is_numeric() or not all(df.dtypes == 'object'):
                raise pd.errors.ParserError

            # Display the uploaded data
            st.write("Uploaded Data:")
            st.write(df)

            # Allow user to input the problem ID
            row_input = st.text_input("Enter Problem ID:")
            if st.button('Evaluate Idea') and row_input:
                try:
                    # Convert the user input to an integer
                    row_number = int(row_input)

                    # Check if the row number is within the valid range
                    if 1 <= row_number <= len(df):
                        # Get the corresponding problem statement and solution
                        problem_statement = df.iloc[row_number - 1, 0]
                        solution = df.iloc[row_number - 1, 1]

                        # Evaluate the idea using the OpenAI Assistant
                        result = evaluate_idea(problem_statement, solution)

                        # Display the result
                        st.write("Evaluation Result:")
                        st.write(result)
                except ValueError:
                    st.error("Invalid input. Please enter a valid integer for the row number.")

        except pd.errors.ParserError:
            st.error("Invalid CSV file format. Please ensure the file follows the expected format.")

        # Clear the "OR" text placeholder
        or_text_placeholder.empty()

    # Allow user to manually input problem statement and solution
    else:
        # Display the "OR" text
        or_text_placeholder.text("OR")

        # Allow user to input the problem statement and solution manually
        st.subheader("Enter the problem and solution manually:")
        problem_statement = st.text_input("Problem Statement")
        solution = st.text_input("Solution")

        if problem_statement and solution:
            if st.button('Evaluate Idea'):
                result = evaluate_idea(problem_statement, solution)
                st.write("Evaluation Result:")
                st.write(result)

if __name__ == "__main__":
    main()
