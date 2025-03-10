from langchain.document_loaders import Docx2txtLoader

def docx_agent(file_path):
    loader = Docx2txtLoader(file_path)
    docs = loader.load()
    return docs
