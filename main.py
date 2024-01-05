import os
import dotenv

import streamlit as st
from openai import OpenAI

dotenv.load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    client = OpenAI()

    st.title("Circular Economy Business Idea Evaluator")

    problem_statement = st.text_input("Problem Statement")
    solution = st.text_input("Solution")

    if problem_statement and solution:
        if st.button('Evaluate Idea'):
            st.session_state['messages'].append({
                "role": "user",
                "content": f"Problem Statement: {problem_statement}\nSolution: {solution}"
            })

            assistant = client.beta.assistants.create(
                instructions="""
                You are an evaluator of business ideas related to the circular economy. 
                Evaluate the idea in terms of the following metrics: 
                maturity stage, market potential, feasibility, scalability, risk associated, 
                technological innovation, adherence to circular economy principles. 
                Give a score or rating (out of 5) for these metrics and an overall rating.
                """,
                model="gpt-4-1106-preview",
                tools=[{"type": "retrieval"}]
            )

            thread = client.beta.threads.create(
                messages=st.session_state['messages']
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

            st.session_state['messages'].append({
                "role": "assistant",
                "content": assistant_response
            })

            st.write(assistant_response.replace("$", "\$"))

if __name__ == "__main__":
    main()