from src.start_bot import start_bot

from src.llm.chains import translate_system_error_chain
from src.bot_utils.language import languages, error_messages
from json import load, dumps


def main() -> None:
    start_bot("7189953918:AAEHKCoCuYW62FLZPt2lC1VqE_h0MaBKCaQ")
    # print(translate_system_error_chain.invoke({"language": "Russian"}))

    # inverted_languages = {v: k for k, v in languages.items()}

    # subs_file = open("error_file.json", "w")
    # unsub_file = open("unsubscriptions.json", "w")

    # new_subs = {}
    # new_unsubs = {}

    # for lang, code in inverted_languages.items():
    #     new_subs[code] = error_messages[lang]

    # subs_file.write(dumps(new_subs))
    # # unsub_file.write(dumps(new_unsubs))

    # subs_file.close()
    # unsub_file.close()


if __name__ == "__main__":
    main()
