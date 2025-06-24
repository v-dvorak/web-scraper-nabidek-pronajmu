import re
from typing import Iterable


def flatten(xs):
    """https://stackoverflow.com/a/2158532
    """
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def find_number_in_str(text: str) -> int | None:
    """
    Matches digits separated by optional space, dot, or comma, with optional whitespace around the separator.
    The number must have at least four digits.

    Returns None if number is not present in text.
    """
    pattern = r"(\d{1,3}(?:\s*[.,\s]\s*\d{3})+|\d{4,})"
    match = re.search(pattern, text)
    if match:
        num_str = match.group(1)
        # Remove all separators to form a raw number string
        clean_str = re.sub(r"[.,\s]", "", num_str)
        return int(clean_str)
    return None

