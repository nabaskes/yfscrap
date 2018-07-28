def kill_parens(text: str):
    'removes all parentheses from a given string'
    return text.replace("(", "").replace(")", "")


def convert_text_multiplier(value: str) -> float:
    'turns a number formatted like 3.47b or 4.92m into a float value'
    if value[-1].lower() in ('m', 'b'):
        if value[-1].lower() == "m":
            multiplier = 1000000.0
        elif value[-1].lower() == "b":
            multiplier = 1000000000.0
        return float(value[:-1])*multiplier
    return float(value)
