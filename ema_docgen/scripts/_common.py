"""Shared text handling for the ema_docgen scripts.

The .qmd sources are hard-wrapped, so anything that matches prose must match on
whitespace-normalised text and map positions back to the original. Everything
here exists to make that safe.
"""

from __future__ import annotations

import re
from typing import Iterator

FENCE_RE = re.compile(r"^\s*```", re.MULTILINE)
PARA_BREAK_RE = re.compile(r"\n[ \t]*\n")


def normalize_with_map(text: str) -> tuple[str, list[int]]:
    """Collapse whitespace runs to single spaces.

    Returns (normalised_text, index_map) where index_map[i] is the offset in
    `text` of the character that produced normalised_text[i].
    """
    out: list[str] = []
    idx: list[int] = []
    prev_space = True
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_space:
                out.append(" ")
                idx.append(i)
                prev_space = True
        else:
            out.append(ch)
            idx.append(i)
            prev_space = False
    # trailing space carries no anchor value
    if out and out[-1] == " ":
        out.pop()
        idx.pop()
    return "".join(out), idx


def normalize(text: str) -> str:
    return " ".join(text.split())


def fenced_regions(text: str) -> list[tuple[int, int]]:
    """Character ranges covered by ``` fenced blocks, inclusive of the fences."""
    marks = [m.start() for m in FENCE_RE.finditer(text)]
    regions: list[tuple[int, int]] = []
    for i in range(0, len(marks) - 1, 2):
        start = marks[i]
        end_line_end = text.find("\n", marks[i + 1])
        end = len(text) if end_line_end == -1 else end_line_end + 1
        regions.append((start, end))
    if len(marks) % 2 == 1:  # unterminated fence — treat rest of file as code
        regions.append((marks[-1], len(text)))
    return regions


def front_matter_region(text: str) -> tuple[int, int] | None:
    """YAML front matter delimited by leading --- ... --- lines."""
    if not text.startswith("---"):
        return None
    m = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    if not m:
        return None
    return (0, 3 + m.end())


def in_regions(pos: int, regions: list[tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in regions)


def blank_out(text: str, regions: list[tuple[int, int]]) -> str:
    """Replace regions with spaces, preserving length and newlines.

    Newlines are kept so line numbers survive.
    """
    chars = list(text)
    for start, end in regions:
        for i in range(max(0, start), min(len(chars), end)):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def prose_only(text: str) -> str:
    """Blank out front matter and fenced code, leaving prose in place."""
    regions = fenced_regions(text)
    fm = front_matter_region(text)
    if fm:
        regions = [fm] + regions
    return blank_out(text, regions)


def find_all(haystack: str, needle: str) -> Iterator[int]:
    start = 0
    while True:
        pos = haystack.find(needle, start)
        if pos == -1:
            return
        yield pos
        start = pos + 1


def locate_anchor(text: str, anchor: str) -> list[tuple[int, int]]:
    """Whitespace-insensitive search. Returns original-text (start, end) spans."""
    norm_text, idx = normalize_with_map(text)
    norm_anchor = normalize(anchor)
    if not norm_anchor:
        return []
    spans: list[tuple[int, int]] = []
    for pos in find_all(norm_text, norm_anchor):
        start = idx[pos]
        end = idx[pos + len(norm_anchor) - 1] + 1
        spans.append((start, end))
    return spans


def paragraph_end(text: str, pos: int) -> int:
    """Offset at which to insert a following paragraph."""
    m = PARA_BREAK_RE.search(text, pos)
    return m.start() if m else len(text)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1
