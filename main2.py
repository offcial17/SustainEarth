import os
import pandas as pd
import streamlit as st
from openai import OpenAI
import dotenv

dotenv.load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def evaluate_idea(problem_statement, solution):
    """
    Function to evaluate an idea using OpenAI Assistant.
    """
    client = OpenAI()

    # Your existing code for assistant creation and evaluation
    assistant = client.beta.assistants.create(
        instructions="""
        You are an evaluator of business ideas related to the circular economy.
        For CSV files evaluation, raise an error that says documents not found only when there is a runtime error and not when text for the problem and solution are available.
        Be very consistent with the format of the responses generated.
        Be very critical and strict for each metric (penalize as much as possible).
        Highlight the areas of concern.
        Keep the headers and scores in bold.
        Explain each metric in a separate paragraph and have at least 100 words each.
        Calculate the result at the end and display it. Print the total score out of 100 in bold and large font at the end.
        Highlight each metric and generate a comprehensive table at the end that compiles the findings as well as a summary paragraph.
        The columns in this table are Metric, Score and Notes/Comments (for concerns/issues).
        Be very consistent with the format of the responses generated.
        Here are the evaluation criteria for an Early-Stage Circular Economy Business Ideas.
        Use this to generate a rating to determine how likely is it to succeed. Calculate the scores for each metric as mentioned below.

        1) Idea Originality and Relevance: How unique and relevant is the idea in the context of the circular economy? Does it address a clear need or gap in the market? Rate Originality out of 5 and Relevance out of 5.

        2) Conceptual Clarity and Differentiation: How clearly is the idea articulated? What sets it apart from existing concepts or competitors? Rate clear communication out of 5 and differentiation out of 5.

        3) Environmental Impact Potential: Assess the potential of the idea to minimize environmental impact and maximize resource efficiency. Use the United States SDGs to add context to the explanation. Highlight how it affects the circular economy. 
        Rate out of 10.

        4) Stakeholder Value Proposition: (Print each of the following in separate lines)
            a. To the Internal Stakeholders: How much value could this idea potentially add to the company? Rate out of 5.
            b. To the External Stakeholders: Consider the potential impact on the community that would create the product. The lower the potential environmental impact, the higher the score. Also consider the customer. How would it add value to them? Rate out of 5.

        5. Customer Scalability Potential: Does the idea have the potential to shift from one-time transactions to long-term engagement, fostering co-creation, and encouraging responsible consumption habits? Rate out of 10.

        6. Feasibility of Implementation: Considering the current market and technological landscape, how feasible is it to implement this idea? Please be critical and Rate out of 15.

        7. Target Market and Customer Awareness: Evaluate the potential awareness and receptivity of the target market towards this idea, considering environmental consciousness and willingness to adopt new practices. Rate out of 10.

        8. Cost and Resource Efficiency Potential: Assess the potential of the idea for cost-effectiveness and resource efficiency, considering aspects like design for disassembly and use of durable materials. How expensive is it to implement this idea in the real world? 
        Contrast that with how expensive does the solution say it is? Is there a gap? If so, does the solution say anything to address how it fixes that gap? If not, please rate low. If there is not such a gap, evaluate fairly. 
        Rate out of 10.

        9. Revenue Generation and Growth Potential:(Print each of the following in separate lines)
            a. Revenue Generation: How could this idea potentially generate revenue? Rate out of 5.
            b. Growth Potential: Assess the scalability and potential for significant growth of this idea. 
        How much money may be required to make this happen? How much time will be required? Rate out of 10.

        10. Risk and Innovation Assessment: Evaluate the level of risk and the potential for disruption and innovation that this idea represents. Rate out of 10.
        """,
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"}]
    )

    thread = client.beta.threads.create(
        messages=[{"role": "user", "content": f"Problem : {problem_statement}\nSolution: {solution}"}]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value

    return assistant_response.replace("$", "\$")

def main():
    # Title
    st.title("ECOLOOP MAVEN")
    # Subtitle
    st.markdown("*Your Business Idea Evaluator*")

    # Allow user to upload a CSV file
    st.subheader("Upload a CSV File in this format - ID, Problem, Solution")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

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
                    # Convert the user input to integer
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
     
    # Allow user to manually input problem statement and solution
    else:
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
