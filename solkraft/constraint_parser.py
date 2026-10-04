"""Shared parsing for explicit side-effect exclusions."""
from __future__ import annotations

import re


EFFECT_FORMS = {
    "merge": r"merg(?:e|ing|ed)?",
    "publish": r"publish(?:ing|ed|es)?",
    "deploy": r"deploy(?:ing|ed|s)?",
    "send": r"send|sending|sent",
    "purchase": r"purchas(?:e|ing|ed)",
    "fabricate": r"fabricat(?:e|ing|ed|ion)?",
    "delete": r"delet(?:e|ing|ed)",
    "revoke": r"revok(?:e|ing|ed)",
    "rotate": r"rotat(?:e|ing|ed)",
    "push": r"push(?:ing|ed|es)?",
}


def hide_quotes(text: str) -> tuple[str, list[str]]:
    quoted = []

    def replace(match):
        quoted.append(match.group(0))
        return " "

    visible = re.sub(
        r"\x60\x60\x60[\\s\\S]*?\x60\x60\x60|\x60[^\x60\\n]*\x60|\"[^\"\\n]*\"|'[^'\\n]*'",
        replace,
        text,
    )
    return visible, quoted


def effect_exclusion_start(text: str) -> int | None:
    """Return the first explicit effect exclusion in text."""
    matches = []
    for form in EFFECT_FORMS.values():
        match = re.search(
            rf"\\b(?:do not|don't|dont|without|never|skip|avoid)\\b[^.;\\n]{{0,70}}\\b(?:{form})\\b",
            text,
        )
        if match:
            matches.append(match.start())
    return min(matches) if matches else None


def excluded_effects(text: str) -> list[str]:
    """Return explicitly forbidden effects while keeping quotes inert."""
    lowered, _ = hide_quotes(text.casefold())
    context_start = re.search(r"\\bcontext notes\\s*:", lowered)
    if context_start:
        tail = lowered[context_start.start():]
        exclusion_start = effect_exclusion_start(tail)
        lowered = (
            lowered[:context_start.start()] + " " + tail[exclusion_start:]
            if exclusion_start is not None
            else lowered[:context_start.start()]
        )

    found = []
    for effect, form in EFFECT_FORMS.items():
        pattern = rf"\\b(?:do not|don't|dont|without|never|skip|avoid)\\b[^.;\\n]{{0,70}}\\b(?:{form})\\b"
        match = re.search(pattern, lowered)
        if match:
            found.append((match.start(), effect))
    return [effect for _, effect in sorted(found)]
