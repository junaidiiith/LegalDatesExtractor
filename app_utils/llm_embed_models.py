from llama_index.llms.fireworks import Fireworks
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
import openai
from app_utils.constants import *
import streamlit as st


def get_llm():
    llm_type = st.secrets[LLM_TYPE]
    if llm_type == OPENAI:
        return OpenAI(
            model=st.secrets[OPENAI_MODEL],
            api_key=st.secrets[OPENAI_API_KEY]
        )
    elif llm_type == FIREWORKS:
        return Fireworks(
            model=st.secrets[FIREWORKS_LLM],
            api_key=st.secrets[FIREWORKS_API_KEY]
        )
    else:
        raise ValueError(f"Unknown LLM type: {llm_type}")


def get_embed_model():
    embed_model_type = st.secrets[EMBED_MODEL_TYPE]
    if embed_model_type == OPENAI:
        return OpenAIEmbedding(
            api_key=st.secrets[OPENAI_API_KEY],
            embed_batch_size=st.secrets[EMBED_BATCH_SIZE]
        )
    elif embed_model_type == FIREWORKS:
        return FireworksEmbedding(
            api_key=st.secrets[FIREWORKS_API_KEY],
            embed_batch_size=st.secrets[EMBED_BATCH_SIZE]
        )
    else:
        raise ValueError(f"Unknown embedding model type: {embed_model_type}")
    

def get_llm_client():
    llm_type = st.secrets[LLM_TYPE]
    if llm_type == OPENAI:
        client = openai.OpenAI(api_key=st.secrets[OPENAI_API_KEY])
    elif llm_type == FIREWORKS:
        client = openai.OpenAI(
            base_url="https://api.fireworks.ai/inference/v1",
            api_key=st.secrets[FIREWORKS_API_KEY]
        )
    else:
        raise ValueError('Invalid LLM type')
    
    return client

def get_llm_model_id():
    llm_type = st.secrets[LLM_TYPE]
    if llm_type == OPENAI:
        return st.secrets[OPENAI_MODEL]
    elif llm_type == FIREWORKS:
        return st.secrets[FIREWORKS_LLM]
    else:
        raise ValueError('Invalid LLM type')



def get_llm_response(messages):
    client = get_llm_client()
    chat_completion = client.chat.completions.create(
        model=get_llm_model_id(),
        messages=messages,
    )
    response = chat_completion.choices[0].message.content
    return response


def render_llm_response(messages, stream=False):
    client = get_llm_client()
    
    if not stream:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_completion = client.chat.completions.create(
                    model=get_llm_model_id(),
                    messages=messages,
                )
                response = chat_completion.choices[0].message.content
            st.markdown(response)
            return response
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            while True:
                try:
                    chat_completion_response = client.chat.completions.create(
                        model=get_llm_model_id(),
                        messages=messages,
                        stream=True,
                    )
                    for response in chat_completion_response:
                        full_response += (response.choices[0].delta.content or "")
                        message_placeholder.markdown(full_response + "▌")

                except openai.BadRequestError as e:
                    error_message = (e.response.json()['error']['message'] or "")
                    if 'PromptTooLongError' in error_message:
                        print("Prompt too long, removing first message...")
                        messages.pop(0)
                    

                    full_response = ""

                if full_response != "":
                    break
            message_placeholder.markdown(full_response)
        # st.markdown(full_response)
        return full_response