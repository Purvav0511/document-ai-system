from langchain.docstore.document import Document
import json

def json_agent(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    # Simply convert JSON to a readable document format
    docs = [{"page_content": json.dumps(data, indent=2)}]
    return docs
