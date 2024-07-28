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
    update_birth_day = "update_birthday"
    subscribe = "subscribe"
    unsubscribe = "unsubscribe"
    request_input_clarification = "request_input_clarification"
    send_goal_achieved = "send_goal_achieved"


class MenuDecision(BaseModel):
    decision: Decision = Field(description="Decision for future action to take")
    decision_details: str = Field(
        description="Provide necessary context for future action of the bot"
    )

    def __str__(self) -> str:
        return f"Action: {self.decision}, Details: {self.decision_details}"


menu_decision_parser = PydanticOutputParser(pydantic_object=MenuDecision)
