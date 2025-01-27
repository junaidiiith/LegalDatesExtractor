import streamlit as st
from app_utils.doc_processing import ( 
    get_document_text,
    print_document_details
)
from app_utils.doc_summarization import (
    create_index_from_document, 
    get_response, 
    doc_summarize_by_chunk
)


def add_to_messages(message, role):
    messages = st.session_state.get('messages', list())
    messages.append({"role": role, "content": message})
    st.session_state['messages'] = messages


def reset():
    st.session_state['messages'] = list()

def get_current_uploaded_doc():
    return st.session_state["uploaded_docs"][st.session_state["doc_file"].name]

def set_current_uploaded_doc(doc):
    st.session_state["uploaded_docs"][st.session_state["doc_file"].name] = doc

def summarize_document():
    current_doc = get_current_uploaded_doc()
    if current_doc.get("summary", None):
        # st.warning("Document already summarized.")
        return
    
    doc = current_doc.get("doc", None)
    if not doc:
        st.error("No text found in the document.")
        return
    # st.session_state["doc_summary"] = "Document Summary: DID NOT IMPLEMENT YET"
    with st.spinner("Summarizing Document..."):
        current_doc["summary"] = doc_summarize_by_chunk(doc["text"])
        set_current_uploaded_doc(current_doc)
    


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


def create_index():
    current_doc = get_current_uploaded_doc()
    if current_doc.get("indexed", False):
        # st.warning("Document already indexed.")
        return
    username = st.session_state['username']
    doc = current_doc.get("doc", None)
    
    if not doc or not doc.get("text", None):
        st.error("No text found in the document.")
        return
    
    doc_text = doc["text"]
    with st.spinner("Indexing Document..."):
        create_index_from_document(doc_text, index_name=username)
        current_doc["indexed"] = True
        set_current_uploaded_doc(current_doc)
    

def extract_doc_data():
    reset()
    
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
        'indexed': False
    }
    print("Total uploaded docs: ", len(st.session_state['uploaded_docs']))
    


def main():
    username = st.session_state['username']
    st.session_state["uploaded_docs"] = st.session_state.get("uploaded_docs", dict())
    st.title("PDF Document Summarization")

    st.file_uploader("Upload a document", type=["docx", "pdf", "txt"], key="doc_file", on_change=extract_doc_data)
    doc = st.session_state.get("doc_file", None)
 

    if doc:
        print_document_details()
        cols = st.columns(3)
        summarize = cols[0].button("Summarize Document", key="extract_dates")
        init_create_index = cols[1].button("Talk to Document", key="ask_questions")
        cols[2].button("Reset Document", key="reset", on_click=reset)

        if summarize or get_current_uploaded_doc().get("summary", None):
            summarize_document()
            st.markdown("### Document Summary")
            st.markdown(get_current_uploaded_doc()['summary'])

                
        if init_create_index or get_current_uploaded_doc().get("indexed", False):
            create_index()
            if query := st.chat_input("Ask me anything about the document"):
                add_to_messages(query, "user")
                with st.spinner("Getting Response..."):
                    response = get_response(query, index_name=username)
                    add_to_messages(response, "assistant")
                
                for message in st.session_state.get('messages', list()):
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])


main()