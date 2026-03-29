import os
from dotenv import load_dotenv
from langchain.tools import tool
from sentence_transformers import SentenceTransformer
import weaviate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import atexit

load_dotenv()

weaviate_url = os.getenv("WEAVIATE_URL")
top_k_results = os.getenv("TOP_K_RESULTS")

transforms_embedding = SentenceTransformer("all-MiniLM-L6-v2") # todo : insert to .env
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

_weaviate_client = None # lazy initialization — only connect when first needed, not at import time


def get_weaviate_client():
    global _weaviate_client
    if _weaviate_client is None:
        _weaviate_client = weaviate.connect_to_local(host="localhost", port=8082, grpc_port=50052)
        atexit.register(_weaviate_client.close)
    return _weaviate_client

#todo: move to helpers/util functions
def embed_query(text: str) -> list[float]:
    """Convert any text to vector"""
    return transforms_embedding.encode(text).tolist()


@tool
def store_results(results: str):
    """Chunk → embed → insert into Weaviate"""
    chunks = splitter.split_text(results)

    collection = get_weaviate_client().collections.get("ResearchResults")
    with collection.batch.dynamic() as batch:
        for chunk in chunks:
            batch.add_object(
                properties={"content": chunk},
                vector= embed_query(chunk)
            )

@tool
def fetch_relevant_results(query: str) -> list[str]:
    """Embed query → search Weaviate → return closest chunks"""
    embedded_query = embed_query(query)
    collection = get_weaviate_client().collections.get("ResearchResults")
    results = collection.query.near_vector(near_vector=embedded_query, limit=5)
    return [obj.properties["content"] for obj in results.objects]




