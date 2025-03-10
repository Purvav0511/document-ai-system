import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load Chroma DB
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
chroma_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Define prompt
prompt_template = ChatPromptTemplate.from_template("""
You are an assistant. Use the context below to answer the user's question.

Context: {context}

Question: {question}
""")

# LLM setup
llm = ChatOpenAI(model="gpt-4o")

# New LangChain interface
chain = prompt_template | llm

# Retrieval function
def retrieve_context(question, k=3):
    results = chroma_db.similarity_search(question, k=k)
    context = "\n\n".join(doc.page_content for doc in results)
    return context

# Main function
def answer_query(question):
    context = retrieve_context(question)
    response = chain.invoke({"context": context, "question": question})
    print("LLM Response:", response.content)

if __name__ == "__main__":
    user_question = "Tell me about my experience with cloud services?"
    answer_query(user_question)
