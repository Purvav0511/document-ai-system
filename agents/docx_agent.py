import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from langchain.document_loaders import Docx2txtLoader
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from utils import split_text

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_and_store_docx(docx_path, chroma_db_path="./chroma_db", chunk_size=1000, overlap=200):
    print("Loading DOCX file...")
    loader = Docx2txtLoader(docx_path)
    docs = loader.load()
    
    all_docs = []
    for doc in docs:
        content = doc.page_content
        if len(content) > chunk_size:
            chunks = split_text(content, chunk_size=chunk_size, overlap=overlap)
            for idx, chunk in enumerate(chunks):
                new_doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": docx_path,
                        "file_type": "docx",
                        "chunk": idx + 1
                    }
                )
                all_docs.append(new_doc)
        else:
            new_doc = Document(
                page_content=content,
                metadata={"source": docx_path, "file_type": "docx"}
            )
            all_docs.append(new_doc)
    
    print(f"Created {len(all_docs)} document chunks from {docx_path}.")
    
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    chroma_db = Chroma.from_documents(all_docs, embeddings, persist_directory=chroma_db_path)
    print(f"✅ Successfully stored DOCX data from {docx_path} into ChromaDB.")

if __name__ == "__main__":
    docx_path = "data/sample3.docx"
    load_and_store_docx(docx_path)
