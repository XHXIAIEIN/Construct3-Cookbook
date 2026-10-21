"""Check the guides: every relative link resolves, and the pitfalls index matches its topic files.

    python scripts/check.py

A link resolves when its file or folder exists beside the linking file and,
when it carries a #fragment, the target Markdown file has a heading with that
GitHub slug. The pitfalls index gives every group one conclusion line per
entry of the topic file it links, and every entry ends with its source.
Exits 1 and prints each problem when there is one.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent
PITFALLS = REPO / "guides" / "event-sheets" / "pitfalls"
INDEX = PITFALLS / "README.md"

FENCE = re.compile(r"^ {0,3}(```|~~~)")
CODE_SPAN = re.compile(r"(`+)(?:(?!\1).)+?\1")
# The target of an inline link or image, with an optional title after it
LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HTML_ANCHOR = re.compile(r"<a\s+(?:id|name)=\"([^\"]+)\"")
# The .md file a Markdown link points at, without its anchor
MD_LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
# A source is a bracketed span that is not a Markdown link's text.
SOURCE = re.compile(r"\[[^\]]+\](?!\()")


def prose_lines(text: str) -> list[str]:
    """The lines of a Markdown text outside fenced code blocks."""
    lines, fenced = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            lines.append(line)
    return lines


def slug(heading: str) -> str:
    """GitHub's anchor for a heading: its rendered text, lowercase, punctuation removed, spaces to hyphens."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    text = re.sub(r"<[^>]+>", "", text).replace("`", "").lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    """Every fragment a link can name in a Markdown file, numbering repeated headings as GitHub does."""
    found: set[str] = set()
    seen: dict[str, int] = {}
    for line in prose_lines(path.read_text(encoding="utf-8")):
        found.update(HTML_ANCHOR.findall(line))
        match = HEADING.match(line)
        if not match:
            continue
        base = slug(match.group(2))
        count = seen.get(base, 0)
        seen[base] = count + 1
        found.add(base if count == 0 else f"{base}-{count}")
    return found


def broken_links(path: Path) -> list[str]:
    problems = []
    for line in prose_lines(path.read_text(encoding="utf-8")):
        for link in LINK.findall(CODE_SPAN.sub("", line)):
            if SCHEME.match(link):
                continue
            target, _, fragment = link.partition("#")
            file = (path.parent / unquote(target)).resolve() if target else path
            if not file.exists():
                problems.append(f"links {link}: the file is missing")
            elif fragment and file.suffix == ".md" and unquote(fragment).lower() not in anchors(file):
                problems.append(f"links {link}: {file.relative_to(REPO).as_posix()} has no heading #{fragment}")
    return problems


def bullets(text: str) -> list[str]:
    """Top-level list entries, each with its continuation lines."""
    entries: list[str] = []
    for line in text.splitlines():
        if line.startswith("- "):
            entries.append(line)
        elif line.startswith("#"):
            entries.append("")
        elif entries and entries[-1]:
            entries[-1] += "\n" + line
    return [entry for entry in entries if entry]


def pitfall_problems() -> list[str]:
    text = INDEX.read_text(encoding="utf-8")
    problems, linked = [], set()
    topics = text.split("\n## Topics\n", 1)[1].split("\n## ", 1)[0]
    for block in topics.split("\n### ")[1:]:
        title, body = block.split("\n", 1)
        links = [link for link in MD_LINK.findall(body) if "/" not in link]
        if len(links) != 1:
            problems.append(f"group {title!r} links {links}, not one topic file")
            continue
        linked.add(links[0])
        topic = PITFALLS / links[0]
        if topic.exists():
            lines, entries = len(bullets(body)), len(bullets(topic.read_text(encoding="utf-8")))
            if lines != entries:
                problems.append(f"group {title!r}: {lines} conclusion lines in the index, {entries} entries in {links[0]}")
    on_disk = {p.name for p in PITFALLS.glob("*.md") if p != INDEX}
    problems += [f"the index links {name}, which does not exist" for name in sorted(linked - on_disk)]
    problems += [f"the index does not link {name}" for name in sorted(on_disk - linked)]
    files = {"README.md": text.split("\n## Topics\n", 1)[0]}
    files.update({p.name: p.read_text(encoding="utf-8") for p in PITFALLS.glob("*.md") if p != INDEX})
    for name, body in files.items():
        problems += [f"{name}: no source in {entry.splitlines()[0]!r}" for entry in bullets(body)
                     if not SOURCE.search(entry)]
    return [f"pitfalls/{p}" for p in problems]


def main() -> int:
    documents = sorted(p for p in REPO.rglob("*.md") if ".git" not in p.parts)
    problems = [f"{path.relative_to(REPO).as_posix()} {p}" for path in documents for p in broken_links(path)]
    problems += pitfall_problems()
    print("\n".join(problems) or f"{len(documents)} documents checked, no problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
