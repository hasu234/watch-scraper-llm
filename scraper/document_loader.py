import os
import pandas as pd
from typing import List
from langchain_core.documents import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob

TEXT_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


def load_documents_into_database(model_name: str, documents_path: str) -> Chroma:
    print("Loading documents")
    raw_documents = load_documents(documents_path)
    documents = TEXT_SPLITTER.split_documents(raw_documents)

    print("Creating embeddings and loading documents into Chroma...")
    db = Chroma.from_documents(
        documents,
        OllamaEmbeddings(model=model_name),
    )
    print("Successfully loaded documents into Chroma.")
    return db

def load_documents(path: str) -> List[Document]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified path does not exist: {path}")

    loaders = {
        ".csv": load_csv_files,
    }

    docs = []
    for file_type, loader in loaders.items():
        print(f"Loading {file_type} files")
        if callable(loader):
            docs.extend(loader(path))
        else:
            docs.extend(loader.load())
    return docs

def load_csv_files(path: str) -> List[Document]:
    docs = []
    for file in glob.glob(os.path.join(path, "**/*.csv"), recursive=True):
        df = pd.read_csv(file)
        content = df.to_string()
        doc = Document(page_content=content, metadata={"source": file, "page": 1})
        docs.append(doc)
    return docs