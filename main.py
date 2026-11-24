"""vending-pickup-line: one pickup line from a vending machine.

The machine has spent its whole life dropping snacks for strangers
who never look at it twice. Tonight it finally speaks up, in its own
voice, using its own world -- coils, buttons, exact change, rows --
and the joke turns on the machine's one job: dropping things. The
punch lands on the last two words.

The program writes that single line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output) after enforcing the competition's gates: UTF-8
text, 1-200 characters, one line, not whitespace-only, no control
characters (tab and DEL count as control characters here). If any
gate fails, nothing is written and the program exits non-zero.
"""

import os
import sys

# The line: 118 characters, no trailing newline in the file.
LINE = (
    "I've spent years dropping snacks for strangers, but you're the "
    "first human I'd drop everything for. Press B4 -- I'm yours."
)

MAX_CHARS = 200


def checks(text):
    """Yield one message per gate the text violates; nothing = pass."""
    if not text.strip():
        yield "entry is blank or only whitespace"
    if len(text) > MAX_CHARS:
        yield "entry is %d characters, gate allows at most %d" % (
            len(text),
            MAX_CHARS,
        )
    if len(text) < 1:
        yield "entry is empty"
    if "\n" in text or "\r" in text:
        yield "entry must be a single line"
    for char in text:
        if ord(char) < 0x20 or ord(char) == 0x7F:
            yield "entry holds control character U+%04X" % ord(char)
            break
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        yield "entry is not valid UTF-8: %s" % exc


def main():
    problems = list(checks(LINE))
    if problems:
        for problem in problems:
            print("gate failed: %s" % problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # Read it back: the file on disk must be exactly the gated line.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != LINE:
        print("gate failed: entry.txt on disk differs from the line", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(LINE), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
