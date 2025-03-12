# utils.py

import time
from typing import List, Any, Callable
from langchain.text_splitter import CharacterTextSplitter

def split_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Splits the given text into smaller chunks using a character-based splitter.
    
    Args:
        text (str): The text to be split.
        chunk_size (int, optional): Maximum number of characters per chunk. Defaults to 1000.
        overlap (int, optional): Number of characters to overlap between chunks. Defaults to 200.
    
    Returns:
        List[str]: A list of text chunks.
    """
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

def create_batches(items: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Splits a list of items into batches of a specified size.
    
    Args:
        items (List[Any]): The list of items to batch.
        batch_size (int): The number of items per batch.
    
    Returns:
        List[List[Any]]: A list of batches (each batch is a list of items).
    """
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

def process_in_batches(
    items: List[Any],
    batch_size: int = 5,
    process_func: Callable[[List[Any]], None] = None,
    delay: int = 1
) -> None:
    """
    Processes a list of items in batches by applying a given process function
    to each batch with a delay between batches.
    
    This can help in cases where you're making API calls (e.g., embedding) and 
    need to avoid rate limits.
    
    Args:
        items (List[Any]): The list of items to process (e.g., text chunks).
        batch_size (int, optional): The number of items to process per batch. Defaults to 5.
        process_func (Callable[[List[Any]], None], optional): A function that processes a batch of items.
        delay (int, optional): Time in seconds to wait between batches. Defaults to 1.
    """
    batches = create_batches(items, batch_size)
    total_batches = len(batches)
    for i, batch in enumerate(batches, start=1):
        print(f"Processing batch {i} of {total_batches} (items {(i - 1) * batch_size + 1} to {(i - 1) * batch_size + len(batch)})...")
        if process_func:
            process_func(batch)
        time.sleep(delay)
