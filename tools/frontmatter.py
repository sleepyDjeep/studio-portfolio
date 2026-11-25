#!/usr/bin/env python3
"""
Fence-aware YAML frontmatter splitting, shared by the builder and the verifier.

Both tools used to split a document on the first two '---' substrings. That is
almost always right, and quietly wrong the rest of the time: a quoted value that
contains '---' ends the frontmatter early, and the entry then compiles with no
title and a body that starts mid-YAML. Splitting on whole fence lines instead
means a bad document raises a named error rather than producing a plausible,
half-empty entry.
"""

import yaml


class FrontmatterError(ValueError):
    """A document's frontmatter cannot be read; the message names the file."""


def split_document(text: str, label: str) -> tuple[dict, str]:
    """Return (metadata, body) for a Markdown document, or raise FrontmatterError."""
    lines = text.replace("\r\n", "\n").split("\n")

    if not lines or lines[0].strip() != "---":
        raise FrontmatterError(f"{label}: missing opening '---' frontmatter fence")

    closing = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if closing is None:
        raise FrontmatterError(f"{label}: never closed the frontmatter fence")

    block = "\n".join(lines[1:closing])
    try:
        meta = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        first_line = str(exc).splitlines()[0] if str(exc) else exc.__class__.__name__
        raise FrontmatterError(f"{label}: frontmatter is not valid YAML ({first_line})") from exc

    if meta is None:
        raise FrontmatterError(f"{label}: frontmatter is empty")
    if not isinstance(meta, dict):
        raise FrontmatterError(
            f"{label}: frontmatter must be a mapping, got {type(meta).__name__}"
        )

    return meta, "\n".join(lines[closing + 1:])
