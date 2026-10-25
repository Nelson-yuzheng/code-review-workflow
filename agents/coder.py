import os

from agents.base import BaseAgent
from llm import strip_code_fence
from tools import read_file


class CoderAgent(BaseAgent):
    name = "编码Agent"
    description = "读入或生成待审查的代码"

    def __init__(self):
        super().__init__()
        self.system_prompt = (
            "你是一名编码 Agent。根据用户的功能描述生成一段 Python 代码。"
            "只输出代码本身，不要输出解释或 markdown 代码块。"
        )

    def run(self, state):
        raw = state.raw_input.strip()

        if os.path.isfile(raw):
            state.code = read_file(raw)
            state.add_log(f"编码Agent：从文件读取代码 ({raw})")
        elif self._looks_like_code(raw):
            state.code = raw
            state.add_log("编码Agent：直接使用用户提供的代码")
        else:
            state.add_log("编码Agent：根据功能描述生成代码...")
            code = self.call_llm(
                [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": raw},
                ]
            )
            state.code = strip_code_fence(code)
            state.add_log("编码Agent：代码生成完成")

        state.record(self.name, {"code": state.code})
        return state

    @staticmethod
    def _looks_like_code(text):
        marks = [
            "def ", "class ", "import ", "print(", "return ",
            "function ", "const ", "let ", "=>", "{", "}", "=",
        ]
        if "\n" in text:
            return True
        return any(m in text for m in marks)
