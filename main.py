from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.memory import ChatMemoryBuffer
import streamlit as st
import pandas as pd


system_prompt = f"""
You are a multi-lingual expert system who has knowledge, based on 
real-time data. You will always try to be helpful and try to help them 
answering their question. If you don't know the answer, say that you DON'T
KNOW.

Jawablah semua dalam Bahasa Indonesia.
Anda adalah asisten user yang memiliki tugas untuk membantu peneliti untuk menganalisis data berdasarkan dokumen-dokumen yang sudah disiapkan user. Berikan analisis sesuai dengan semua dokumen yang disediakan user untuk membantu pembuatan papernya.

Percakapan sejauh ini:
"""

Settings.llm = Ollama(model="llama3.1:latest", base_url="http://127.0.0.1:11434", system_prompt=system_prompt) 
Settings.embed_model = OllamaEmbedding(base_url="http://127.0.0.1:11434", model_name="mxbai-embed-large:latest") 

docs = SimpleDirectoryReader("docs").load_data()
index = VectorStoreIndex.from_documents(docs)

st.title("Analisis dan Rangkuman dokumen")
# st.write("Lorem ipsum dolor sit amet")

if "messages_docs" not in st.session_state:
    st.session_state.messages_docs = [
        {"role": "assistant",
         "content": "Halo, apakah ada yang anda ingin tanyakan seputar dokumen?"}
    ]

if "chat_engine_docs" not in st.session_state:

    memory = ChatMemoryBuffer.from_defaults(token_limit=50384)
    st.session_state.chat_engine_docs = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt= system_prompt,
    verbose=True
)

# Display chat messages from history on app rerun
for message in st.session_state.messages_docs:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt:= st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages_docs.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Berpikir..."):
            response_stream = st.session_state.chat_engine_docs.chat(prompt)
            st.markdown(response_stream)

    # Add user message to chat history
    st.session_state.messages_riasec.append({"role": "assistant", "content": response_stream})