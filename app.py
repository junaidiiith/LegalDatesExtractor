import streamlit as st
from app_utils.constants import *
import app_utils.auth as auth_utils
from settings import (
    auth_file,
)

def run_pages(pages):
    pg = st.navigation(pages)
    pg.run()


auth_utils.authenticate(auth_file=auth_file)

if st.session_state['authentication_status']:
    # print("Authentication status: Now", st.session_state['authentication_status'])
    username = st.session_state['username']
    name = st.session_state['name']  
    roles = st.session_state['roles']

    pages = [
        st.Page("app_pages/dates_extraction.py", title="Legal Dates Extraction"),
        st.Page("app_pages/transcript_generation.py", title="Transcript Generation"),
        st.Page("app_pages/pdf_summarization.py", title="PDF Summarization"),
    ]

    run_pages(pages)
    