def ascii_to_base32(text):
    mapping = { "!": "2", "?": "3", ",": "4", ".": "5", "-": "6", " ": "7" }
    formatted_text = text.upper()
    formatted_text = "".join(mapping.get(c, c) for c in formatted_text)
    return formatted_text