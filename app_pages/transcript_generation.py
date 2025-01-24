import streamlit as st
import openai


model = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def transcript_audio(audio_file):
    with st.spinner("Transcribing audio..."):
        transcript = openai.audio.transcriptions.create(
			model=st.secrets["OPENAI_AUDIO_MODEL"],
			file=audio_file,
			language="en",
			prompt="Transcribe the following audio, provide timestamps with timestamps according to the format: [timestamp] text",
		)
    
    return transcript.text
    

def main():
	st.title("Document Transcript Generation")
 
	audio_file = st.file_uploader("Upload an Audio to transcribe", type=["mp3", "wav", "m4a"], key="audio_file")

	if audio_file:
		transcript = transcript_audio(audio_file=audio_file)
		st.markdown("### Transcribed text")
		st.write(transcript)
    
main()