from typing import Dict, Any, Optional
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(
    model="gpt-4", api_key="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"
)


def prompt(
    prompt_test: str,
    partial_variables: Optional[Dict[str, Any]] = None,
) -> ChatOpenAI:
    return (
        ChatPromptTemplate.from_template(
            prompt_test + "\n\n Please, answer in {user_language}.",
            partial_variables=partial_variables,
        )
        | model
    )
