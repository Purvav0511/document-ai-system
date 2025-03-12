# pdf_agent.py

import os
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import split_text, process_in_batches

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_and_store_pdf(pdf_path, chroma_db_path="./chroma_db", chunk_size=1000, overlap=200):
    # Load PDF pages using PyPDFLoader
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    
    all_docs = []
    for page in pages:
        content = page.page_content
        # If a page is longer than our chunk_size, further split it.
        if len(content) > chunk_size:
            chunks = split_text(content, chunk_size=chunk_size, overlap=overlap)
            for idx, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": pdf_path,
                        "file_type": "pdf",
                        "page": page.metadata.get("page", None),
                        "chunk": idx + 1
                    }
                )
                all_docs.append(doc)
        else:
            doc = Document(
                page_content=content,
                metadata={"source": pdf_path, "file_type": "pdf", "page": page.metadata.get("page", None)}
            )
            all_docs.append(doc)
    
    print(f"Created {len(all_docs)} document chunks from {pdf_path}.")
    
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    chroma_db = Chroma.from_documents(all_docs, embeddings, persist_directory=chroma_db_path)
    chroma_db.persist()
    print(f"✅ Successfully stored PDF data from {pdf_path} into ChromaDB.")

if __name__ == "__main__":
    pdf_path = "data/CELEX_32016R0679_EN_TXT.pdf"
    load_and_store_pdf(pdf_path)
