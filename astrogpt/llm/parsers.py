from typing import Optional
from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field  # <-- Uses v1 namespace
from enum import Enum


class BirthDayValidation(BaseModel):
    birthday_text: str = Field(description="The birthday of the user in text format")
    extraction_error: Optional[str] = Field(
        description="Message to display if the birthday could not be extracted"
    )


birth_day_parser = PydanticOutputParser(pydantic_object=BirthDayValidation)


class Decision(str, Enum):
    # finish_message_handling = "finish_message_handling"
    update_birth_day = "update_birthday"
    send_daily_forecast = "send_daily_forecast"
    subscribe = "subscribe"
    unsubscribe = "unsubscribe"
    unclear_user_input = "unclear_user_input"


class MenuDecision(BaseModel):
    decision: Decision = Field(description="Decision for future action to take")
    decision_details: str = Field(
        description="Provide necessary context for future action"
    )

    def __str__(self) -> str:
        return f"Decision: {self.decision}, Details: {self.decision_details}"


class HandledDecision(MenuDecision):
    def __init__(self, menu_decision: MenuDecision, action_result: str) -> None:
        super().__init__(
            decision=menu_decision.decision,
            decision_details=menu_decision.decision_details,
        )

        self.action_result = action_result

    def __str__(self) -> str:
        return f"{super().__str__()}, Action Result: {self.action_result}"


menu_decision_parser = PydanticOutputParser(pydantic_object=MenuDecision)
