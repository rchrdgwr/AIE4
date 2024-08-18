import os
from typing import List
import fitz


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []  # contains a list of documents in text format
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        elif os.path.isfile(self.path) and self.path.endswith(".pdf"):
            self.load_pdf()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())
    
    def load_pdf(self):
        with fitz.open(self.path) as pdf_document:
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text()

            self.documents.append(text)


    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".txt"):
                    with open(
                        file_path, "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())
                if file.endswith(".pdf"):
                    with fitz.open(file_path) as pdf_document:  # Use the file_path here
                        text = ""
                        for page_num in range(pdf_document.page_count):
                            page = pdf_document.load_page(page_num)
                            text += page.get_text()
                        
                        self.documents.append(text)


    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    # chunking
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    # modification made to view changing chunk size and overlap
    loader = TextFileLoader("../data/combined_sagas.txt")
    loader.load()
    splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=10)
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[2])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
