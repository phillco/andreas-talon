# Andreas Talon user scripts

All the scripts in my Talon user directory.

In constant development. Things will break!

## Interesting features

This is a list of features that I have implemented that I think is of more interest to other Talon users. Things I have already upstreamed to [knausj](https://github.com/knausj85/knausj_talon) are omitted. Since I don't actually use a fork of knausj some modifications (often different names) might be required.

1. **VSCode language definition for Talon** - Supports `on hover` and `go to definition` for Talon lists, captures and actions.
    - [registerLanguageDefinitions.ts](https://github.com/AndreasArvidsson/andreas-talon-vscode/blob/master/src/registerLanguageDefinitions.ts)
1. **Custom subtitles** - User customizable subtitles for Talon
    - [Subtitles and notifications](./core/on_phrase/subtitles_and_notifications)
1. **Command history** - Improved command history with description of commands
    - [Command history](./core/on_phrase/command_history)
1. **Analyze phrase** - Analyze a Talon phrase and retrieve metadata and description of commands
    - [Analyze phrase](./core/on_phrase/analyze_phrase)
1. **Mode indicator** - Graphical indicator to show you which Talon mode your currently are in
    - [Mode indicator](./plugins/mode_indicator)
1. **Talon Deck** - Stream deck inspired interactive dashboard for Talon Voice
    - [Talon Deck](https://github.com/AndreasArvidsson/talon-deck)
1. **Gamepad tester** - Builtin UI for visualizing interaction with Talon `gamepad()` api
    - [Gamepad tester](./plugins/gamepad_tester)
1. **Clipboard manager** - Clipboard manager built in Talon
    - [Clipboard manager](./plugins/clipboard_manager)
1. **Quick pick** - UI for quick access to useful features by clicking buttons
    - [Quick pick](./plugins/quick_pick)
1. **Foot switch support** - Add support for scrolling, navigating and more
    - [Foot switch](./core/foot_switch)
1. **RePhrase** - Reevaluate spoken phrase after Talon context change. Can for example be used to change to another application/window and execute commands to that window in the same utterance. `"focus firefox tab new"`
    - [window_management.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/f84a1aed3a11608eafcacd12ce37244a6cc07502/misc/window_management/window_management.talon#L1-L5)
    - [window_focus.py](https://github.com/AndreasArvidsson/andreas-talon/blob/f84a1aed3a11608eafcacd12ce37244a6cc07502/misc/window_management/window_focus.py#L111-L117)
    - [rephrase.py](https://github.com/AndreasArvidsson/andreas-talon/blob/master/misc/rephrase.py)
1. **<user.text> with abbreviations, spelling and numbers** - `"say foo forty four brief address air bat cap bar"` => `foo 44 addr abc bar`
    - [dictation.py](https://github.com/AndreasArvidsson/andreas-talon/blob/cbe580f5c6984afe31c76c3a3feb9229b1ede1d1/text/dictation.py#L44-L60)
1. **Smarter homophones** - Talon remembers recently used homophones and automatically replaces/reuses your chosen version
    - [dictation.py](https://github.com/AndreasArvidsson/andreas-talon/blob/b21c9eb553950ff9b3c137a98e8c705a3e8cb393/core/text/text_and_dictation.py#L127)
    - [homophones.py](https://github.com/AndreasArvidsson/andreas-talon/blob/b21c9eb553950ff9b3c137a98e8c705a3e8cb393/core/homophones/homophones.py#L99-L108)
1. **Lorem ipsum generator** - `"lorem ipsum thirty"` => `Lorem ipsum dolor sit amet...`
    - [Lorem ipsum](./plugins/lorem_ipsum)
1. **Snippet insertion** - Generic textual snippet support with override for VSCode
    - [javascript.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/langs/javascript/javascript.py#L139-L144)
    - [snippets.py](https://github.com/AndreasArvidsson/andreas-talon/blob/master/text/snippets.py)
1. **Imports fix** - Add missing and remove unused imports for VSCode
    - [vscode.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/cc2f5ecd5f696addd1d8df60207337e295fa800e/apps/vscode/vscode.talon#L32-L35)
    - [vscode.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.py#L391-L396)
1. **Copy command ID** - Copy command ID for the selected command in the VSCode command palette
    - [vscode.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.talon#L252)
    - [vscode.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.py#L382-L389)
1. **Wake Talon on double pop noise** - When Talon is in sleep mode a rapid double pop noise will wake Talon
    - [on_pop.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/on_pop.py)
    - [sleep.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/sleep/sleep.py#L23-L29)

## Dependencies

-   [Talon Voice](https://talonvoice.com) - The software that makes it all happen
-   [Cursorless](https://github.com/cursorless-dev/cursorless) - Don't even try to edit code without it
-   [Andreas VSCode Talon extension](https://github.com/AndreasArvidsson/vscode-talon-extension) - My own VSCode extension that adds multiple features for using VSCode with Talon
-   [Rango Talon](https://github.com/AndreasArvidsson/rango-talon) - Rango Talon side
-   [Rango extension](https://addons.mozilla.org/en-US/firefox/addon/rango) - Rango extension browser side
-   [Command client](https://github.com/AndreasArvidsson/talon-vscode-command-client) - Command RPC client Talon side
-   [Command server](https://marketplace.visualstudio.com/items?itemName=pokey.command-server) - Command RPC extension VSCode side
-   [nircmd](https://www.nirsoft.net/utils/nircmd.html) - Change playback device on windows
-   [clipboard-cli](https://www.npmjs.com/package/clipboard-cli) - CLI copy/paste
