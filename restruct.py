from prase import parse_bookmarks
from price import calculate_price
from prompts import prompt_vector
from utils import choose_bookmarks_file
from loader import get_loader
from vector_db import show_search, db_init, docs_add, token_count
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

def restruct():
    docs = []
    file_path = choose_bookmarks_file()
    if file_path:
        bookmarks = parse_bookmarks(file_path)
        for bookmark in bookmarks:
            try:
                loader_func = get_loader(bookmark['url'])
                loader = loader_func(bookmark['url'])
                docs += loader.load()
            except Exception as e:
                logging.error(f"Error processing bookmark {bookmark['url']}: {e}", exc_info=True)
            
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        splits = splitter.split_documents(docs)
        return splits
    return None