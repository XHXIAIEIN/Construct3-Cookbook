"""Check the guides: links, the pitfalls index against its pages, and the names of the pages.

    python scripts/check.py

A link resolves when its file or folder exists beside the linking file. If
the link carries a #fragment, the target Markdown file must also have a
heading with that GitHub slug. In the pitfalls index, guides/pitfalls.md,
every page has one group with one conclusion line per entry of the page,
and every entry ends with its source.

A page's path names what the page is about, and it comes from one of three
sources (AGENTS.md, "Naming"). plugins/, behaviors/ and effects/ take an id
of the Construct3-RAG clone's data/c3-schemas/_index.json. *-category/ takes
a category key of its data/c3-lang/en-US.json. primitives/ takes the path of
a page under the manual's project-primitives/ in the Construct3-Manual clone.
The check reads each clone beside this repository. If a clone is missing,
the check skips its part and prints the clone command. If the check finds a
problem, it prints each problem and exits with 1.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent
GUIDES = REPO / "guides"
INDEX = GUIDES / "pitfalls.md"
ADDONS = ("plugins", "behaviors", "effects")
CATEGORIES = ("behavior-category", "plugin-category", "effect-category")
PAGE_FOLDERS = (*ADDONS, *CATEGORIES, "primitives")
RAG = REPO.parent / "Construct3-RAG"
MANUAL = REPO.parent / "Construct3-Manual"
CLONE = {RAG: "https://github.com/XHXIAIEIN/Construct3-RAG", MANUAL: "https://github.com/XHXIAIEIN/Construct3-Manual"}

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


def pages() -> dict[str, Path]:
    """The pitfall pages by their path under guides/."""
    return {p.relative_to(GUIDES).as_posix(): p for folder in PAGE_FOLDERS for p in (GUIDES / folder).rglob("*.md")}


def index_problems() -> list[str]:
    text = INDEX.read_text(encoding="utf-8")
    problems, linked = [], set()
    topics = text.split("\n## Topics\n", 1)[1].split("\n## ", 1)[0]
    for block in topics.split("\n### ")[1:]:
        title, body = block.split("\n", 1)
        links = [link for link in MD_LINK.findall(body.split("\n- ", 1)[0]) if link.split("/")[0] in PAGE_FOLDERS]
        if len(links) != 1:
            problems.append(f"pitfalls.md: group {title!r} links {links}, not one page")
            continue
        linked.add(links[0])
        page = GUIDES / links[0]
        if page.exists():
            lines, entries = len(bullets(body)), len(bullets(page.read_text(encoding="utf-8")))
            if lines != entries:
                problems.append(f"pitfalls.md: group {title!r}: {lines} conclusion lines, {entries} entries in {links[0]}")
    on_disk = pages()
    problems += [f"pitfalls.md links {name}, which does not exist" for name in sorted(linked - set(on_disk))]
    problems += [f"pitfalls.md does not link {name}" for name in sorted(set(on_disk) - linked)]
    files = {"pitfalls.md": text.split("\n## Topics\n", 1)[0]}
    files.update({name: p.read_text(encoding="utf-8") for name, p in on_disk.items()})
    for name, body in files.items():
        problems += [f"{name}: no source in {entry.splitlines()[0]!r}" for entry in bullets(body)
                     if not SOURCE.search(entry)]
    return problems


def addons(path: Path) -> list[str]:
    """The ids of the `addons:` line between the `---` fences a page opens with; [] without one."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return []
    head = text[4:].split("\n---", 1)[0]
    line = next((l for l in head.splitlines() if l.startswith("addons:")), "addons:")
    return [x.strip().lower() for x in line[len("addons:"):].split(",") if x.strip()]


def name_problems() -> tuple[list[str], list[str]]:
    """The pages whose path is not an id, a category key or a manual page; and a note per missing clone."""
    problems, skipped = [], []
    names = pages()
    if (RAG / "data" / "c3-schemas" / "_index.json").is_file():
        index = json.loads((RAG / "data" / "c3-schemas" / "_index.json").read_text(encoding="utf-8"))
        model = json.loads((RAG / "data" / "c3-lang" / "en-US.json").read_text(encoding="utf-8-sig"))["text"]["model"]
        schemas = RAG / "data" / "c3-schemas" / "en-US"
        for name in names:
            kind, _, rest = name.partition("/")
            stem = rest[:-3]
            if kind in ADDONS and stem not in index[kind] and not (schemas / kind / f"{stem}.json").is_file():
                problems.append(f"{name}: {stem} is not a {kind[:-1]} id of Construct3-RAG")
            if kind in CATEGORIES and stem not in model[kind]:
                problems.append(f"{name}: {stem} is not a key of text.model.{kind} in c3-lang")
            # The addons: line names an addon id, or an addon's ACE as addon/ace-id
            for ref in addons(names[name]):
                addon, _, ace = ref.partition("/")
                schema = next((schemas / k / f"{addon}.json" for k in ("plugins", "behaviors")
                               if (schemas / k / f"{addon}.json").is_file()), None)
                if schema is None:
                    problems.append(f"{name}: addons: {addon} is not a plugin or behavior id of Construct3-RAG")
                elif ace and ace not in {e["id"] for part in ("conditions", "actions", "expressions")
                                         for e in json.loads(schema.read_text(encoding="utf-8")).get(part, [])}:
                    problems.append(f"{name}: addons: {ace} is not an ACE of {addon}")
    else:
        skipped.append(RAG)
    primitives = MANUAL / "Construct3-Manual" / "project-primitives"
    if primitives.is_dir():
        problems += [f"{name}: the manual has no project-primitives/{name.partition('/')[2]}"
                     for name in names if name.startswith("primitives/")
                     and not (primitives / name.partition("/")[2]).is_file()]
    else:
        skipped.append(MANUAL)
    return problems, [f'note: skipped the names that {c.name} holds; git clone --depth 1 {CLONE[c]} "{c.as_posix()}"'
                      for c in skipped]


def main() -> int:
    # Hidden folders hold no guides: .git, and the worktrees a session makes under .claude/
    documents = sorted(p for p in REPO.rglob("*.md") if not any(x.startswith(".") for x in p.relative_to(REPO).parts))
    problems = [f"{path.relative_to(REPO).as_posix()} {p}" for path in documents for p in broken_links(path)]
    problems += [f"guides/{p}" for p in index_problems()]
    named, notes = name_problems()
    problems += [f"guides/{p}" for p in named]
    print("\n".join(notes + problems) if notes or problems else "", end="\n" if notes or problems else "")
    if not problems:
        print(f"{len(documents)} documents checked, no problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
