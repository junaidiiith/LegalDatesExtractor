import os
import streamlit as st


auth_file = 'authentication.yaml'
chroma_data_dir = 'chroma_db_data'
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
FIREWORKS_API_KEY = st.secrets['FIREWORKS_API_KEY']

CHUNK_SIZE = 4096
CHUNK_OVERLAP = 128

