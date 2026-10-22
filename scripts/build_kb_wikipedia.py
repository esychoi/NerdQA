import os
import re
import uuid
from collections.abc import Iterator

import chromadb
import mwparserfromhell
import pywikibot
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def remove_sections(wikipedia_text: str) -> str:
    sections = r"References|Notes|Citations|Sources|Primary|Secondary|Further reading|External links|Bibliography"
    pattern = r"(?im)^(" r"={1,6}\s*(?:" + sections + r")\s*={1,6}" r")\s*\n" r".*?" r"(?=^={1,6}(?!\=)|\Z)"
    return re.sub(pattern, "", wikipedia_text, flags=re.DOTALL | re.MULTILINE)


def preprocess_page_text(wikipedia_page_text: str) -> str:
    text = remove_sections(wikipedia_page_text)
    text = mwparserfromhell.parse(text)
    text = text.strip_code()
    return text


def get_wikipedia_pages(category: str) -> Iterator[tuple[str, str]]:
    site = pywikibot.Site("en", "wikipedia")
    wikipedia_category = pywikibot.Category(site, f"Category:{category}")
    wikipedia_pages = wikipedia_category.articles(namespaces=0)
    for page in wikipedia_pages:
        yield page.title(), preprocess_page_text(page.text)


if __name__ == "__main__":
    THEME = "LOTR"
    CATEGORIES = [
        "The_Lord_of_the_Rings",
        "The_Lord_of_the_Rings_characters",
        "Middle-earth_animals",
        "Middle-earth_objects",
    ]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""])
    embedding_function = OllamaEmbeddingFunction(
        model_name=os.getenv("EMBEDDING_MODEL_NAME"), url=os.getenv("OLLAMA_URL")
    )
    client = chromadb.PersistentClient(path=os.getenv("CHROMADB_PATH"))
    collection = client.get_or_create_collection(name=THEME, embedding_function=embedding_function)

    # Load the document
    for category in CATEGORIES:
        try:
            print(f"Processing category {category}")
            for page_title, page_text in get_wikipedia_pages(category):
                chunks = splitter.split_text(page_text)

                collection.add(
                    ids=[str(uuid.uuid4()) for _ in chunks],
                    documents=chunks,
                    metadatas=[
                        {
                            "source": "LOTR_Wikipedia",
                            "category": category,
                            "title": str(page_title),
                            "page_chunk": i,
                            "page_chunks": len(chunks),
                        }
                        for i in range(len(chunks))
                    ],
                )

            print(f"Successfully added category {category}")

        except Exception as e:
            print(f"Exception occurred with category {category}: {e}")
