from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from ingest_docs import ingest_all_documents

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INGEST_ON_STARTUP = os.getenv("INGEST_ON_STARTUP", "true").lower() == "true"

def check_chroma_db_exists(db_path="./chroma_db"):
    # Check if the directory exists and is non-empty
    return os.path.exists(db_path) and os.listdir(db_path)

app = FastAPI()

INGEST_MODE = os.getenv("INGEST_MODE", "none").lower()

scheduler = BackgroundScheduler()

if INGEST_MODE in ["scheduled", "both"]:
    # Schedule the ingestion function to run every 10 minutes
    scheduler.add_job(ingest_all_documents, 'interval', minutes=180)
    scheduler.start()
    print("Scheduled ingestion is enabled.")

@app.post("/ingest")
async def ingest_documents(background_tasks: BackgroundTasks):
    if INGEST_MODE in ["manual", "both"]:
        background_tasks.add_task(ingest_all_documents)
        return {"status": "Manual ingestion started"}
    else:
        return {"status": "Manual ingestion is disabled in the current configuration"}


embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
chroma_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_document(query_request: QueryRequest):
    question = query_request.question
    
    # Get relevant documents from Chroma
    docs = chroma_db.similarity_search(question, k=7)
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


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


@app.get("/health")
async def health_check():
    return {"status": "OK"}