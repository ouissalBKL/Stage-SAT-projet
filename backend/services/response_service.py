# services/response_service.py
import re


def clean_response(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"<\|header_start\|>", "", text)
    text = re.sub(r"<\|header_end\|>", "", text)
    text = re.sub(r"<\|.*?\|>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
