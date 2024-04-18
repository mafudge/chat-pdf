__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from streamlit_chat import message
import random 
import os
import logging
import glob
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.document_loaders import PyPDFLoader

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

st.session_state.setdefault('past', [] )
st.session_state.setdefault('generated', [])

st.title("Chat With Your PDF")
st.write("This demonstrates the simplest method of Retrieval Augmented Generation: integrating an LLM with a PDF for Q&A")
st.write('''
    1. Ollama / TinyLlama is the LLM (Large Language Model).
    2. Your PDF is split up into "chunks", weighted, and stored in a vector database.
    3. When you ask a question, the LLM extracts key terms from the query.
    4. Those key terms are used to search the vector database for matching chunks from the query.
    5. Those chunks, along with your original question are 
       fed back into the LLM as part of the prompt asking it to answer the question based on the information given.
    6. The LLM generates the result.    
''')
st.write("Be patient. The demo can take a while to load as it does not support GPUs.")


logging.info("Starting.")
pdffile = st.file_uploader("Upload a PDF:")
if pdffile is not None:

    # To read file as bytes:
    bytes_data = pdffile.getvalue()
    filename = f"{random.getrandbits(32)}-{pdffile.name}"
    logging.info(f"Uploaded PDF: {filename}")
    with open(filename,"wb") as f:
        f.write(bytes_data)
    loader = PyPDFLoader(filename)
    chunks = loader.load_and_split()
    llm = ChatOllama(model="tinyllama", base_url="http://ollama:11434")
    embeddings = OllamaEmbeddings(base_url="http://ollama:11434")
    db = Chroma.from_documents(chunks,embeddings)
    retriever = db.as_retriever()    
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    if os.path.exists(filename):
        os.remove(filename)

    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.past.append(user_input)
        answer = qa.run(user_input)
        st.session_state.generated.append(answer)

    def on_btn_click():
        del st.session_state.past[:]
        del st.session_state.generated[:]

    chat_placeholder = st.empty()

    with chat_placeholder.container():    
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(st.session_state['generated'][i], is_user=False, key=f"{i}_bot")
        
        st.button("Clear history", on_click=on_btn_click)

    with st.container():
        st.text_input("Ask Question:", on_change=on_input_change, key="user_input")