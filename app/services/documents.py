from abc import ABC, abstractmethod
from uuid import uuid4

from fastapi import HTTPException
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .utils import get_cleaned_documents
from db.chroma_db import vectorstore


class BaseLoader(ABC):
    @abstractmethod
    def load(self, *args, **kwargs) -> list[Document]:
        """
        Abstract method to load data.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List: Loaded data.
        """
        ...

    def load_and_split(
        self,
        *,
        text_splitter=RecursiveCharacterTextSplitter,
        chunk_size: int = 800,
        overlap: int = 200,
    ) -> list[Document]:
        """
        Load documents and split them into chunks using a specified text splitter.

        Args:
            text_splitter (type, optional): The text splitter class or object to use for splitting.
            Defaults to RecursiveCharacterTextSplitter.
            chunk_size (int, optional): The size of each chunk in characters. Defaults to 800.
            overlap (int, optional): The overlap between consecutive chunks in characters. Defaults to 200.

        Returns:
            List[Document]: A list of Document objects representing the split chunks of text.

        Raises:
            TypeError: If the provided text splitter is not a callable or does not have required methods.
            ValueError: If chunk_size or overlap are not positive integers.
            Exception: Any other unexpected errors that occur during loading or splitting.

        Example:
            >>> loader = inherited class
            >>> chunks = loader.load_and_split(chunk_size=1000, overlap=300)
            >>> for chunk in chunks:
            >>>     print(f"Chunk metadata: {chunk.metadata}")
            >>>     print(f"Chunk content: {chunk.page_content}")
        """
        try:
            # Validate parameters
            if not isinstance(chunk_size, int) or chunk_size <= 0:
                raise ValueError("chunk_size must be a positive integer.")
            if not isinstance(overlap, int) or overlap < 0:
                raise ValueError("overlap must be a non-negative integer.")

            # Create text splitter instance
            text_splitter = text_splitter(chunk_size=chunk_size, chunk_overlap=overlap)

            # Load documents
            documents = self.load()

            # Split documents using text splitter
            return text_splitter.split_documents(documents)

        except TypeError as e:
            print(f"TypeError in load_and_split: {e}")
            raise
        except ValueError as e:
            print(f"ValueError in load_and_split: {e}")
            raise
        except Exception as e:
            print(f"Error in load_and_split: {e}")
            raise


class WebDataLoader(BaseLoader):
    def __init__(self, urls: list[str]):
        self._urls: list[str] = urls

    def load(self) -> list[Document]:
        try:
            if not isinstance(self._urls, list):
                raise TypeError("url path must be a list of string.")
            if not self._urls:
                raise ValueError("url path cannot be empty.")

            documents = WebBaseLoader(self._urls).load()
            return get_cleaned_documents(documents)

        except TypeError as e:
            print(f"TypeError: {e}")
            raise

        except ValueError as e:
            print(f"ValueError: {e}")
            raise

        except Exception as e:
            print(f"Error loading PDF: {e}")
            raise


class DocumentService:
    @staticmethod
    def create(type: str, name: str):
        if type == "web":
            document_splits = WebDataLoader(urls=[name]).load_and_split()
            uuids = [str(uuid4()) for _ in range(len(document_splits))]
            vectorstore.add_documents(document_splits, ids=uuids)
        else:
            raise Exception(
                f"Unknown document type: got {name}, expected one of ['web']."
            )

    def read():
        pass

    def update():
        pass

    def delete():
        pass


# if __name__ == "__main__":

#     loader = WebDataLoader(urls=["https://en.wikipedia.org/wiki/One_Piece"])
#     docs = loader.load_and_split()

#     print(type(docs), len(docs), type(docs[0]))
#     print(docs[0])
