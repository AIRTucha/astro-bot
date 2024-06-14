from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSerializable
from langchain_core.messages import BaseMessage
from langchain_core.utils.utils import convert_to_secret_str
import os

open_ai_key = os.getenv("OPEN_AI_KEY")

if open_ai_key is None:
    raise ValueError("OPEN_AI_KEY is not set")

textGenModel = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    api_key=convert_to_secret_str(open_ai_key),
)

reasoningModel = ChatOpenAI(
    model="gpt-4o",
    api_key=convert_to_secret_str(open_ai_key),
)


def prompt(
    model: ChatOpenAI,
    prompt_test: str,
    partial_variables: Optional[Dict[str, Any]] = None,
) -> RunnableSerializable[dict[str, str], BaseMessage | Any]:
    return (
        ChatPromptTemplate.from_template(
            prompt_test + "\n\n Please, answer in {user_language}.",
            partial_variables=partial_variables,
        )
        | model
    )
