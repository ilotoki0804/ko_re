from __future__ import annotations

import functools
import re as _re
from re import Match, Pattern, RegexFlag, escape
from typing import Callable, Literal

from ._core import compilestr

# fmt: off
__all__ = [
    "match", "fullmatch", "search", "sub", "subn", "split",
    "findall", "finditer", "compile", "escape",
    "Pattern", "Match", "A", "I", "L", "M", "S", "X", "U",
    "ASCII", "IGNORECASE", "LOCALE", "MULTILINE", "DOTALL", "VERBOSE",
    "UNICODE", "NOFLAG", "RegexFlag",
]
# fmt: on


NOFLAG = 0
ASCII = A = _re.ASCII
IGNORECASE = I = _re.IGNORECASE  # noqa: E741
LOCALE = L = _re.LOCALE
UNICODE = U = _re.UNICODE
MULTILINE = M = _re.MULTILINE
DOTALL = S = _re.DOTALL
VERBOSE = X = _re.VERBOSE

OrderType = Literal["default", "regular_first"] | None


# --------------------------------------------------------------------
# public interface


def match(pattern: str, string: str, flags: int | RegexFlag = 0, order: OrderType = None):
    """Try to apply the pattern at the start of the string, returning
    a Match object, or None if no match was found."""
    return _compile(pattern, flags, order).match(string)


def fullmatch(pattern: str, string: str, flags: int | RegexFlag = 0, order: OrderType = None):
    """Try to apply the pattern to all of the string, returning
    a Match object, or None if no match was found."""
    return _compile(pattern, flags, order).fullmatch(string)


def search(pattern: str, string: str, flags: int | RegexFlag = 0, order: OrderType = None):
    """Scan through string looking for a match to the pattern, returning
    a Match object, or None if no match was found."""
    return _compile(pattern, flags, order).search(string)


def sub(
    pattern: str, repl: str | Callable[[Match[str]], str], string: str, count: int = 0, flags: int | RegexFlag = 0, order: OrderType = None
):
    """Return the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in string by the
    replacement repl.  repl can be either a string or a callable;
    if a string, backslash escapes in it are processed.  If it is
    a callable, it's passed the Match object and must return
    a replacement string to be used."""
    return _compile(pattern, flags, order).sub(repl, string, count)


def subn(
    pattern: str, repl: str | Callable[[Match[str]], str], string: str, count: int = 0, flags: int | RegexFlag = 0, order: OrderType = None
):
    """Return a 2-tuple containing (new_string, number).
    new_string is the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in the source
    string by the replacement repl.  number is the number of
    substitutions that were made. repl can be either a string or a
    callable; if a string, backslash escapes in it are processed.
    If it is a callable, it's passed the Match object and must
    return a replacement string to be used."""
    return _compile(pattern, flags, order).subn(repl, string, count)


def split(pattern: str, string: str, maxsplit: int = 0, flags: int | RegexFlag = 0, order: OrderType = None):
    """Split the source string by the occurrences of the pattern,
    returning a list containing the resulting substrings.  If
    capturing parentheses are used in pattern, then the text of all
    groups in the pattern are also returned as part of the resulting
    list.  If maxsplit is nonzero, at most maxsplit splits occur,
    and the remainder of the string is returned as the final element
    of the list."""
    return _compile(pattern, flags, order).split(string, maxsplit)


def findall(pattern: str, string: str, flags: int | RegexFlag = 0, order: OrderType = None):
    """Return a list of all non-overlapping matches in the string.

    If one or more capturing groups are present in the pattern, return
    a list of groups; this will be a list of tuples if the pattern
    has more than one group.

    Empty matches are included in the result."""
    return _compile(pattern, flags, order).findall(string)


def finditer(pattern: str, string: str, flags: int | RegexFlag = 0, order: OrderType = None):
    """Return an iterator over all non-overlapping matches in the
    string.  For each match, the iterator returns a Match object.

    Empty matches are included in the result."""
    return _compile(pattern, flags, order).finditer(string)


def compile(pattern: str, flags: int | RegexFlag = 0, order: OrderType = None):
    "Compile a regular expression pattern, returning a Pattern object."
    return _compile(pattern, flags, order)


@functools.cache  # Simple caching. You should use `compile` if you want performance.
def _compile(pattern: str, flags: int | RegexFlag = 0, order: OrderType = None):
    return _re.compile(compilestr(pattern, order), flags)
