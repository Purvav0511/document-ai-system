# main.py updated example
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM and embeddings
llm = ChatOpenAI(model="gpt-4o")
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Initialize ChromaDB
chroma = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Store a test embedding
chroma.add_texts(["Hello, ChromaDB!"])

# Query similar texts
results = chroma.similarity_search("Hello!")
print("ChromaDB Results:", results)

# Test your LLM
response = llm.invoke("Hello, world! Are you working?")
print("LLM Response:", response.content)
