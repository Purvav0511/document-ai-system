import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI

def csv_agent(file_path):
    df = pd.read_csv(file_path)
    agent = create_pandas_dataframe_agent(ChatOpenAI(), df, verbose=True)
    return agent
