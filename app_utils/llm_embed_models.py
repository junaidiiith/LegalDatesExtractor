from llama_index.llms.fireworks import Fireworks
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
import os
from llama_index.core.llms import ChatMessage
from app_utils.constants import *
from dotenv import load_dotenv
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
            embed_batch_size=st.secrets[EMBED_BATCH_SIZE, 16]
        )
    elif embed_model_type == FIREWORKS:
        return FireworksEmbedding(
            api_key=st.secrets[FIREWORKS_API_KEY],
            embed_batch_size=st.secrets[EMBED_BATCH_SIZE, 16]
        )
    else:
        raise ValueError(f"Unknown embedding model type: {embed_model_type}")
    

def get_llm_response(query: str, system_prompt: str = None, llm=None):
    if llm is None:
        llm = get_llm()
    messages = [ChatMessage(role = "system", content=system_prompt)] if system_prompt else []
    messages.append(ChatMessage(role="user", content=query))
    response = llm.chat(messages)
    return response.message.blocks[0].text.strip()