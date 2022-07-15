from talon import Context, Module

mod = Module()
ctx = Context()


# Default words that will need to be capitalized.
capitalize_defaults = [
    # NB. the lexicon now capitalizes January/February by default, but not the
    # others below. Not sure why.
    "January",
    "February",
    # March omitted because it's a regular word too
    "April",
    # May omitted because it's a regular word too
    "June",
    "July",
    "August",  # technically also an adjective but the month is far more common
    "September",
    "October",
    "November",
    "December",
]

# Default words that need to be remapped.
word_map_defaults = {
    "organization": "organisation",
    "organizations": "organisations",
    "dis": "this",
    "classname": "class name",
}
word_map_defaults.update({word.lower(): word for word in capitalize_defaults})

# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
ctx.settings["dictate.word_map"] = word_map_defaults

# Default words that should be added to Talon's vocabulary.
simple_default_vocabulary = [
    "admin",
    "vpn",
    "dns",
    "exe",
    "linux",
    "array",
    "html",
    "url",
    "vscode",
    "json",
    "api",
    "http",
    "css",
    "cursorless",
    "cheat sheet",
    "user",
    "backup",
    "andreas",
    "arvidsson",
    "rsi",
    "pokey",
    "aegis",
    "vimium",
    "karlstad",
    "yeah",
    "usb",
    "highcharts",
    "csv",
    "chuck",
    "any",
    "tree sitter",
    "num",
    "quarkus",
    "keycloak",
    "util",
    "rango",
    "talon",
    "pause",
]
# Defaults for different pronounciations of words that need to be added to Talon's vocabulary.
default_vocabulary = {
    "knaus": "knausj",
    "toby": "tobii",
    "curse less": "cursorless",
    "visual code": "vscode",
    "arvid son": "arvidsson",
}
default_vocabulary.update({word.lower(): word for word in simple_default_vocabulary})

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
mod.list("vocabulary", desc="additional vocabulary words")
ctx.lists["user.vocabulary"] = default_vocabulary
