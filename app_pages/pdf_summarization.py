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
    st.session_state["doc_text"] = None
    st.session_state["doc_indexed"] = False
    st.session_state['messages'] = list()


def summarize_document():
    doc_text = st.session_state.get("doc_text", None)
    if not doc_text:
        return
    st.session_state["doc_summary"] = doc_summarize_by_chunk(doc_text)


def create_index():
    username = st.session_state['username']
    doc_text = st.session_state.get("doc_text", None)
    if not doc_text:
        return
    create_index_from_document(doc_text, index_name=username)
    st.session_state["doc_indexed"] = True
    

def main():
    username = st.session_state['username']
    st.title("PDF Document Summarization")

    st.file_uploader("Upload a document", type=["docx", "pdf"], key="doc_file", on_change=get_document_text)
    doc = st.session_state.get("doc_file", None)
 

    if doc:
        print_document_details()
        cols = st.columns(3)
        summarize = cols[0].button("Summarize Document", key="extract_dates")
        cols[1].button("Ask Questions from Document", key="ask_questions", on_click=create_index)
        cols[2].button("Reset", key="reset", on_click=reset)		

        if summarize or st.session_state.get("doc_summary", None):
            if summarize:
                with st.spinner("Summarizing Document..."):
                    summarize_document()
     
            st.write("Document Summary")
            st.write(st.session_state["doc_summary"])

   
        if query := st.chat_input(
            disabled=not st.session_state.get("doc_indexed", False),	
         ):
            add_to_messages(query, "user")
            with st.spinner("Getting Response..."):
                response = get_response(query, index_name=username)
                add_to_messages(response, "assistant")

        for message in st.session_state.get('messages', list()):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

main()