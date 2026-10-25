import json
import os
from datetime import datetime

from agents.coder import CoderAgent
from agents.fixer import FixerAgent
from agents.reviewer import ReviewerAgent
from core.logger import LOG_DIR, log
from core.state import WorkflowState


class Workflow:
    def __init__(self, state=None):
        self.state = state or WorkflowState()
        self.registry = {
            "coder": CoderAgent(),
            "reviewer": ReviewerAgent(),
            "fixer": FixerAgent(),
        }

    def add_agent(self, key, agent):
        self.registry[key] = agent

    def _run_step(self, key):
        agent = self.registry[key]
        log(f"▶ {agent.name} 开始", "STEP")
        self.state = agent.run(self.state)
        return self.state

    def run(self):
        log("=" * 60)
        log("Workflow 启动：编码 → 审查 → (修复 → 审查) 循环")
        log("=" * 60)
        try:
            self._run_step("coder")

            for round_num in range(1, self.state.max_iterations + 1):
                self._run_step("reviewer")
                if not self.state.review_report.get("has_critical"):
                    log("✓ 审查通过，流程结束", "DONE")
                    break
                log(f"发现严重问题，第 {round_num} 轮修复...", "WARN")
                self._run_step("fixer")
                self.state.iteration = round_num
            else:
                log("⚠ 达到最大审查轮数，流程结束", "WARN")
        except Exception as e:
            log(f"✗ 流程出错：{e}", "ERROR")
            raise
        finally:
            self._save_result()
        return self.state

    def _save_result(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = os.path.join(LOG_DIR, f"result_{ts}.json")
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(self.state.to_dict(), f, ensure_ascii=False, indent=2)
        log(f"结果已保存到 {result_path}")

        code_path = os.path.join(LOG_DIR, f"final_code_{ts}.py")
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(self.state.code)
        log(f"最终代码已保存到 {code_path}")
