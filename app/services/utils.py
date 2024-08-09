import re

from langchain_core.documents import Document


def cleanse_whitespace(text: str) -> str:
    """
    Remove newline characters (\n), tabs (\t), carriage returns (\r), and
    consecutive spaces from the input text.

    Args:
        text (str): The input text to cleanse.

    Returns:
        str: The cleansed text with all whitespace characters replaced and
             consecutive spaces reduced to a single space.

    Raises:
        TypeError: If the input `text` is not a string.

    Example:
        >>> cleanse_whitespace("Hello\\n\\tWorld!\\r How are you?\\n\\n")
        'Hello World! How are you?'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    try:
        # Replace newline characters, tabs, and carriage returns with a space
        text = re.sub(r"[\n\t\r]", " ", text)

        # Replace multiple spaces with a single space
        text = re.sub(r"\s+", " ", text)

        # Strip leading and trailing whitespace
        text = text.strip()

        return text

    except Exception as e:
        print(f"Error: {e}")
        raise


def get_cleaned_documents(documents: list[Document]) -> list[Document]:
    """
    Clean the page content of each document in the provided list by removing
    unwanted whitespace characters and returning a list of cleaned documents.

    Args:
        documents (List[Document]): A list of Document objects to be cleaned.

    Returns:
        List[Document]: A list of Document objects with cleaned page content.

    Raises:
        TypeError: If the input documents is not a list of Document objects.
        Exception: For any unexpected errors that occur during cleaning.

    Example:
        >>> documents = [Document(page_content="Some text\nwith whitespace\t", metadata={"id": 1})]
        >>> cleaned_documents = get_cleaned_documents(documents)
        >>> for doc in cleaned_documents:
        >>>     print(f"Metadata: {doc.metadata}")
        >>>     print(f"Cleaned content: {doc.page_content}")
    """
    try:
        if not isinstance(documents, list):
            raise TypeError("Input must be a list of Document objects.")
        for doc in documents:
            if not isinstance(doc, Document):
                raise TypeError("All items in the input list must be Document objects.")

        return [
            Document(
                page_content=cleanse_whitespace(doc.page_content), metadata=doc.metadata
            )
            for doc in documents
        ]

    except TypeError as e:
        print(f"TypeError in get_cleaned_documents: {e}")
        raise
    except Exception as e:
        print(f"Error in get_cleaned_documents: {e}")
        raise
