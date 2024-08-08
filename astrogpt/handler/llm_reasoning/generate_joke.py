from typing import List
from ...logger.logger import logger
from astrogpt.llm.chains import joke_chain
from astrogpt.bot_utils.reply_chat import ReplyChat
from sqlalchemy.orm import Session
from astrogpt.bot_utils.language import get_language
from astrogpt.handler.llm_reasoning.action_result import ActionResult
from astrogpt.db_utils.add_joke import add_joke
from astrogpt.db_utils.get_jokes import get_jokes
from astrogpt.handler.llm_reasoning.format_list import format_list


async def generate_joke(
    chat: ReplyChat,
    session: Session,
) -> List[ActionResult]:
    try:
        user_name = chat.get_user_name()
        user_input = chat.get_message_text()
        user_language = get_language(chat)

        joke_example = get_jokes(session, count=3)
        joke_examples_str = format_list(joke_example)

        joke = joke_chain.invoke(
            {
                "user_name": user_name,
                "joke_examples": joke_examples_str,
                "user_language": user_language,
                "user_input": user_input,
            }
        )
        add_joke(session=session, joke=joke)

        return [ActionResult(action="Joke Generated", result=joke)]
    except Exception as e:
        return [
            ActionResult(
                action="Joke Generation Error", result="Failed due to " + str(e)
            )
        ]
