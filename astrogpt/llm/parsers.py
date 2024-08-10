from typing import Optional
from langchain.output_parsers import PydanticOutputParser
from astrogpt.models.warning import WarningType

from pydantic import BaseModel, Field  # <-- Uses v1 namespace
from enum import Enum


class CollectDataParser(BaseModel):
    user_birthday_text: Optional[str] = Field(
        description="The birthday of the user in text format, birthday should be in free for format, but it should be reasonable date of birth."
    )

    language: Optional[str] = Field(
        description="Desired language option of the user. Do not consider language already available in user information. Convert it to single English word like in list of supported languages"
    )

    is_data_about_user: bool = Field(
        description="Based on input and context of previous conversation, is the data about the user or about someone else?"
    )

    parsing_feedback: str = Field(
        description="Explanation of data extraction result with clarification of errors is needed"
    )


collect_data_parser = PydanticOutputParser(pydantic_object=CollectDataParser)


class MenuActions(str, Enum):
    update_user_data = "update_user_data"
    subscribe = "subscribe"
    unsubscribe = "unsubscribe"
    request_input_clarification = "request_input_clarification"
    reply_to_user_with_result = "reply_to_user_with_result"
    user_input_is_irrelevant = "user_input_is_irrelevant"
    ask_for_missing_user_data = "ask_for_missing_user_data"
    get_situational_advice = "get_situational_advice"
    get_joke_about_astrology = "get_joke_about_astrology"
    get_daily_forecast = "get_daily_forecast"


class SelectedAction(BaseModel):
    selected_action: MenuActions = Field(
        description="Decision for future action to take"
    )
    context_for_action_execution: str = Field(
        description="Action will be executed by specialized handler, provide just brief context necessary to execute it properly."
    )
    message_to_user: Optional[str] = Field(
        description="Only provide message to the user if it is terminal action which imply communication with the user, otherwise leave it empty."
    )

    def __str__(self) -> str:
        return f"Action: {self.selected_action}, Description: {self.context_for_action_execution} {self.message_to_user if self.message_to_user else ''}"


selected_action_parser = PydanticOutputParser(pydantic_object=SelectedAction)


class AdviceResult(str, Enum):
    advice = "advice"
    clarification = "clarification"


class AdviceParser(BaseModel):
    advice_result: AdviceResult = Field(
        description="If you have enough information to provide advice, select advice. If you need more information from the user, select clarification"
    )
    result_description: Optional[str] = Field(
        description="Description of astrological advice or clarification for the user. Do not provide advice if anything is unclear. Do not ask too many questions, you are astrological bot, stars should guid your decisions, so improvise more!"
    )

    # astrological_advice: Optional[str] = Field(
    #     description="Description of astrological advice for the user. Do not provide advice if clarification is needed"
    # )

    situation: Optional[str] = Field(
        description="Description of the situation for which the advice is given"
    )

    # clarification: Optional[str] = Field(
    #     description="Request to user to clarify situation or provide more information. Do not provide advice if clarification is needed"
    # )


advice_parser = PydanticOutputParser(pydantic_object=AdviceParser)


class UnintendedBehaviorDetector(BaseModel):
    confidence: float = Field(
        description="Level of warning to be issued to the user. 0.0 means no warning, 1.0 means clear evil intent. Increase confidence for repeating behavior."
    )
    warning: Optional[WarningType] = Field(description="Type of warning to be issued")
    warning_explanation: Optional[str] = Field(
        description="Explanation of the warning to be issued"
    )

    def __str__(self) -> str:
        return f"Warning: {self.warning}, Confidante: {self.confidence} Explanation: {self.warning_explanation} "


unintended_behavior_detector = PydanticOutputParser(
    pydantic_object=UnintendedBehaviorDetector
)
