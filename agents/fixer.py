import json

from agents.base import BaseAgent
from llm import strip_code_fence


class FixerAgent(BaseAgent):
    name = "修复Agent"
    description = "根据审查报告修复代码"

    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一名代码修复 Agent。根据审查报告中的问题修复代码。
要求：
- 只修复审查报告中列出的问题，不做无关改动
- 保持代码原有风格和功能不变
- 只输出修复后的完整代码，不要输出任何解释或 markdown 代码块
"""

    def run(self, state):
        state.add_log("修复Agent：开始修复...")
        issues = json.dumps(state.review_report.get("issues", []), ensure_ascii=False)
        content = self.call_llm(
            [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": f"审查报告：\n{issues}\n\n原始代码：\n```\n{state.code}\n```",
                },
            ]
        )
        state.code = strip_code_fence(content)
        state.add_log("修复Agent：修复完成")
        state.record(self.name, {"code": state.code})
        return state
