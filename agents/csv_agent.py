import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from utils import process_in_batches

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_and_store_csv(csv_path, chroma_db_path="./chroma_db", chunk_size=1000, batch_size=5):
    print("Reading CSV file...")
    df = pd.read_csv(csv_path)
    print(f"CSV file read successfully. DataFrame shape: {df.shape}")
    
    documents = []
    num_chunks = (len(df) // chunk_size) + 1
    for i in range(num_chunks):
        chunk = df.iloc[i*chunk_size:(i+1)*chunk_size]
        if chunk.empty:
            continue
        csv_text = chunk.to_csv(index=False)
        doc = Document(
            page_content=csv_text,
            metadata={"source": csv_path, "file_type": "csv", "chunk": i+1}
        )
        documents.append(doc)
    
    print(f"Created {len(documents)} document chunks from {csv_path}.")
    
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    chroma_db = Chroma(persist_directory=chroma_db_path, embedding_function=embeddings)
    
    def add_batch(batch_docs):
        texts = [doc.page_content for doc in batch_docs]
        metadatas = [doc.metadata for doc in batch_docs]
        chroma_db.add_texts(texts, metadatas=metadatas)
    
    process_in_batches(documents, batch_size=batch_size, process_func=add_batch, delay=1)
    
    # No longer needed: chroma_db.persist()
    print(f"✅ Successfully stored CSV data from {csv_path} into ChromaDB.")

if __name__ == "__main__":
    csv_path = "data/Crime_Data_from_2020_to_Present.csv"
    load_and_store_csv(csv_path)
