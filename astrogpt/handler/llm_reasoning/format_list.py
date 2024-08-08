from typing import List


def format_list(list: List[object]) -> str:
    return "\n\n".join([str(item) for item in list])
