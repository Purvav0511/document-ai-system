from agents.pdf_agent import load_and_store_pdf
from agents.csv_agent import load_and_store_csv
from agents.docx_agent import load_and_store_docx
from agents.json_agent import load_and_store_json

def route_agent(file_path):
    if file_path.endswith('.pdf'):
        return load_and_store_pdf(file_path)
    elif file_path.endswith('.csv'):
        return load_and_store_csv(file_path)
    elif file_path.endswith('.docx'):
        return load_and_store_docx(file_path)
    elif file_path.endswith('.json'):
        return load_and_store_json(file_path)
    else:
        raise ValueError("Unsupported file type")

# if __name__ == "__main__":
#     # Example test: manually specify a file to ingest.
#     test_file = "data/Purvav Punyani Combined Resume.pdf"  # or a CSV file
#     route_agent(test_file)
