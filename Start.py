{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-01-05 18:09:31.398 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\sroff\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import dotenv\n",
    "\n",
    "import streamlit as st\n",
    "from openai import OpenAI\n",
    "\n",
    "dotenv.load_dotenv(\".env\")\n",
    "OPENAI_API_KEY = os.getenv(\"OPENAI_API_KEY\")\n",
    "\n",
    "def main():\n",
    "    if 'messages' not in st.session_state:\n",
    "        st.session_state['messages'] = []\n",
    "\n",
    "    client = OpenAI(api_key=\"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\")  # Add the api_key parameter to the OpenAI client constructor\n",
    "\n",
    "    st.title(\"Circular Economy Business Idea Evaluator\")\n",
    "\n",
    "    problem_statement = st.text_input(\"Problem Statement\")\n",
    "    solution = st.text_input(\"Solution\")\n",
    "\n",
    "    if problem_statement and solution:\n",
    "        if st.button('Evaluate Idea'):\n",
    "            st.session_state['messages'].append({\n",
    "                \"role\": \"user\",\n",
    "                \"content\": f\"Problem Statement: {problem_statement}\\nSolution: {solution}\"\n",
    "            })\n",
    "\n",
    "            assistant = client.beta.assistants.create(\n",
    "                instructions=\"\"\"\n",
    "                You are an evaluator of business ideas related to the circular economy. \n",
    "                Evaluate the idea in terms of the following metrics: \n",
    "                maturity stage, market potential, feasibility, scalability, risk associated, \n",
    "                technological innovation, adherence to circular economy principles. \n",
    "                Give a score or rating (out of 5) for these metrics and an overall rating.\n",
    "                \"\"\",\n",
    "                model=\"gpt-4-1106-preview\",\n",
    "                tools=[{\"type\": \"retrieval\"}]\n",
    "            )\n",
    "\n",
    "            thread = client.beta.threads.create(\n",
    "                messages=st.session_state['messages']\n",
    "            )\n",
    "\n",
    "            run = client.beta.threads.runs.create(\n",
    "                thread_id=thread.id,\n",
    "                assistant_id=assistant.id\n",
    "            )\n",
    "\n",
    "            while run.status != \"completed\":\n",
    "                run = client.beta.threads.runs.retrieve(\n",
    "                    thread_id=thread.id,\n",
    "                    run_id=run.id\n",
    "                )\n",
    "\n",
    "            messages = client.beta.threads.messages.list(thread_id=thread.id)\n",
    "            assistant_response = messages.data[0].content[0].text.value\n",
    "\n",
    "            st.session_state['messages'].append({\n",
    "                \"role\": \"assistant\",\n",
    "                \"content\": assistant_response\n",
    "            })\n",
    "\n",
    "            st.write(assistant_response.replace(\"$\", \"\\$\"))\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
