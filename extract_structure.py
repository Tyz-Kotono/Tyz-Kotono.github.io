import os
import json
import re

DOCS_DIR = "docs"
OUTPUT_JSON = "structure.json"

def extract_outline(md_path):
    outlines = []
    with open(md_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                outlines.append({"level": level, "title": title})
    return outlines

def build_structure(base_path):
    nav = []
    outlines = {}

    def recursive(dir_path, rel_path=""):
        items = []
        for entry in sorted(os.listdir(dir_path)):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                sub_items = recursive(full_path, os.path.join(rel_path, entry))
                items.append({entry: sub_items})
            elif entry.endswith(".md"):
                file_rel_path = os.path.join(rel_path, entry).replace("\\", "/")
                title = os.path.splitext(entry)[0]
                items.append({title: file_rel_path})

                # 提取标题结构
                outlines[file_rel_path] = extract_outline(full_path)
        return items

    nav = recursive(base_path)
    return {
        "nav": nav,
        "outline": outlines
    }

if __name__ == "__main__":
    structure = build_structure(DOCS_DIR)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)
    print(f"✅ 导航结构和大纲提取完成，已保存到 {OUTPUT_JSON}")
