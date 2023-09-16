import os 
# from apikey import apikey 
# from serp import serpapi

import streamlit as st 
from langchain.llms import OpenAI,HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
import PyPDF2
from typing_extensions import Concatenate

# os.environ['OPENAI_API_KEY'] = "sk-EWFb7peDQc"
os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"

# os.environ['SERPAPI_API_KEY'] = serpapi


# App framework
st.title('JobSearch')
uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    df = PyPDF2.PdfReader(uploaded_file)
#Extracting Resume Data function

    # read text from pdf
    raw_text = ''
    for i, page in enumerate(df.pages):

        if content:
            raw_text += content
#text splitter



# Prompt templates
job_template = PromptTemplate(
    input_variables = ['raw_text'], 
    template='suggest some job title based on this raw text: {raw_text} '
)

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'], 
    template='write me a youtube video script based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = HuggingFaceHub(repo_id='google/flan-t5-xl',model_kwargs={"temperature":1e-10})
title_chain = LLMChain(llm=llm, prompt=job_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

#wiki = WikipediaAPIWrapper()

# # Show stuff to the screen if there's a prompt
# if prompt: 
if uploaded_file is not None:
    title = title_chain.run(raw_text)
#     wiki_research = wiki.run(prompt) 
#     script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title) 
#     st.write(script) 

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

#     with st.expander('Script History'): 
#         st.info(script_memory.buffer)

#     with st.expander('Wikipedia Research'): 
#         st.info(wiki_research)