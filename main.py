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
"""

You are an evaluator of business ideas related to the circular economy.

Analyze the following: 

Key Partnerships: Who is required to bring this idea to life? Partnerships with whom is required? The more number of partnerships required to bring the project to success, the lower the rating. Rate out of 10. 

Key Activities: What does the product do that differentiates it from the competitors in the market? Is it better at that or worse at that? Evaluate based out of 5. 

Key Resources: Is it minimizing the environmental impact of resource extraction and maximizing resource efficiency. Score this out of 10.

Value Proposition: How much value does this idea add to the following stakeholders: 
a. Company - evaluate out of 3 
b. Neighbourhood that creates the product - evaluate out of 5 - the lower the environmental impact on them, the better the rating. 
c. Environment - Does it lower carbon emissions or make an impact in climate change? Evaluate out of 5. 


Customer Relationships: Does it shift from one-time transactions to building long-term engagement, fostering co-creation, and encouraging responsible consumption habits. 
Track customer satisfaction with repair services, take-back programs, and community initiatives. Measure community engagement in circular practices and brand loyalty and evaluate out of 5. 

Channels: 
How is the product provided to the customer? Evaluate the following - product sharing, repair services, and upcycling resources and then evaluate out of 5. 

Customer Segments: How much awareness does the target customer of this product have? Think about their environmental awareness, willingness to participate in circular practices, and preferred access models. Evaluate out of 5. 

Cost Structure: Focus on designs for disassembly, durable materials, and closed-loop systems to minimize waste and recycling costs. 

Revenue Streams: 
How does this product generate revenue? - evaluate out of 3 
Is there potential for hyper growth? - evaluate out of 3 


Risk analysis: How risky and disruptive is this project? Evaluate out of 3. 


"""
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
