from typing import List
from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.list("delimiters_spaced", desc="List of delimiters with trailing white space")
ctx.lists["self.delimiters_spaced"] = {
    "spam":     ",",
    "colgap":   ":",
    "period":   "."
}

mod.list("delimiter_pair", desc="List of matching pair delimiters")
matching_pairs = {
    "round":    ["(", ")"],
    "index":    ["[", "]"],
    "diamond":  ["<", ">"],
    "block":    ["{", "}"],
    "twin":     ["'", "'"],
    "quad":     ['"', '"']
}
matching_pairs["string"] = matching_pairs["quad"]
ctx.lists["self.delimiter_pair"] = matching_pairs.keys()


@mod.capture(rule="{user.delimiter_pair}")
def delimiter_pair(m) -> List[str]:
    return matching_pairs[m.delimiter_pair]


@mod.action_class
class Actions:
    def delimiters_pair_insert(pair: List[str]):
        """Insert matching pair delimiters"""
        actions.insert(pair[0] + pair[1])
        for _ in pair[1]:
            actions.edit.left()

    def delimiters_pair_wrap_selection(pair: List[str]):
        """Wrap selection with matching pair delimiters"""
        selection = actions.edit.selected_text()
        actions.insert(f"{pair[0]}{selection}{pair[1]}")
