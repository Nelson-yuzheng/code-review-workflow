from agents.base import BaseAgent
from llm import extract_json


class ReviewerAgent(BaseAgent):
    name = "审查Agent"
    description = "审查代码，输出结构化 JSON 审查报告"

    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一名专业的代码审查 Agent（复用项目 1 的审查逻辑）。
请审查用户提供的代码，重点关注：
1. 正确性：逻辑错误、边界条件、潜在 Bug、异常处理
2. 可读性：命名、注释、结构
3. 可维护性：重复代码、过长函数
4. 性能与安全

必须只输出一个 JSON 对象，不要输出任何其它文字或 markdown 代码块，格式如下：
{
  "summary": "总体评价（一句话）",
  "has_critical": true,
  "issues": [
    {
      "severity": "严重",
      "type": "逻辑错误",
      "location": "第3行",
      "description": "问题描述",
      "suggestion": "修改建议"
    }
  ]
}
要求：
- severity 只能是 "严重"、"建议"、"提示" 之一
- 只要存在 severity 为 "严重" 的问题，has_critical 必须为 true，否则为 false
- 如果没有问题，issues 为空数组 []
"""

    def run(self, state):
        state.add_log("审查Agent：开始审查...")
        content = self.call_llm(
            [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"请审查以下代码：\n```\n{state.code}\n```"},
            ],
            json_mode=True,
        )
        report = extract_json(content)
        if report is None:
            report = {
                "summary": "审查报告解析失败",
                "has_critical": False,
                "issues": [],
            }
        state.review_report = report
        state.add_log(
            f"审查Agent：发现 {len(report.get('issues', []))} 个问题，"
            f"严重问题={report.get('has_critical', False)}"
        )
        state.record(self.name, report)
        return state
