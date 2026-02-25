import os
import time
import logging
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from data.employees import generate_employee_data
from assistant import Assistant
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from gui import AssistantGUI

load_dotenv()
logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Nvidia 10-K Analyzer", page_icon="📈", layout="wide")

@st.cache_data(ttl=3600, show_spinner="Loading data...")
def get_user_data():
    return generate_employee_data(1)[0]

@st.cache_resource(ttl=3600, show_spinner="Loading Vector Database...")
def init_vector_store(pdf_path):
    try:
        if not os.path.exists(pdf_path):
            st.error(f"File not found: {pdf_path}")
            return None
        
        db_path = "./data/chroma_db"
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

        if os.path.exists(db_path) and os.path.isdir(db_path):
            try:
                v_store = Chroma(persist_directory=db_path, embedding_function=embeddings)
                if v_store._collection.count() > 0:
                    logging.info("Loaded existing DB from disk.")
                    return v_store
            except Exception:
                pass 

        logging.info(f"Processing new PDF: {pdf_path}")
        
        docs = PyPDFLoader(pdf_path).load()
        splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
        
        batch_size = 5
        v_store = None
        
        bar = st.progress(0, text="Embedding documents...")
        
        for i in range(0, len(splits), batch_size):
            batch = splits[i:i + batch_size]
            
            for attempt in range(3):
                try:
                    if v_store is None:
                        v_store = Chroma.from_documents(
                            documents=batch, 
                            embedding=embeddings,
                            persist_directory=db_path
                        )
                    else:
                        v_store.add_documents(batch)
                    break 
                except Exception as e:
                    if "429" in str(e):
                        time.sleep(30)
                    else:
                        raise e
            
            progress = min((i + batch_size) / len(splits), 1.0)
            bar.progress(progress, text=f"Processed {i + len(batch)}/{len(splits)} chunks")
            time.sleep(2)
            
        bar.empty()
        return v_store

    except Exception as e:
        logging.error(f"Vector store error: {e}")
        st.error(f"Error: {e}")
        return None

if __name__ == "__main__":
    user_data = get_user_data()
    vector_store = init_vector_store("data/nvidia-sec-10-k-form.pdf")
    
    if "customer" not in st.session_state:
        st.session_state.customer = user_data
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": WELCOME_MESSAGE}]

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        vector_store=vector_store,
        employee_information=st.session_state.customer
    )
    
    AssistantGUI(assistant).render()