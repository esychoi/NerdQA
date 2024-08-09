from langchain_core.messages import HumanMessage, SystemMessage

from llm.agents import chat_model


class CompletionService:
    @staticmethod
    def chat_completion(system_prompt: str, user_prompt: str):
        message = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        response = chat_model.invoke(message)
        return response
