import re

HTML_TAGS = re.compile('<.*?>')


def clean_text(text: str) -> str:
    new_text = re.sub(HTML_TAGS, '', text)
    return new_text
