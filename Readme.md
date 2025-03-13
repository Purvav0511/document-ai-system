# Multi-Agent Enterprise Document Q&A System

## Overview

This project is a LangChain-powered multi-agent system designed to ingest and process various types of documents—PDFs, CSVs, JSONs, and DOCXs—and answer user queries based on the extracted content. The system stores document embeddings in ChromaDB (a vector database) and uses a unified query endpoint to retrieve relevant document chunks and generate answers via an LLM (e.g., GPT-4).

This repository is intended for demonstration and illustrative purposes. It is built and deployed locally, with future plans to add caching, a user-friendly UI, and conversation memory for multi-turn Q&A.

## Features

- **Multi-Document Ingestion:**
  - **PDF Agent:**  
    Uses `PyPDFLoader` to extract and split PDF pages, further splitting long pages into manageable chunks.
  - **CSV Agent:**  
    Reads CSV files using Pandas, splits the data into row-based chunks, and processes them in batches.
  - **JSON Agent:**  
    Handles various JSON formats (standard JSON and NDJSON) and normalizes them into a consistent, pretty-printed format.
  - **DOCX Agent:**  
    Uses `Docx2txtLoader` to extract text from DOCX files and splits the content as needed.

- **Unified Vector Storage:**  
  All processed document chunks are embedded using OpenAIEmbeddings and stored in a unified ChromaDB vector store, making similarity search straightforward.

- **Unified Query Endpoint:**  
  A FastAPI endpoint receives user queries, retrieves relevant document chunks from ChromaDB, constructs a prompt with a predefined template, and generates a final answer using an LLM chain (ChatOpenAI).

- **Future Enhancements:**  
  Planned improvements include:
  - **Caching and Reuse:**  
    Persisting query results to reduce repeated API calls.
  - **Dynamic Q&A with Memory:**  
    Supporting multi-turn conversations with conversation memory.
  - **Document Upload UI:**  
    A frontend interface for users to upload new documents.
  - **Automated Delta Ingestion:**  
    Ingesting only new or updated files based on a record system.

## Architecture

### High-Level Flow Diagram




### Component Details

- **Ingestion Pipeline:**  
  Files placed in the `data/` directory are processed by a router that dispatches to the appropriate agent based on file extension. Each agent extracts, normalizes, and chunks the document content before embedding it into ChromaDB.

- **Unified Query API:**  
  The FastAPI backend’s `/query` endpoint performs a similarity search on the unified ChromaDB. It aggregates context from the top matching chunks, builds a prompt using a predefined template, and generates an answer via a ChatOpenAI chain.

- **Future Enhancements:**  
  Future work includes adding caching for query results, implementing conversation memory for dynamic multi-turn Q&A, and building a user interface for document uploads.

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/document-ai-system.git
   cd document-ai-system
