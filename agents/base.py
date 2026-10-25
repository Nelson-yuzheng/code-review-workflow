from abc import ABC, abstractmethod

from llm import chat


class BaseAgent(ABC):
    name = "base"
    description = ""

    def __init__(self):
        self.system_prompt = ""

    def call_llm(self, messages, temperature=0.3, json_mode=False):
        response = chat(messages, temperature=temperature, json_mode=json_mode)
        return response.choices[0].message.content or ""

    @abstractmethod
    def run(self, state):
        raise NotImplementedError
