from dataclasses import dataclass


@dataclass
class ActionResult:
    action: str
    result: str

    def __str__(self) -> str:
        return f"Action {self.action}, Result: {self.result}"
