import PyPDF2
import streamlit as st
from docx import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile



def pdf_to_markdown(pdf_file):
    # Initialize the PDF reader
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texts = list()
    
    # Iterate through all pages and extract text
    for page in pdf_reader.pages:
        part_text = page.extract_text()
        texts.append(part_text)
    
    return "\n".join(texts)



def get_document_text():
	uploaded_doc: UploadedFile = st.session_state.get("doc_file", None)
	if not uploaded_doc:
		return

	if uploaded_doc.name.endswith(".txt"):
		print(uploaded_doc)
		text = uploaded_doc.read().decode("utf-8")
		st.session_state["doc"] = {
			"name": uploaded_doc.name,
			"text": text,
			"details": f"Number of lines: {len(text.splitlines())}\nNumber of words: {len(text.split())}"
		}
	
	elif uploaded_doc.name.endswith(".pdf"):
		text = pdf_to_markdown(uploaded_doc)

		st.session_state["doc"] = {
			"name": uploaded_doc.name,
			"text": text,
			"details": f"Number of pages: {len(text.split('\n'))}\nNumber of words: {len(text.split())}"
		}
		
	elif uploaded_doc.name.endswith(".docx"):
		doc = Document(uploaded_doc)
		text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

		st.session_state["doc"] = {
			"name": uploaded_doc.name,
			"text": text,
			"details": f"Number of paragraphs: {len(doc.paragraphs)}\nNumber of words: {len(' '.join([p.text for p in doc.paragraphs]).split())}"
		}
		
	else:
		st.error("Invalid file format. Only .docx and .pdf files are supported.")
		return


def print_document_details():
	doc_text = st.session_state.get("doc_text", None)
	if not doc_text:
		return

	st.markdown(f"### Uploaded document {doc_text['name']} Info")
	st.write(doc_text["details"])

