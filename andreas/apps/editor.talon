# ----- Navigation -----
page up:                           edit.page_up()
page down:                         edit.page_down()

peak:                              edit.file_start()
bottom:                            edit.file_end()

head:                              edit.line_start()
tail:                              edit.line_end()
middle:                            user.line_middle()

up [<number_small>]:               user.up(number_small or 1)
down [<number_small>]:             user.down(number_small or 1)
left [<number_small>]:             user.left(number_small or 1)
right [<number_small>]:            user.right(number_small or 1)

lefter [<number_small>]:           user.word_left(number_small or 1)
righter [<number_small>]:          user.word_right(number_small or 1)

slap:                              edit.line_insert_down()
slapper:                           user.line_insert_down(2)

indent:                            edit.indent_more()
dedent:                            edit.indent_less()

# ----- Navigate to specified text/symbol: go right paren
{user.navigation_action} {user.navigation_direction} to <user.text_symbol>:
	user.navigation(navigation_action, navigation_direction or "right", text_symbol)

# ----- Selection -----
take all:                          edit.select_all()
take none:                         edit.select_none()
take line:                         edit.select_line()
take word:                         edit.select_word()

extend peak:                       edit.extend_file_start()
extend bottom:                     edit.extend_file_end()
extend head:                       edit.extend_line_start()
extend tail:                       edit.extend_line_end()

extend up [<number_small>]:        user.extend_up(number_small or 1)
extend down [<number_small>]:      user.extend_down(number_small or 1)
extend left [<number_small>]:      user.extend_left(number_small or 1)
extend right [<number_small>]:     user.extend_right(number_small or 1)

extend lefter [<number_small>]:    user.extend_word_left(number_small or 1)
extend righter [<number_small>]:   user.extend_word_right(number_small or 1)

# ----- Delete, undo, redo -----
(undo it | nope):                  edit.undo()
redo it:                           edit.redo()

del:                               edit.delete()
drill:                             user.delete_right()

remove:                            edit.delete_word()
wipe:                              user.delete_word_right()

chuck line:                        edit.delete_line()
chuck head:                        user.delete_line_start()
chuck tail:                        user.delete_line_end()
clear line:                        user.clear_line()

# ----- Cut, copy, paste -----
cut it:                            edit.cut()
cut word:                          user.cut_word()
cut line:                          user.cut_line()
cut head:                          user.cut_line_start()
cut tail:                          user.cut_line_end()

copy it:                           edit.copy()
copy word:                         user.copy_word()
copy line:                         user.copy_line()
copy head:                         user.copy_line_start()
copy tail:                         user.copy_line_end()

paste it:                          edit.paste()
(clone | dupe) line:               edit.line_clone()

drag up [<number_small>]:          user.line_swap_up(number_small or 1)
drag down [<number_small>]:        user.line_swap_down(number_small or 1)

# ----- Save -----
save:                              edit.save()

# ----- Find / Replace -----
find [<user.text>]:                edit.find(text or "")
find all [<user.text>]:            user.find_all(text or "")
find file [<user.text>]:           user.find_file(text or "")
find recent [<user.text>]:         user.find_file_recent(text or "")
find (previous | prev):            edit.find_previous()
find next:                         edit.find_next()
find replace [<user.text>]:        user.find_replace(text or "")
replace word:                      user.find_replace_word()
replace all:                       user.find_replace_all()

# ----- Brackets -----
args:
	"()"
	key(left)
index:
	"[]"
	key(left)
diamond:
	"<>"
	key(left)
block:
	"{}"
	key(left)

# ----- Quotes -----
twin:
	"''"
	key(left)
string:
	'""'
	key(left)

# ----- Misc -----
spamma:                            ", "
colgap:                            ": "
period:                            ". "
smiley face:                       ":)"

push {user.key_symbol}:
	edit.line_end()
	"{key_symbol}"
	edit.line_insert_down()

stop:                              user.stop_app()