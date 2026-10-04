"""Check a draft against the platform-safe and voice rules in CLAUDE.md.

Usage: python scripts/check_draft.py output/<slug>/draft.md
"""
import re
import sys
from pathlib import Path

HYPE_WORDS = ["revolutionary", "game-changer", "game changer", "in today's fast-paced world"]
CURLY_QUOTES = "\u201c\u201d\u2018\u2019"


def check(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    issues = []
    in_code = False
    seen_title = False

    for n, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Code fences
        if stripped.startswith("```"):
            if not in_code and stripped == "```":
                issues.append((n, "Code block has no language tag"))
            in_code = not in_code
            continue

        if in_code:
            if any(q in line for q in CURLY_QUOTES):
                issues.append((n, "Curly quote inside code block"))
            continue

        # Voice rules
        if "\u2014" in line:
            issues.append((n, "Em dash"))
        lower = line.lower()
        for word in HYPE_WORDS:
            if word in lower:
                issues.append((n, f'Hype word: "{word}"'))
        if re.search(r"\blet us\b(?! know)", lower):
            issues.append((n, 'Use "let\'s" instead of "let us"'))

        # Platform-safe formatting
        heading = re.match(r"^(#+)\s", line)
        if heading:
            level = len(heading.group(1))
            if level == 1 and not seen_title:
                seen_title = True
            elif level not in (2, 3):
                issues.append((n, f"H{level} heading (use H2 or H3 only)"))
        if re.match(r"^\s{2,}([-*+]|\d+\.)\s", line):
            issues.append((n, "Nested list"))
        if stripped.startswith("|"):
            issues.append((n, "Markdown table"))
        if re.search(r"!\[.*?\]\(.*?\)", line):
            issues.append((n, "Embedded image (list it in the publish kit instead)"))

    if in_code:
        issues.append((len(lines), "Code block never closed"))
    return issues


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_draft.py output/<slug>/draft.md")
        sys.exit(2)
    issues = check(sys.argv[1])
    if not issues:
        print("All checks passed")
        return
    for n, message in issues:
        print(f"Line {n}: {message}")
    print(f"\n{len(issues)} issue(s) found")
    sys.exit(1)


if __name__ == "__main__":
    main()