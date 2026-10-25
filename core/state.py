from dataclasses import dataclass, field


@dataclass
class WorkflowState:
    raw_input: str = ""
    code: str = ""
    review_report: dict = field(default_factory=dict)
    iteration: int = 0
    max_iterations: int = 3
    logs: list = field(default_factory=list)
    history: list = field(default_factory=list)

    def add_log(self, message):
        self.logs.append(message)

    def record(self, agent_name, data):
        self.history.append({"agent": agent_name, "data": data})

    def to_dict(self):
        return {
            "code": self.code,
            "review_report": self.review_report,
            "iteration": self.iteration,
            "logs": self.logs,
            "history": self.history,
        }
