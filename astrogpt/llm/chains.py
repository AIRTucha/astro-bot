from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate
from astrogpt.llm.prompt.advice_prompt import advice_prompt
from astrogpt.llm.prompt.collect_data_prompt import collect_data_prompt
from astrogpt.llm.prompt.joke_prompt import joke_prompt
from astrogpt.llm.prompt.menu_prompt import menu_prompt
from astrogpt.llm.prompt.prediction_prompt import prediction_prompt
from astrogpt.llm.prompt.reply_user_prompt import reply_user_prompt
from astrogpt.llm.prompt.unintended_behavior_detection_prompt import (
    unintended_behavior_detection_prompt,
)
from astrogpt.llm.prompt.welcome_prompt import welcome_prompt

from .parsers import (
    collect_data_parser,
    selected_action_parser,
    advice_parser,
    unintended_behavior_detector,
)
from astrogpt.llm.llm_models import prompt, textGenModel, reasoningModel


welcome_chain = prompt(textGenModel, welcome_prompt) | StrOutputParser()

menu_chain = (
    prompt(
        reasoningModel,
        menu_prompt,
        partial_variables={
            "format_instructions": selected_action_parser.get_format_instructions()
        },
    )
    | selected_action_parser
)

prediction_chain = prompt(textGenModel, prediction_prompt) | StrOutputParser()

reply_user_input_chain = prompt(textGenModel, reply_user_prompt) | StrOutputParser()

collect_user_data_chain = (
    prompt(
        reasoningModel,
        collect_data_prompt,
        partial_variables={
            "format_instructions": collect_data_parser.get_format_instructions()
        },
    )
    | collect_data_parser
)

advice_chain = (
    prompt(
        reasoningModel,
        advice_prompt,
        partial_variables={
            "format_instructions": advice_parser.get_format_instructions()
        },
    )
    | advice_parser
)

unintended_behavior_detection_chain = (
    ChatPromptTemplate.from_template(
        unintended_behavior_detection_prompt,
        partial_variables={
            "format_instructions": unintended_behavior_detector.get_format_instructions()
        },
    )
    | reasoningModel
    | unintended_behavior_detector
)

joke_chain = prompt(textGenModel, joke_prompt) | StrOutputParser()
