from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate
from .prompts import (
    welcome_prompt,
    welcome_again_prompt,
    parse_date_of_birth_prompt,
    prediction_prompt,
    cancel_prompt,
    translate_system_error_prompt,
    subscribed_prompt,
    unsubscribed_prompt,
    daily_forecast_subscribe_inquiry_prompt,
    daily_forecast_unsubscribe_inquiry_prompt,
    unexpected_input_reply_prompt,
)
from .parsers import birth_day_parser
from src.llm.prompt import prompt, textGenModel, reasoningModel


welcome_chain = prompt(textGenModel, welcome_prompt) | StrOutputParser()

welcome_again_chain = prompt(textGenModel, welcome_again_prompt) | StrOutputParser()

daily_forecast_subscribe_inquiry_chain = (
    prompt(textGenModel, daily_forecast_subscribe_inquiry_prompt) | StrOutputParser()
)

daily_forecast_unsubscribe_inquiry_chain = (
    prompt(textGenModel, daily_forecast_unsubscribe_inquiry_prompt) | StrOutputParser()
)

parse_birthday_chain = (
    prompt(
        reasoningModel,
        parse_date_of_birth_prompt,
        partial_variables={
            "format_instructions": birth_day_parser.get_format_instructions()
        },
    )
    | birth_day_parser
)


prediction_chain = prompt(textGenModel, prediction_prompt) | StrOutputParser()

cancel_chain = prompt(textGenModel, cancel_prompt) | StrOutputParser()

translate_system_error_chain = (
    ChatPromptTemplate.from_template(
        translate_system_error_prompt,
    )
    | textGenModel
    | StrOutputParser()
)

subscribed_chain = prompt(textGenModel, subscribed_prompt) | StrOutputParser()

unsubscribed_chain = prompt(textGenModel, unsubscribed_prompt) | StrOutputParser()

daily_forecast_subscribe_inquiry_chain = (
    prompt(textGenModel, daily_forecast_subscribe_inquiry_prompt) | StrOutputParser()
)

daily_forecast_unsubscribe_inquiry_chain = (
    prompt(textGenModel, daily_forecast_unsubscribe_inquiry_prompt) | StrOutputParser()
)

unexpected_input_reply_chain = (
    prompt(textGenModel, unexpected_input_reply_prompt) | StrOutputParser()
)
