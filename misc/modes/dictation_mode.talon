mode: dictation
experiment: anchor-file
-

# Freely dictate text
<user.prose>:               "{prose}"

# Insert the actual words
# Only words, no symbols or numbers
escape <user.words>$:       "{words}"
escape <user.words> over:   "{words}"

bullet:                     "* "
task:                       "- [ ] "

new line:
    edit.line_insert_down()
    user.dictation_format_reset()

new block:
    edit.line_insert_down()
    edit.line_insert_down()
    user.dictation_format_reset()

# Switch to command mode and insert a phrase
(command mode | over) [<phrase>]$:
    user.command_mode(phrase or "")
