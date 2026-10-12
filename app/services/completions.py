import ollama


class CompletionService:
    @staticmethod
    def chat_completion(system_prompt: str, user_prompt: str):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})
        response = ollama.chat(model="qwen3:8b", messages=messages)
        return response["message"]["content"]
