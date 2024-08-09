from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from core.settings import settings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": settings.DEVICE, "token": settings.HF_TOKEN},
)


vectorstore = Chroma(
    collection_name="nerd_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not neccesary
)

retriever = vectorstore.as_retriever()
