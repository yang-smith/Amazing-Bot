
from tiktoken import encoding_for_model
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def db_init():
    if os.path.exists("./chroma_db"):
        print("Chroma DB already exists. Skipping the creation process.")
    else:
        loader = TextLoader("README.md") 
        documents = loader.load()   
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        docs = text_splitter.split_documents(documents)
        db = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings())
        db.persist(persist_directory="./chroma_db")

def docs_add(docs):
    db = Chroma.from_documents(embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")
    db.add_documents(docs)
    db.persist()

def token_count(splits, model = "gpt-3.5-turbo"):
    """splits: Documents or str"""
    encoding = encoding_for_model(model)
    token_count = 0
    if isinstance(splits, str):
        token_count = len(encoding.encode(splits))
    else:
        for split in splits:
            token_count += len(encoding.encode(split.page_content))
    return token_count


def show_search(query, db):
    results = db.similarity_search(query)
    result_str = ""
    
    for result in results:
        print(result.page_content)
        print("\n"+"-"*30 + "\n")
        result_str += result.page_content
    return result_str