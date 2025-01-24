import streamlit as st

import openai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from stqdm import stqdm

from app_utils.doc_processing import get_document_text, print_document_details
from settings import CHUNK_OVERLAP, CHUNK_SIZE


model = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
system_prompt = {
    "role": "system", 
    "content": "You are an expert in reading legal criminal cases and you need to extract the dates and the details about what happened on that date."
}


def get_dates_details(text, messages=None):
	if messages is None:
		messages = [system_prompt]

	prompt = \
	f"""
	You need to extract the dates and the details about what happened on that date. 
	Provide empty string in case there are no dates present.
	Any date that involves an event should be extracted.

	Extract the dates from the following text:
	{text}

	Example: 
	Input: The present reference is an abuse of the process. 
	The claimants, on an earlier occasion, had initiated another Arbitration reference, involving disputes purportedly arising out of the self same agreement dated 10th November, 2008, against the present respondents, which ultimately resulted into an Award dated 5th May, 2022.  

	Output:
	- 10th November, 2008: The claimants initiated an Arbitration reference involving disputes purportedly arising out of the self same agreement.
	- 5th May, 2022: The Arbitration reference resulted into an Award.
	"""
	response = model.chat.completions.create(
		model="gpt-4o",
		messages=messages + [
			{"role": "user", "content": prompt}
		],
	)
	ai_response = response.choices[0].message.content
	# time.sleep(0.01)
	# ai_response = "Good job! You have successfully extracted the dates and the details about what happened on that date."
	messages.append({"role": "assistant", "content": ai_response})
	
	return messages


def refine_dates_texts():
	doc_dates = st.session_state.get("doc_dates", None)

	if not doc_dates:
		st.error("No document dates found.")
		return
	
	doc_dates_refined = st.session_state.get("doc_dates_refined", None)
		
	if not doc_dates_refined:
		prompt = \
		f"""
		You are provided with a list of dates and what happened on those dates.
		The event on all these dates may be interconnected and therefore some date might be missing some information.
		You need to refine the the details about what happened on each date from the following text:
		{doc_dates}
		"""
		with st.spinner("Refining dates and details..."):
			# time.sleep(1)
			response = model.chat.completions.create(
				model="gpt-4o",
				messages=[
					{"role": "system", "content": "You are an expert in reading legal criminal cases and finding the missing details about the dates and events."},
					{"role": "user", "content": prompt},
				],
			)
			doc_dates_refined = response.choices[0].message.content
			# doc_dates_refined = "Amazing! You have successfully refined the details about what happened on each date."
			
		st.session_state["doc_dates_refined"] = doc_dates_refined


def get_document_dates():
	doc = st.session_state.get("doc", None)
	if not doc or not doc.get("text", None):
		st.error("No text found in the document.")
		return
	text = doc["text"]
	doc_dates = st.session_state.get("doc_dates", None)

	if not doc_dates:
		chunk_size = st.session_state.get("chunk_size", CHUNK_SIZE)
		chunk_overlap = st.session_state.get("chunk_overlap", CHUNK_OVERLAP)
		text_splitter = RecursiveCharacterTextSplitter(
			chunk_size=chunk_size, 
			chunk_overlap=chunk_overlap
		)
		texts = text_splitter.split_text(text)
		
		messages = None

		for text in stqdm(texts, desc="Extracting dates and details"):
			messages = get_dates_details(text, messages=messages)
		
		doc_dates = "\n".join([m['content'] for m in messages if m['role'] == 'assistant'])
		st.session_state["doc_dates"] = doc_dates


def reset():
	st.session_state["doc"] = None
	st.session_state["doc_dates"] = None
	st.session_state["doc_dates_refined"] = None
	
    
def main():
	st.title("Legal Document Dates Extractor")

	# with st.expander("Size of text to process at once"):
	# 	cols = st.columns(2)
	# 	cols[0].number_input("Chunk size", value=5000, key="chunk_size", help="The size of the text to be processed at a time. Default is 5000.")
	# 	cols[1].number_input("Chunk overlap", value=100, key="chunk_overlap", help="The overlap between chunks. Default is 50.")

	st.file_uploader("Upload a document", type=["docx", "pdf"], key="doc_file", on_change=get_document_text)
	doc = st.session_state.get("doc_file", None)
	
	extract_dates, refine_dates = False, False
	if doc:
		print_document_details()
		cols = st.columns(3)
		
		extract_dates = cols[0].button("Extract dates and details", key="extract_dates", on_click=get_document_dates)
		refine_dates = cols[1].button("Refine dates and details", key="refine_dates", on_click=refine_dates_texts)
		cols[2].button("Reset Document", key="reset", on_click=reset)
		

	if extract_dates or st.session_state.get("doc_dates", None):
		with st.container():
			doc_dates = st.session_state.get("doc_dates")
			st.markdown("### Extracted dates and details\n" + doc_dates)
			st.session_state["doc_dates"] = doc_dates
	
	if refine_dates or st.session_state.get("doc_dates_refined", None):
		with st.container():
			doc_dates_refined = st.session_state.get("doc_dates_refined")
			st.markdown("### Refined dates and details")
			st.write(doc_dates_refined)

main()