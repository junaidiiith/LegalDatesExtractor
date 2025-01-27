import streamlit as st
from app_utils.doc_processing import get_document_text


def get_doc_name():
    if st.session_state.get('doc_file', None):
        return st.session_state["doc_file"].name
    return None

    
def get_current_uploaded_doc():
    st.session_state["uploaded_docs"] = st.session_state.get("uploaded_docs", dict())
    return st.session_state["uploaded_docs"].get(get_doc_name(), dict())

def set_current_uploaded_doc(k, v):
    st.session_state["uploaded_docs"][get_doc_name()][k] = v


def extract_doc_data():
    st.session_state['uploaded_docs'] = st.session_state.get('uploaded_docs', dict())
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
    



def generate_response():
    import random
    responses = [
        "This is an insightful point!",
        "I never thought about it that way.",
        "That's an interesting take on the topic.",
        "You bring up a good argument, let's explore it further.",
        "Let's delve deeper into this subject.",
        "Your perspective is quite unique!",
        "This is a great prompt to consider.",
        "You've touched on a key issue there."
    ]
    return random.choice(responses)
