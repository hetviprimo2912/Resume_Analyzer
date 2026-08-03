import re


EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

PHONE_PATTERN = re.compile(
    r"^\+?\d[\d\s\-\(\)]{7,}$"
)

URL_PATTERN = re.compile(
    r"^(https?://|www\.)"
)

SPACED_UPPERCASE_PATTERN = re.compile(
    r"^(?:[A-Z]\s)+[A-Z]$"
)


def is_email(text: str) -> bool:
    return EMAIL_PATTERN.match(text) is not None


def is_phone(text: str) -> bool:
    return PHONE_PATTERN.match(text) is not None


def is_url(text: str) -> bool:
    return URL_PATTERN.match(text) is not None


def is_spaced_uppercase(text: str) -> bool:
    """
    Example:
        S K I L L S
        P R O J E C T S
    """
    return SPACED_UPPERCASE_PATTERN.match(text.strip()) is not None