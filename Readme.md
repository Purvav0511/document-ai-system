# Multi-Agent Enterprise Document Q&A System

## Project Overview

This project demonstrates a multi-agent document Q&A system built with LangChain and FastAPI. It ingests various document types (PDF, CSV, JSON, DOCX), processes and embeds their content using OpenAI's models, and stores the embeddings in ChromaDB. The system then retrieves relevant document chunks via similarity search and uses an LLM (e.g., GPT-4) to answer user queries.

This illustrative project is designed for enterprise use cases—such as compliance and regulatory analysis—while also serving as a demo of how to build robust ingestion pipelines and unified query interfaces. Future enhancements include caching, conversation memory for dynamic Q&A, and a user-friendly document upload UI.

## Tech Stack

- **Python 3.10+**
- **FastAPI** – API framework for building the backend
- **LangChain** – For chaining LLM workflows
- **ChromaDB** – Vector database for storing document embeddings
- **OpenAI GPT-4 & Embeddings** – For natural language processing and answer generation
- **Pandas, Docx2txt, JSON** – For processing various document formats

## Project Structure



## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/document-ai-system.git
   cd document-ai-system
2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Configure Environment Variables:**
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   INGEST_MODE=manual  # Options: manual, scheduled, both, none

## Running the Application

### Document Ingestion

#### Manual Ingestion
Run the ingestion pipeline script to process files in the `data/` folder:

```bash
python ingest_docs.py
```
This script checks for new or updated documents (using a record system) and processes them with the appropriate agent (PDF, CSV, JSON, DOCX).

Ingestion Endpoint (Optional)
If enabled, you can trigger ingestion manually by calling the /ingest endpoint on the FastAPI server.

## Query API
  Start the FastAPI Server

  ```bash
  uvicorn app:app --reload
```

## Access the Interactive API Docs
Open http://127.0.0.1:8000/docs in your browser to test the /query endpoint.

## Submit a Query
Example queries:

"What are the main skills and experiences listed in the resume?"
"Summarize the crime trends from the CSV data."
"What are the key compliance points in the EU policy document?"
##Future Enhancements
# Caching and Query Optimization:
Implement persistent caching (e.g., using Redis) to store query results and reduce duplicate API calls.

# Dynamic Q&A with Memory:
Integrate conversation memory to support multi-turn dialogues, enabling the system to retain context across queries.

# User Interface Enhancements:
Develop a web UI (using Streamlit, React, etc.) that allows users to:

# Upload documents.
# Trigger ingestion.
# Interact with the Q&A system through a friendly dashboard.
# Automated Delta Ingestion:
Enhance the ingestion pipeline to automatically process only new or updated files based on a record system.

# LangFlow Integration:
Once the core features are stable, use LangFlow for visual prototyping and further prompt tuning.

##License
This project is licensed under the MIT License.

##Acknowledgments
LangChain: For providing powerful LLM chaining abstractions.
ChromaDB: For efficient vector storage and similarity search.
FastAPI: For building the backend API.
OpenAI: For GPT-4 and embedding models.
Community Contributors: Thank you to all those who helped build and improve the open-source tools used in this project.
   
