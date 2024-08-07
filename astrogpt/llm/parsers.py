from typing import Optional
from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field  # <-- Uses v1 namespace
from enum import Enum


class CollectDataParser(BaseModel):
    birthday_text: Optional[str] = Field(
        description="The birthday of the user in text format, birthday should be in free for format, but it should be reasonable date of birth"
    )

    language: Optional[str] = Field(
        description="Desired language option of the user. Do not consider language already available in user information. Convert it to single English word like in list of supported languages"
    )

    parsing_feedback: str = Field(
        description="Explanation of data extraction result with clarification of errors is needed"
    )


collect_data_parser = PydanticOutputParser(pydantic_object=CollectDataParser)


class Decision(str, Enum):
    update_user_data = "update_user_data"
    update_language = "update_language"
    subscribe = "subscribe"
    unsubscribe = "unsubscribe"
    request_input_clarification = "request_input_clarification"
    send_goal_achieved = "send_goal_achieved"
    user_input_is_irrelevant = "user_input_is_irrelevant"
    ask_for_missing_user_data = "ask_for_missing_user_data"
    provide_situational_advice = "provide_situational_advice"


class MenuDecision(BaseModel):
    decision: Decision = Field(description="Decision for future action to take")
    decision_details: str = Field(
        description="Provide necessary context for future action of the bot"
    )

    def __str__(self) -> str:
        return f"Action: {self.decision}, Details: {self.decision_details}"


menu_decision_parser = PydanticOutputParser(pydantic_object=MenuDecision)


class AdviceParser(BaseModel):
    astrological_advice: Optional[str] = Field(
        description="Description of astrological advice for the user"
    )

    situation: Optional[str] = Field(
        description="Description of the situation for which the advice is given"
    )

    clarification: Optional[str] = Field(
        description="Explanation of the advice with clarification of errors is needed"
    )


advice_parser = PydanticOutputParser(pydantic_object=AdviceParser)
