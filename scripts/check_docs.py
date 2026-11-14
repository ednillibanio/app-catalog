"""Check language pairs, relative links and anchors of the catalog's Markdown files.

Run from the repository root: python3 scripts/check_docs.py
Exit status 0 when no problem is found, 1 otherwise. See docs/operations/operator-guide.md.
"""

import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote
from pathlib import Path

READER_ROOT_FILES = ("README.md", "CONTRIBUTING.md", "catalog/README.md")
PT = ".pt-BR.md"


def list_markdown():
    out = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        capture_output=True, check=True,
    ).stdout
    return sorted({p for p in out.decode().split("\0") if p})


def body(path):
    """Lines outside fenced code blocks (backtick or tilde fences of any length)."""
    lines, fence = [], None
    for line in Path(path).read_text().splitlines():
        m = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) \
                    and not line.strip().strip(fence[0]):
                fence = None
        elif m:
            fence = m.group(1)
        else:
            lines.append(line)
    return lines


def first_line(path):
    return (Path(path).read_text().splitlines() or [""])[0]


def heading_texts(path):
    return [m.group(1) for line in body(path) if (m := re.match(r" {0,3}#{1,6}\s+(.*?)\s*#*\s*$", line))]


def slug(text):
    text = re.sub(r"\[([^\]]*)\]\((?:[^()]|\([^()]*\))*\)", r"\1", text)  # links keep their text
    text = re.sub(r"[`*]", "", text)
    text = re.sub(r"(?<!\w)_+|_+(?!\w)", "", text)  # emphasis underscores; snake_case is kept
    text = unicodedata.normalize("NFC", text).lower()
    text = "".join(c for c in text if c.isalnum() or c in " -_")
    return text.replace(" ", "-")


def anchors(path):
    """GitHub heading anchors: a repeated slug gets the first free -1, -2, ... suffix."""
    out = set()
    for text in heading_texts(path):
        base, candidate, n = slug(text), slug(text), 0
        while candidate in out:
            n += 1
            candidate = f"{base}-{n}"
        out.add(candidate)
    return out


# Supported syntax: inline links with an optional title and one level of balanced parentheses
# in the destination, angle-bracket destinations, and reference definitions. Fenced code blocks and
# inline code (also across lines) are ignored. Indented code blocks and Setext headings
# (underlined with === or ---) are not recognized: use fenced blocks and # headings. Percent-encoded
# paths and anchors are decoded.
INLINE = re.compile(
    r"\]\(\s*(<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)")
REFDEF = re.compile(r"^ {0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)", re.M)


def links(path, skip_first_line=False):
    lines = body(path)
    if skip_first_line and lines:
        lines = lines[1:]
    text = re.sub(r"(`+).+?\1", "", "\n".join(lines), flags=re.S)
    found = INLINE.findall(text) + REFDEF.findall(text)
    return [t[1:-1] if t.startswith("<") else t for t in found]


def main():
    files = list_markdown()
    errors = []
    missing = [f for f in files if not Path(f).exists()]
    errors += [f"{f}: tracked but missing from the working tree" for f in missing]
    files = [f for f in files if Path(f).exists()]

    reader = [f for f in files if not f.endswith(PT)
              and (f in READER_ROOT_FILES or f.startswith("docs/"))]
    for en in reader:
        pt = en[:-3] + PT
        if not Path(pt).exists():
            errors.append(f"{en}: missing {pt}")
            continue
        if first_line(en) != f"English | [Português]({Path(pt).name})":
            errors.append(f"{en}: first line is not the language switch")
        if first_line(pt) != f"[English]({Path(en).name}) | Português":
            errors.append(f"{pt}: first line is not the language switch")
        if len(heading_texts(en)) != len(heading_texts(pt)):
            errors.append(f"{en}: {len(heading_texts(en))} headings, {pt}: {len(heading_texts(pt))}")
    for pt in [f for f in files if f.endswith(PT)]:
        if pt[: -len(PT)] + ".md" not in files:
            errors.append(f"{pt}: no English source")

    for src in files:
        # The first line of a translated pair is the language switch, validated above.
        is_pair = src.endswith(PT) or src[:-3] + PT in files
        for target in links(src, skip_first_line=is_pair):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            path, _, anchor = (unquote(part) for part in target.partition("#"))
            dest = (Path(src).parent / path).resolve() if path else Path(src).resolve()
            if not dest.exists():
                errors.append(f"{src}: broken link {target}")
                continue
            if anchor and dest.suffix == ".md" and anchor not in anchors(dest):
                errors.append(f"{src}: broken anchor {target}")
            translated = dest.with_name(dest.name[:-3] + PT)
            if (src.endswith(PT) and dest.suffix == ".md" and not dest.name.endswith(PT)
                    and translated.exists()):
                errors.append(f"{src}: links to English {target}; use the {PT} version")

    print("\n".join(errors) or f"OK: {len(reader)} language pairs, {len(files)} Markdown files")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
