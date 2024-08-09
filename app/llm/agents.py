from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from core.settings import settings


llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    huggingfacehub_api_token=settings.HF_TOKEN,
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

chat_model = ChatHuggingFace(llm=llm, verbose=True)
