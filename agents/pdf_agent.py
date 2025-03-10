import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_and_store_pdf(pdf_path, chroma_db_path="./chroma_db"):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    # Embeddings
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # Store into ChromaDB
    chroma_db = Chroma.from_documents(pages, embeddings, persist_directory=chroma_db_path)
    chroma_db.persist()
    print(f"✅ Successfully stored {len(pages)} pages into ChromaDB.")

if __name__ == "__main__":
    pdf_path = "data/Purvav Punyani Combined Resume.pdf"
    load_and_store_pdf(pdf_path)
