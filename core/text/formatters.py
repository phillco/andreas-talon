from talon import Module, Context, actions
from typing import Callable
import re

mod = Module()
ctx = Context()


class Formatter:
    def __init__(
        self,
        id: str,
        format: Callable[[str], str],
        unformat: Callable[[str], str] = None,
    ):
        self.id = id
        self.format = format
        self.unformat = unformat


class CodeFormatter(Formatter):
    def __init__(
        self,
        id: str,
        delimiter: str,
        format_first: Callable[[str], str],
        format_rest: Callable[[str], str],
    ):
        self.id = id
        self._delimiter = delimiter
        self._format_first = format_first
        self._format_rest = format_rest

    def format(self, text: str) -> str:
        return self._format_delim(
            text, self._delimiter, self._format_first, self._format_rest
        )

    def unformat(self, text: str) -> str:
        return remove_code_formatting(text)

    def _format_delim(
        self,
        text: str,
        delimiter: str,
        format_first: Callable[[str], str],
        format_rest: Callable[[str], str],
    ):
        # Strip anything that is not alpha-num, whitespace or dot
        text = re.sub(r"[^\w\d\s.]+", "", text)
        # Split on anything that is not alpha-num
        words = re.split(r"([^\w\d]+)", text)
        groups = []
        group = []
        first = True

        for word in words:
            if word.isspace():
                continue
            # Word is number
            if word.isnumeric():
                first = True
            # Word is symbol
            elif not word.isalpha():
                groups.append(delimiter.join(group))
                word = word.strip()
                first = True
                groups.append(word)
                group = []
                continue
            elif first:
                first = False
                if format_first:
                    word = format_first(word)
            elif format_rest:
                word = format_rest(word)
            group.append(word)

        groups.append(delimiter.join(group))
        return "".join(groups)


class TitleFormatter(Formatter):
    _words_to_keep_lowercase = (
        "a an and as at but by en for if in nor of on or per the to v via vs".split()
    )

    def __init__(self, id: str):
        self.id = id

    def format(self, text: str) -> str:
        words = [x for x in re.split(r"(\s+)", text) if x]
        words = self._title_case_words(words)
        return "".join(words)

    def unformat(self, text: str) -> str:
        return unformat_upper(text)

    def _title_case_word(
        self, word: str, is_first: bool, is_last: bool, following_symbol: bool
    ) -> str:
        if not word.islower() or (
            word in self._words_to_keep_lowercase
            and not is_first
            and not is_last
            and not following_symbol
        ):
            return word

        if "-" in word:
            words = word.split("-")
            words = self._title_case_words(words)
            return "-".join(words)

        return word.capitalize()

    def _title_case_words(self, words: list[str]) -> list[str]:
        following_symbol = False
        for i, word in enumerate(words):
            if word.isspace():
                continue
            is_first = i == 0
            is_last = i == len(words) - 1
            words[i] = self._title_case_word(word, is_first, is_last, following_symbol)
            following_symbol = not word[-1].isalnum()
        return words


class CapitalizeFormatter(Formatter):
    def __init__(self, id: str):
        self.id = id

    def format(self, text: str) -> str:
        return re.sub(r"^\S+", lambda m: m.group().capitalize(), text)

    def unformat(self, text: str) -> str:
        return unformat_upper(text)


class SentenceFormatter(Formatter):
    def __init__(self, id: str):
        self.id = id

    def format(self, text: str) -> str:
        """Capitalize first word if it's already all lower case"""
        words = [x for x in re.split(r"(\s+)", text) if x]
        if words[0].islower():
            words[0] = words[0].capitalize()
        return "".join(words)

    def unformat(self, text: str) -> str:
        return unformat_upper(text)


def capitalize(text: str) -> str:
    return text.capitalize()


def lower(text: str) -> str:
    return text.lower()


def unformat_upper(text: str) -> str:
    return text.lower() if text.isupper() else text


def remove_code_formatting(text: str) -> str:
    """Remove format from text"""
    # Don't split delimited sequences in a string with whitespaces.
    # Could for example be: `short-term` or `iPhone` in a sentence
    if re.search(r"\s", text) is None:
        # Split on delimiters.
        result = re.sub(r"[-_.:/]+", " ", text)
        # Split camel case. Including numbers
        result = actions.user.de_camel(result)
        # Delimiter/camel case successfully split. Lower case to restore "original" text.
        if text != result:
            return result.lower()

    return text


formatters = [
    # Special formatters
    Formatter("TRAILING_SPACE", lambda text: f"{text} "),
    Formatter("DOUBLE_QUOTED_STRING", lambda text: f'"{text}"'),
    Formatter("SINGLE_QUOTED_STRING", lambda text: f"'{text}'"),
    # Prose formatters
    Formatter("KEEP_FORMAT", lambda text: text),
    Formatter("ALL_UPPERCASE", lambda text: text.upper()),
    Formatter("ALL_LOWERCASE", lambda text: text.lower()),
    TitleFormatter("TITLE_CASE"),
    SentenceFormatter("SENTENCE"),
    # Code formatters
    CodeFormatter("NO_SPACES", "", lower, lower),
    CodeFormatter("CAMEL_CASE", "", lower, capitalize),
    CodeFormatter("PASCAL_CASE", "", capitalize, capitalize),
    CodeFormatter("SNAKE_CASE", "_", lower, lower),
    CodeFormatter("DASH_SEPARATED", "-", lower, lower),
    CodeFormatter("DOT_SEPARATED", ".", lower, lower),
    CodeFormatter("SLASH_SEPARATED", "/", lower, lower),
    CodeFormatter("DOUBLE_UNDERSCORE", "__", lower, lower),
    CodeFormatter("DOUBLE_COLON_SEPARATED", "::", lower, lower),
    # Re-formatters
    CapitalizeFormatter("CAPITALIZE_FIRST_WORD"),
    Formatter("COMMA_SEPARATED", lambda text: re.sub(r"\s+", ", ", text)),
    Formatter("REMOVE_FORMATTING", lambda text: remove_code_formatting(text)),
]

formatters_dict = {f.id: f for f in formatters}

formatters_code = {
    "smash": "NO_SPACES",
    "camel": "CAMEL_CASE",
    "pascal": "PASCAL_CASE",
    "snake": "SNAKE_CASE",
    "constant": "ALL_UPPERCASE,SNAKE_CASE",
    "kebab": "DASH_SEPARATED",
    "dotted": "DOT_SEPARATED",
    "slasher": "SLASH_SEPARATED",
    # "dunder": "DOUBLE_UNDERSCORE",
    # "packed": "DOUBLE_COLON_SEPARATED",
}

formatters_prose = {
    "sentence": "SENTENCE",
    "sense": "SENTENCE",
    "title": "TITLE_CASE",
    "upper": "ALL_UPPERCASE",
    "lower": "ALL_LOWERCASE",
}


# This is the mapping from spoken phrases to formatters
mod.list("formatter_code", "List of code formatters")
ctx.lists["self.formatter_code"] = {
    **formatters_code,
    # I don't want these formatters in the formatter list/capture since they are not for reformatting
    "string": "DOUBLE_QUOTED_STRING",
    # "twin": "SINGLE_QUOTED_STRING",
}

mod.list("formatter_prose", "List of prose formatters")
ctx.lists["self.formatter_prose"] = {
    **formatters_prose,
    # I don't want these formatters in the formatter list/capture since they are not for reformatting
    "say": "KEEP_FORMAT",
}


mod.list("formatter", "List of formatters only used for reformatting")
ctx.lists["self.formatter"] = {
    **formatters_code,
    **formatters_prose,
    # These formatters are only for reformatting and neither code or prose
    "cap": "CAPITALIZE_FIRST_WORD",
    "list": "COMMA_SEPARATED",
    "un": "REMOVE_FORMATTING",
}

mod.list("formatter_word", "List of word formatters")
ctx.lists["self.formatter_word"] = {
    "word": "ALL_LOWERCASE",
    "trot": "TRAILING_SPACE,ALL_LOWERCASE",
    "proud": "CAPITALIZE_FIRST_WORD",
    "leap": "TRAILING_SPACE,CAPITALIZE_FIRST_WORD",
}


@mod.capture(rule="{self.formatter}+")
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m)


@mod.action_class
class Actions:
    def insert_formatted(text: str, formatters: str):
        """Insert text <text> formatted as <formatters>"""
        formatted = actions.user.format_text(text, formatters)
        actions.insert(formatted)

    def format_text(text: str, formatters: str) -> str:
        """Formats <text> as <formatters>"""
        return format_text(text, formatters, unformat=False)

    def reformat_text(text: str, formatters: str) -> str:
        """Re-formats <text> as <formatters>"""
        return format_text(text, formatters, unformat=True)

    def reformat_selection(formatters: str):
        """Reformats the current selection as <formatters>"""
        selected = actions.edit.selected_text()
        if selected:
            formatted = actions.user.reformat_text(selected, formatters)
            actions.insert(formatted)

    def de_camel(text: str) -> str:
        """Replacing camelCase boundaries with blank space"""
        Ll = "a-zåäö"
        Lu = "A-ZÅÄÖ"
        L = f"{Ll}{Lu}"
        low_to_upper = rf"(?<=[{Ll}])(?=[{Lu}])"  # camel|Case
        upper_to_last_upper = rf"(?<=[L{Lu}])(?=[{Lu}][{Ll}])"  # IP|Address
        letter_to_digit = rf"(?<=[{L}])(?=[\d])"  # version|10
        digit_to_letter = rf"(?<=[\d])(?=[{L}])"  # 2|x
        return re.sub(
            rf"{low_to_upper}|{upper_to_last_upper}|{letter_to_digit}|{digit_to_letter}",
            " ",
            text,
        )


def format_text(text: str, formatters: str, unformat: bool) -> str:
    """Formats a text according to formatters. formatters is a comma-separated string of formatters (e.g. 'TITLE_CASE,SNAKE_CASE')"""
    text, pre, post = shrink_to_string_inside(text)

    for i, formatter_name in enumerate(reversed(formatters.split(","))):
        formatter = formatters_dict[formatter_name]
        if unformat and i == 0 and formatter.unformat:
            text = formatter.unformat(text)
        text = formatter.format(text)

    return f"{pre}{text}{post}"


string_delimiters = [
    ['"""', '"""'],
    ['"', '"'],
    ["'", "'"],
]


def shrink_to_string_inside(text: str) -> (str, str, str):
    for [left, right] in string_delimiters:
        if text.startswith(left) and text.endswith(right):
            return text[len(left) : -len(right)], left, right
    return text, "", ""
