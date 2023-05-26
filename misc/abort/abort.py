from talon import Module, Context, actions
from talon.grammar import Phrase, Capture
from talon.grammar.vm import VMCapture
from talon.engines.w2l import DecodeWord
from dataclasses import dataclass
import time

mod = Module()

ctx_en = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""


@dataclass
class AbortPhrase:
    phrase: str
    start: float
    end: float


abort_phrases = ["cancel", "canceled", "avbryt"]

abort_phrase: AbortPhrase = None
ts_threshold: float = None


@mod.action_class
class Actions:
    def abort_current_phrase():
        """Abort current spoken phrase"""
        global ts_threshold
        ts_threshold = time.perf_counter()

    def abort_specific_phrase(phrase: str, start: float, end: float):
        """Abort the specified phrase"""
        global abort_phrase
        abort_phrase = AbortPhrase(phrase, start, end)

    def abort_phrase(phrase: Phrase) -> tuple[bool, str]:
        """Possibly abort current spoken phrase"""
        global ts_threshold, abort_phrase

        words = phrase["phrase"]
        current_phrase = " ".join(words)

        if abort_phrase is not None:
            if abort_phrase.phrase == current_phrase:
                start = getattr(words[0], "start", 0)
                end = getattr(words[-1], "end", 0)
                if start <= abort_phrase.start and end >= abort_phrase.end:
                    actions.user.debug(f"Aborted phrase. {current_phrase}")
                    abort_entire_phrase(phrase)
                    abort_phrase = None
                    return True, ""
            abort_phrase = None

        if ts_threshold is not None:
            delta = ts_threshold - phrase["_ts"]
            ts_threshold = None
            if delta > 0:
                actions.user.debug(f"Aborted phrase. {delta:.2f}s")
                abort_entire_phrase(phrase)
                return True, ""

        for abort_phrase in abort_phrases:
            if words[-1] == abort_phrase:
                # Update phrase since that is used by analyze phrase
                phrase["phrase"] = phrase["phrase"][-1:]

                # Updating the sequence is what actually aborts the command we don't want to do.
                # You could just set an empty list: phrase["parsed"]._sequence = []
                # Unfortunately that will not work with analyze phrase since our command history won't be updated.

                phrase["parsed"]._sequence = [
                    get_capture(phrase, abort_phrase),
                ]

                if len(words) > 1:
                    return True, f"... {abort_phrase}"
                return True, abort_phrase

        return False, current_phrase

    def abort_phrase_command():
        """Abort current spoken phrase"""
        return ""


def abort_entire_phrase(phrase: Phrase):
    phrase["phrase"] = []
    if "parsed" in phrase:
        phrase["parsed"]._sequence = []


def get_capture(phrase: Phrase, abort_phrase: str) -> Capture:
    # Last capture in sequence is actually cancel, just reused that one.
    capture = phrase["parsed"]._sequence[-1]
    if abort_phrase == str(capture):
        return capture

    # Last capture is not a cancel command. Probably a back anchored phrase.
    # eg: "sentence foo bar cancel"
    # To get around this is to actually construct the cancel capture.

    name = "__cancel_ra__"
    sequence = [DecodeWord(abort_phrase)]
    vmc = VMCapture(name=name, data=sequence)
    return Capture(vm_capture=vmc, sequence=sequence, mapping={})
