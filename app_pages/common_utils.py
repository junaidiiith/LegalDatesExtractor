import streamlit as st
from app_utils.doc_processing import get_document_text



def get_current_uploaded_doc():
    return st.session_state["uploaded_docs"][st.session_state["doc_file"].name]

def set_current_uploaded_doc(doc):
    st.session_state["uploaded_docs"][st.session_state["doc_file"].name] = doc


def extract_doc_data():
    if not st.session_state.get("doc_file", None):
        return
    doc_file = st.session_state["doc_file"]
    if doc_file.name in st.session_state.get("uploaded_docs", dict()):
        print("Document already uploaded")
        st.session_state['doc'] = st.session_state['uploaded_docs'][doc_file.name]['doc']
        return
    get_document_text()
    st.session_state['uploaded_docs'][doc_file.name] = {
        'doc': st.session_state['doc'],
        'summary': None,
        'indexed': False,
        'extracted_dates': None,
        'refined_dates': None,
    }
    print("Total uploaded docs: ", len(st.session_state['uploaded_docs']))
    
