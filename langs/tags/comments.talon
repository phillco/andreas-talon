tag: user.comments
-

make comment:         user.comments_insert()

make comment <user.text>$:
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    user.comments_insert(text)

make block comment:   user.comments_insert_block()

make block comment <user.text>$:
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    user.comments_insert_block(text)