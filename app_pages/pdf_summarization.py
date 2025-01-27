import streamlit as st
from app_pages.common_utils import extract_doc_data, get_current_uploaded_doc, set_current_uploaded_doc
from app_utils.doc_processing import ( 
    print_document_details
)
from app_utils.doc_llm_utils import (
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


def summarize_document():
    if get_current_uploaded_doc().get("summary", None):
        # st.warning("Document already summarized.")
        return
    
    doc = get_current_uploaded_doc().get("doc", None)
    if not doc:
        st.error("No text found in the document.")
        return
    # st.session_state["doc_summary"] = "Document Summary: DID NOT IMPLEMENT YET"
    with st.spinner("Summarizing Document..."):
        set_current_uploaded_doc('summary', doc_summarize_by_chunk(doc["text"]))


def create_index():
    if get_current_uploaded_doc().get("indexed", False):
        # st.warning("Document already indexed.")
        return
    username = st.session_state['username']
    doc = get_current_uploaded_doc().get("doc", None)
    
    if not doc or not doc.get("text", None):
        st.error("No text found in the document.")
        return
    
    doc_text = doc["text"]
    with st.spinner("Indexing Document..."):
        create_index_from_document(doc_text, index_name=username)
        set_current_uploaded_doc('indexed', True)
\
def upload_doc():
    reset()
    extract_doc_data()


def main():
    username = st.session_state['username']
    st.title("PDF Document Summarization")

    st.file_uploader("Upload a document", type=["docx", "pdf", "txt"], key="doc_file", on_change=upload_doc)
    doc = st.session_state.get("doc_file", None)
 

    if doc:
        print_document_details()
        cols = st.columns(3)
        cols[0].button("Summarize Document", key="extract_dates", on_click=summarize_document)
        cols[1].button("Talk to Document", key="ask_questions", on_click=create_index)
        cols[2].button("Reset Document", key="reset", on_click=reset)

        if get_current_uploaded_doc().get("summary", None):
            st.markdown("### Document Summary")
            st.markdown(get_current_uploaded_doc()['summary'])

                
        if get_current_uploaded_doc().get("indexed", False):
            if query := st.chat_input("Ask me anything about the document"):
                add_to_messages(query, "user")
                with st.spinner("Getting Response..."):
                    response = get_response(query, index_name=username)
                    add_to_messages(response, "assistant")
                
                for message in st.session_state.get('messages', list()):
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])


main()