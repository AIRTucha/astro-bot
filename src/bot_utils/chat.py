from abc import ABC, abstractmethod


class Chat(ABC):
    @abstractmethod
    def get_user_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_language_code(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_user_id(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def send_text(self, text: str, *button_texts: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_message_text(self) -> str:
        raise NotImplementedError
