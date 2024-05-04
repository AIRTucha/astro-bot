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
)
from .parsers import birth_day_parser
from src.llm.prompt import prompt, model


welcome_chain = prompt(welcome_prompt) | StrOutputParser()

welcome_again_chain = prompt(welcome_again_prompt) | StrOutputParser()

daily_forecast_subscribe_inquiry_chain = (
    prompt(daily_forecast_subscribe_inquiry_prompt) | StrOutputParser()
)

daily_forecast_unsubscribe_inquiry_chain = (
    prompt(daily_forecast_unsubscribe_inquiry_prompt) | StrOutputParser()
)

parse_birthday_chain = (
    prompt(
        parse_date_of_birth_prompt,
        partial_variables={
            "format_instructions": birth_day_parser.get_format_instructions()
        },
    )
    | birth_day_parser
)


prediction_chain = prompt(prediction_prompt) | StrOutputParser()

cancel_chain = prompt(cancel_prompt) | StrOutputParser()

translate_system_error_chain = (
    ChatPromptTemplate.from_template(
        translate_system_error_prompt,
    )
    | model
    | StrOutputParser()
)

subscribed_chain = prompt(subscribed_prompt) | StrOutputParser()

unsubscribed_chain = prompt(unsubscribed_prompt) | StrOutputParser()

daily_forecast_subscribe_inquiry_chain = (
    prompt(daily_forecast_subscribe_inquiry_prompt) | StrOutputParser()
)

daily_forecast_unsubscribe_inquiry_chain = (
    prompt(daily_forecast_unsubscribe_inquiry_prompt) | StrOutputParser()
)
