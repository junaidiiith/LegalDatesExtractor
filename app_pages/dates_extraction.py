import streamlit as st
from stqdm import stqdm

from app_pages.common_utils import (
    extract_doc_data, 
    get_current_uploaded_doc, 
    set_current_uploaded_doc
)
from app_utils.doc_llm_utils import (
    extract_doc_dates, 
    refine_doc_dates
)
from app_utils.doc_processing import (
    print_document_details, 
    get_nodes_from_documents
)


def refine_dates_texts():
    
    if not get_current_uploaded_doc().get("extracted_dates", None):
        print("No dates found in the document. Extracting dates...")
        get_document_dates()
        
    if not get_current_uploaded_doc().get("refined_dates", None):
        with st.spinner("Refining dates and details..."):
            print("Refining dates and details...")
            extracted_dates = get_current_uploaded_doc().get("extracted_dates")
            doc_dates_refined = refine_doc_dates(extracted_dates)
            # doc_dates_refined = "Refined"
        
        set_current_uploaded_doc("refined_dates", doc_dates_refined)


def get_document_dates():
    if not get_current_uploaded_doc().get("doc", None):
        st.error("No text found in the document.")
        return
    text = get_current_uploaded_doc().get("doc")["text"]

    if not get_current_uploaded_doc().get("extracted_dates", None):
        texts = [n.text for n in get_nodes_from_documents(text)]
        dated_texts = []
        for text in stqdm(texts, desc="Extracting dates and details"):
            dated_text = extract_doc_dates(text)
            dated_texts.append(dated_text)
        
        doc_dates = "\n".join(dated_texts)
        
        set_current_uploaded_doc("extracted_dates", doc_dates)
        

def reset():
    current_doc = get_current_uploaded_doc()
    current_doc["extracted_dates"] = None
    current_doc["refined_dates"] = None
 
 
def upload_doc():
    reset()
    extract_doc_data()

    
def main():
    st.title("Legal Document Dates Extractor")

    # with st.expander("Size of text to process at once"):
    # 	cols = st.columns(2)
    # 	cols[0].number_input("Chunk size", value=5000, key="chunk_size", help="The size of the text to be processed at a time. Default is 5000.")
    # 	cols[1].number_input("Chunk overlap", value=100, key="chunk_overlap", help="The overlap between chunks. Default is 50.")

    st.file_uploader("Upload a document", type=["docx", "pdf"], key="doc_file", on_change=upload_doc)
    doc = st.session_state.get("doc_file", None)
    
    if doc:
        print_document_details()
        cols = st.columns(3)
        
        cols[0].button("Extract dates and details", key="extract_dates", on_click=get_document_dates)
        cols[1].button("Refine dates and details", key="refine_dates", on_click=refine_dates_texts)
        cols[2].button("Reset Document", key="reset", on_click=reset)
        

    extracted_data = get_current_uploaded_doc().get("extracted_dates", None)
    refined_data = get_current_uploaded_doc().get("refined_dates", None)
    
    if refined_data:
        with st.container():
            doc_dates_refined = get_current_uploaded_doc().get("refined_dates")
            st.markdown("### Refined Dates and details")
            st.write(doc_dates_refined)
            
    elif extracted_data:
        with st.container():
            doc_dates = get_current_uploaded_doc().get("extracted_dates")
            st.markdown("### Extracted Dates and details\n")
            st.write(doc_dates)

main()