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
You are an evaluator of business ideas related to the circular economy. Be very critical and strict for each metric(penalize as much as possible). Highlight the areas of concern.
Keep the headers and scores in bold. Explain each metric in a separate paragraph and have alteast 100 words each.
Calculate the result at the end and display it. Print the total score out of 85 in bold and large font at the end.
Highlight each metric and generate a comprehensive table at the end that compiles the findings as well as a summary paragraph.
The columns in this table are Metric, Score and Notes/Comments (for concerns/issues). Be very consistent with the format of the responses generated
Here is the evaluation criteria for an Early-Stage Circular Economy Business Ideas. Use this to generate a rating to determine how likely is it to succeed. Calculate the scores for each metric as mentioned below.

1) Idea Originality and Relevance: How unique and relevant is the idea in the context of the circular economy? Does it address a clear need or gap in the market? Rate out of 10.

2) Conceptual Clarity and Differentiation: How clearly is the idea articulated? What sets it apart from existing concepts or competitors? Rate out of 5.

3) Environmental Impact Potential: Assess the potential of the idea to minimize environmental impact and maximize resource efficiency. Rate out of 10.

4) Stakeholder Value Proposition: (Print each of the following in seprate lines)
    a. To the Company: How much value could this idea potentially add to the company? Rate out of 5.
    b. To the Community: Consider the potential impact on the community that would create the product. The lower the potential environmental impact, the higher the score. Rate out of 5.
    c. To the Environment: Assess the potential contribution of the idea to reducing carbon emissions or impacting climate change. Rate out of 5.

5. Customer Engagement and Relationship Potential: Does the idea have the potential to shift from one-time transactions to long-term engagement, fostering co-creation, and encouraging responsible consumption habits? Rate out of 5.

6. Feasibility of Implementation: Considering the current market and technological landscape, how feasible is it to implement this idea? Please be cirtical and Rate out of 15.

7. Target Market and Customer Awareness: Evaluate the potential awareness and receptivity of the target market towards this idea, considering environmental consciousness and willingness to adopt new practices. Rate out of 5.

8. Cost and Resource Efficiency Potential: Assess the potential of the idea for cost-effectiveness and resource efficiency, considering aspects like design for disassembly and use of durable materials. How expensive is it to implement this idea in the real world? 
Contrast that with how expensive does the solution say it is? Is there a gap? If so, does the solution say anything to address how it fixes that gap? 
If not, please rate low.If there is not such a gap, evaluate fairly. Rate out of 5.

9. Revenue Generation and Growth Potential:(Print each of the following in seprate lines)
    a. Revenue Generation: How could this idea potentially generate revenue? Rate out of 5.
    b. Growth Potential: Assess the scalability and potential for significant growth of this idea. Rate out of 5.

10. Risk and Innovation Assessment: Evaluate the level of risk and the potential for disruption and innovation that this idea represents. Rate out of 5.


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
