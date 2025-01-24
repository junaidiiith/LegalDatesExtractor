from llama_index.core import get_response_synthesizer
from llama_index.core.schema import Document
from app_utils.llm_embed_models import get_embed_model, get_llm, get_llm_response
from app_utils.prompts import SUMMARIES_MERGING_PROMPT, SUMMARIZATION_PROMPT
from settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    chroma_data_dir    
)

from llama_index.core import (
    StorageContext, 
    load_index_from_storage
)

from llama_index.core import DocumentSummaryIndex
from llama_index.core.node_parser import SentenceSplitter

from llama_index.core.indices.document_summary import (
    DocumentSummaryIndexLLMRetriever,
    DocumentSummaryIndexEmbeddingRetriever
)
from llama_index.core.query_engine import RetrieverQueryEngine
from stqdm import stqdm
import shutil


SIMILARITY_TOP_K = 2


def get_nodes_from_documents(data: str):
    splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    docs = splitter.split_text(data)
    print("Total number of documents generated:", len(docs))
    return [
        Document(text=doc)
        for doc in docs
    ]

def create_index_from_document(
    data: str, 
    index_name: str = 'default',
    response_mode="tree_summarize"
):
    shutil.rmtree(f"{chroma_data_dir}/{index_name}", ignore_errors=True)
    nodes = get_nodes_from_documents(data)
    response_synthesizer = get_response_synthesizer(
        response_mode=response_mode, 
        use_async=True
    )
    doc_summary_index = DocumentSummaryIndex.from_documents(
        documents=nodes,
        llm=get_llm(),
        response_synthesizer=response_synthesizer,
        show_progress=True,
    )
    print(f"Persisting index to {chroma_data_dir}/{index_name}")
    doc_summary_index.storage_context.persist(f"{chroma_data_dir}/{index_name}")
    return doc_summary_index


def get_vector_index(
    index_name: str, 
) -> DocumentSummaryIndex:
    storage_context = StorageContext.from_defaults(persist_dir=f"{chroma_data_dir}/{index_name}")
    doc_summary_index = load_index_from_storage(storage_context)
    return doc_summary_index


def get_response(
    query: str, 
    index_name: str, 
    retrieval_mode: str = 'embed',
    response_mode="tree_summarize"
):
    doc_summary_index = get_vector_index(index_name)
    if retrieval_mode == 'embed':
        retriever = DocumentSummaryIndexEmbeddingRetriever(
            index=doc_summary_index,
            similarity_top_k=SIMILARITY_TOP_K,
            embed_model=get_embed_model(),
        )
    elif retrieval_mode == 'llm':
        retriever = DocumentSummaryIndexLLMRetriever(
            doc_summary_index,
            get_llm(),
            choice_top_k=SIMILARITY_TOP_K
        )
    else:
        raise ValueError(f"Unknown retrieval mode: {retrieval_mode}")
    
    response_synthesizer = get_response_synthesizer(
        response_mode=response_mode
    )

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )

    # query
    response = query_engine.query(query)
    return response


def doc_summarize_by_chunk(data: str):
    nodes = get_nodes_from_documents(data)
    chunk_summaries = [
        get_llm_response(node.text, system_prompt=SUMMARIZATION_PROMPT)
        for node in stqdm(nodes, desc="Summarizing Document")
    ]
    chunk_summaries_text = "\n".join(chunk_summaries)
    
    return get_llm_response(chunk_summaries_text, system_prompt=SUMMARIES_MERGING_PROMPT)