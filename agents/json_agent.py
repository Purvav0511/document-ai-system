import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from utils import split_text, process_in_batches

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def normalize_json_content(file_path):
    """
    Attempts to load a JSON file in various ways and returns a formatted string.
    First, it tries to load it as a single JSON object/array.
    If that fails, it attempts to load it as JSON Lines (NDJSON).
    If both fail, it returns the raw text.
    """
    with open(file_path, 'r') as f:
        raw_text = f.read().strip()
    
    # Attempt to load as a single JSON object/array.
    try:
        data = json.loads(raw_text)
        return json.dumps(data, indent=2)
    except json.JSONDecodeError:
        pass
    
    # Attempt to load as NDJSON.
    try:
        lines = raw_text.splitlines()
        parsed_objects = [json.loads(line.strip()) for line in lines if line.strip()]
        return "\n".join(json.dumps(obj, indent=2) for obj in parsed_objects)
    except json.JSONDecodeError:
        pass
    
    # Fallback: return raw text.
    return raw_text

def load_and_store_json(json_path, chroma_db_path="./chroma_db", chunk_size=1000, overlap=200, batch_size=5):
    print("Reading JSON file...")
    formatted_text = normalize_json_content(json_path)
    print("JSON file normalized.")
    
    if len(formatted_text) > chunk_size:
        chunks = split_text(formatted_text, chunk_size=chunk_size, overlap=overlap)
    else:
        chunks = [formatted_text]
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={"source": json_path, "file_type": "json", "chunk": i+1}
        )
        documents.append(doc)
    
    print(f"Created {len(documents)} document chunks from {json_path}.")
    
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    chroma_db = Chroma(persist_directory=chroma_db_path, embedding_function=embeddings)
    
    def add_batch(batch_docs):
        texts = [doc.page_content for doc in batch_docs]
        metadatas = [doc.metadata for doc in batch_docs]
        chroma_db.add_texts(texts, metadatas=metadatas)
    
    process_in_batches(documents, batch_size=batch_size, process_func=add_batch, delay=1)
    
    print(f"✅ Successfully stored JSON data from {json_path} into ChromaDB.")

if __name__ == "__main__":
    # Replace with the path to your large JSON file.
    json_path = "data/titanic.json"
    load_and_store_json(json_path)
