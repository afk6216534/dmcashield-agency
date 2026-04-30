from typing import Dict, List
from agents.base_agent import BaseAgent

class CodeReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodeReviewAgent")
        self.issues_found = 0

    def review_code(self, code: str, language: str = "python") -> Dict:
        issues = []
        if "import " not in code:
            issues.append("Missing imports")
        if len(code.splitlines()) > 100:
            issues.append("File too long")
        self.issues_found += len(issues)
        return {"issues": issues, "status": "reviewed"}

    def start(self):
        return {"status": "online", "issues_found": self.issues_found}
