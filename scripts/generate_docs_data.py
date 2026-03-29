#!/usr/bin/env python3
"""
Parse AISVS chapter files into docs/data.json for the requirements visualizer.
Run from repo root: python3 scripts/generate_docs_data.py
"""

import json
import re
import sys
from pathlib import Path

CHAPTER_FILES = sorted(Path("1.0/en").glob("0x10-C[0-9][0-9]*.md"))

# Strip **bold** markers and "Verify that" prefix for compact display
def clean_desc(text):
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    return text.strip()

def parse_chapter(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    chapter_node = {"type": "chapter", "children": []}

    # Chapter title from first # heading
    for line in lines:
        m = re.match(r"^# (C\d+\s+.+)", line)
        if m:
            chapter_node["name"] = m.group(1).strip()
            break

    if "name" not in chapter_node:
        return None

    current_section = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # Section heading: ## C1.1 Section Title
        m = re.match(r"^## (C\d+\.\d+)\s+(.+)", line)
        if m:
            sec_id = m.group(1)
            sec_title = m.group(2).strip()
            # Next non-blank, non-table line is the section description
            desc = ""
            j = i + 1
            while j < len(lines):
                candidate = lines[j].strip()
                if candidate and not candidate.startswith("|") and not candidate.startswith("#") and not candidate.startswith(">") and not candidate.startswith("---"):
                    desc = candidate
                    break
                j += 1
            current_section = {
                "name": sec_id,
                "title": sec_title,
                "description": desc,
                "type": "section",
                "children": []
            }
            chapter_node["children"].append(current_section)
            i += 1
            continue

        # Control row: | **1.1.1** | ...description... | 1 |
        m = re.match(
            r"^\|\s*\*\*(\d+\.\d+\.\d+)\*\*\s*\|\s*(.+?)\s*\|\s*([123])\s*\|",
            line
        )
        if m and current_section is not None:
            ctrl_id = m.group(1)
            desc = clean_desc(m.group(2))
            level = int(m.group(3))
            current_section["children"].append({
                "name": ctrl_id,
                "type": f"control-l{level}",
                "level": level,
                "description": desc,
            })
            i += 1
            continue

        i += 1

    # Drop sections with no controls (e.g. "Control Objective")
    chapter_node["children"] = [s for s in chapter_node["children"] if s["children"]]
    return chapter_node


def main():
    root = {
        "name": "AISVS",
        "type": "root",
        "description": "AI Security Verification Standard — verifiable controls for AI-driven applications.",
        "children": []
    }

    for path in CHAPTER_FILES:
        chapter = parse_chapter(path)
        if chapter:
            root["children"].append(chapter)

    out = Path("docs/data.json")
    out.write_text(json.dumps(root, indent=2, ensure_ascii=False), encoding="utf-8")

    # Summary
    chapters = len(root["children"])
    sections = sum(len(c["children"]) for c in root["children"])
    controls = sum(
        len(s["children"])
        for c in root["children"]
        for s in c["children"]
    )
    print(f"Written {out}: {chapters} chapters, {sections} sections, {controls} controls")


if __name__ == "__main__":
    main()
