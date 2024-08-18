from aimakerspace.text_utils import TextFileLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
import asyncio  # supports asynchronous tasks
import numpy as np
import os

class DocumentManager:
    def __init__(self):
        self.run_time = 0

    def insert(self, key: str, vector: np.array) -> None:
        self.vectors[key] = vector

    def prepare_document(self, document_path: str, chunk_size=1000, chunk_overlap=200) -> VectorDatabase:
        try:
            if not os.path.isfile(document_path):
                raise FileNotFoundError(f"The document at '{document_path}' does not exist.")

            text_loader = TextFileLoader(document_path)
            documents = text_loader.load_documents()
            if not documents:
                raise ValueError(f"The document '{document_path}' is empty.")
            text_splitter = CharacterTextSplitter(chunk_size, chunk_overlap)  # default, if not passed is 1000, 200
            split_documents = text_splitter.split_texts(documents)
            vector_db = VectorDatabase()
            vector_db = asyncio.run(vector_db.abuild_from_list(split_documents))  
            print("Docuemnt processed - ready for querying")  
            return vector_db
        
        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

        return None 