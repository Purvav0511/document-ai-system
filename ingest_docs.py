import os
from router import route_agent

DATA_DIR = "./data"

def ingest_all_documents(directory=DATA_DIR):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            print(f"Ingesting {file_path} ...")
            docs = route_agent(file_path)
            print(f"✅ Processed {filename}: {len(docs) if isinstance(docs, list) else 'agent output'}")
        
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            

if __name__ == "__main__":
    ingest_all_documents()