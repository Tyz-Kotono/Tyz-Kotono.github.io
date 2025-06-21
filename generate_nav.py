import os
import yaml

DOCS_DIR = "docs"
YML_PATH = "mkdocs.yml"

def scan_docs(base_path):
    nav = []

    for root, dirs, files in os.walk(base_path):
        if root == base_path:
            level = nav
        else:
            rel_path = os.path.relpath(root, base_path)
            parts = rel_path.split(os.sep)
            level = nav
            for part in parts:
                found = next((item for item in level if isinstance(item, dict) and part in item), None)
                if not found:
                    new_item = {part: []}
                    level.append(new_item)
                    level = new_item[part]
                else:
                    level = found[part]

        for file in sorted(files):
            if file.endswith(".md"):
                full_path = os.path.relpath(os.path.join(root, file), base_path).replace("\\", "/")
                title = os.path.splitext(file)[0]
                level.append({title: full_path})

    return nav

def update_yml(nav):
    with open(YML_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["nav"] = nav

    with open(YML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print("✅ mkdocs.yml 导航更新完成")

if __name__ == "__main__":
    nav = scan_docs(DOCS_DIR)
    update_yml(nav)
