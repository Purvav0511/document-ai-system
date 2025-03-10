from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
chroma_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_document(query_request: QueryRequest):
    question = query_request.question
    
    # Get relevant documents from Chroma
    docs = chroma_db.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Properly structured prompt
    prompt_template = ChatPromptTemplate.from_template("""
    You are an AI assistant tasked with answering user questions based only on the provided context. 
    Provide a structured, concise answer with bullet points and summarize relevant information clearly.
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """)

    chain = LLMChain(llm=llm, prompt=prompt_template)
    answer = chain.invoke({"context": context, "question": question})

    return {
        "answer": {
            "question": question,
            "text": answer['text'].strip(),
            "context": context
        }
    }
