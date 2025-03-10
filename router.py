from pdf_agent import pdf_agent
from csv_agent import csv_agent
from docx_agent import docx_agent
from json_agent import json_agent

def route_agent(file_path):
    if file_path.endswith('.pdf'):
        return pdf_agent(file_path)
    elif file_path.endswith('.csv'):
        return csv_agent(file_path)
    elif file_path.endswith('.docx'):
        return docx_agent(file_path)
    elif file_path.endswith('.json'):
        return json_agent(file_path)
    else:
        raise ValueError("Unsupported file type")
