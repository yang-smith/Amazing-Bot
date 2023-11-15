from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import BiliBiliLoader
from langchain.document_loaders import NewsURLLoader

loader_map = {
    'news': NewsURLLoader,
    'blibli': BiliBiliLoader,
    'http' : WebBaseLoader
}

def get_loader(url):
    for key, loader_func in loader_map.items():
        if key in url:
            return loader_func
    raise ValueError("No suitable loader found")
