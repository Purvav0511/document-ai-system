from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = PyPDFLoader("data/Purvav Punyani Combined Resume.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents(documents)

print(f"Number of document chunks after splitting: {len(docs)}")
for i, doc in enumerate(docs):
    print(f"\n--- Document chunk {i+1} ---\n{doc.page_content[:500]}")  # Preview first 500 chars
