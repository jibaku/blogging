#-*- coding: utf-8 -*-


def tokenize(*args):
    """Return the tokens for the string passed as parameters."""
    raw_keywords = []
    for arg in args:
        raw_keywords += arg.split()
    cleaned_keywords = []
    for keyword in raw_keywords:
        keyword = keyword.strip("(")
        keyword = keyword.strip(")")
        keyword = keyword.strip(",")
        keyword = keyword.strip(".")
        cleaned_keywords.append(keyword)
