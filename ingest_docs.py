import os
import json
from datetime import datetime
from router import route_agent  # Your router dispatches files to the correct agent

# Path to the JSON file that records ingested documents
INGEST_RECORD_PATH = "ingested_files.json"

def load_ingestion_record():
    """Load the record of ingested files from a JSON file."""
    if os.path.exists(INGEST_RECORD_PATH):
        with open(INGEST_RECORD_PATH, "r") as f:
            return json.load(f)
    return {}

def save_ingestion_record(record):
    """Save the updated ingestion record to a JSON file."""
    with open(INGEST_RECORD_PATH, "w") as f:
        json.dump(record, f, indent=2)

def should_ingest(file_path, record):
    """
    Determine whether a file should be ingested.
    Checks if the file is not in the record or if it has been modified since last ingestion.
    """
    if file_path in record:
        last_modified = os.path.getmtime(file_path)
        # If file's last modification time is less than or equal to the stored timestamp, skip ingestion.
        if last_modified <= record[file_path]["last_modified"]:
            return False
    return True

def update_record(file_path, record):
    """Update the record for a given file after successful ingestion."""
    record[file_path] = {
        "last_modified": os.path.getmtime(file_path),
        "ingested_at": datetime.now().isoformat()
    }
    save_ingestion_record(record)

def ingest_all_documents(directory="./data"):
    """Iterate over files in the data directory, ingesting only new or updated files."""
    record = load_ingestion_record()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if should_ingest(file_path, record):
            try:
                print(f"Ingesting {file_path} ...")
                # Dispatch file to the appropriate agent via your router
                route_agent(file_path)
                print(f"✅ Processed {filename}")
                update_record(file_path, record)
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
        else:
            print(f"Skipping {file_path} (already ingested)")

if __name__ == "__main__":
    ingest_all_documents()
