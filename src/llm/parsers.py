from typing import Optional
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field


class BirthDayValidation(BaseModel):
    birthday_text: str = Field(description="The birthday of the user in text format")
    extraction_error: Optional[str] = Field(
        description="Message to display if the birthday could not be extracted"
    )


birth_day_parser = PydanticOutputParser(pydantic_object=BirthDayValidation)
