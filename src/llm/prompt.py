from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSerializable
from langchain_core.messages import BaseMessage
from langchain_core.utils.utils import convert_to_secret_str


model = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    api_key=convert_to_secret_str(
        "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"
    ),
)


def prompt(
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
