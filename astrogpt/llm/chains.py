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
    command_explanation_prompt,
    unexpected_input_reply_prompt,
    menu_prompt,
    reply_user_prompt,
    parse_user_language_prompt,
)
from .parsers import birth_day_parser, menu_decision_parser, user_language_parser
from astrogpt.llm.prompt import prompt, textGenModel, reasoningModel


welcome_chain = prompt(textGenModel, welcome_prompt) | StrOutputParser()

welcome_again_chain = prompt(textGenModel, welcome_again_prompt) | StrOutputParser()

command_explanation_chain = (
    prompt(textGenModel, command_explanation_prompt) | StrOutputParser()
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

parse_user_language_chain = (
    prompt(
        reasoningModel,
        parse_user_language_prompt,
        partial_variables={
            "format_instructions": user_language_parser.get_format_instructions()
        },
    )
    | user_language_parser
)

menu_chain = (
    prompt(
        reasoningModel,
        menu_prompt,
        partial_variables={
            "format_instructions": menu_decision_parser.get_format_instructions()
        },
    )
    | menu_decision_parser
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

unexpected_input_reply_chain = (
    prompt(textGenModel, unexpected_input_reply_prompt) | StrOutputParser()
)

reply_user_input_chain = prompt(textGenModel, reply_user_prompt) | StrOutputParser()
