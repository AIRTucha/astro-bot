def replace_none_with_missing(text: str | None) -> str:
    return text if text is not None else "MISSING"
