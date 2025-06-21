import os
import json
import markdown
from pathlib import Path

# 配置
DOCS_DIR = "docs"
STRUCTURE_JSON = "structure.json"
SITE_DIR = "site"

# HTML 页面模板
TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <nav>
        <h2>导航</h2>
        <ul>{nav_html}</ul>
    </nav>
    <main>
        <h1>{title}</h1>
        <div class="toc">
            <h3>目录</h3>
            <ul>{outline_html}</ul>
        </div>
        <article>{content}</article>
    </main>
</body>
</html>
"""

# 递归生成左侧导航 HTML
def generate_nav(nav_list):
    html = ""
    for item in nav_list:
        if isinstance(item, dict):
            for k, v in item.items():
                html += f"<li>{k}<ul>{generate_nav(v)}</ul></li>"
        else:
            html += f"<li>{item}</li>"
    return html

# 根据 outline 构建 TOC（右侧目录）
def generate_outline(outline):
    html = ""
    for item in outline:
        indent = "&nbsp;" * (item['level'] - 1) * 4
        html += f"<li>{indent}{item['title']}</li>"
    return html

# 渲染单个页面
def render_page(md_path, rel_path, nav, outline):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    title = Path(md_path).stem
    outline_html = generate_outline(outline.get(rel_path, []))
    nav_html = generate_nav(nav)

    return TEMPLATE.format(
        title=title,
        nav_html=nav_html,
        outline_html=outline_html,
        content=html_body
    )

# 写入 HTML 页面
def write_page(output_path, content):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 构建整个站点
def build_site():
    with open(STRUCTURE_JSON, 'r', encoding='utf-8') as f:
        structure = json.load(f)

    if os.path.exists(SITE_DIR):
        import shutil
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR)

    # 写入每个文档页面
    for rel_path in structure['outline']:
        md_path = os.path.join(DOCS_DIR, rel_path)
        html_path = os.path.join(SITE_DIR, rel_path).replace(".md", ".html")
        html = render_page(md_path, rel_path, structure['nav'], structure['outline'])
        write_page(html_path, html)
        print(f"✅ 生成页面: {html_path}")

    # 写入主页
    index_path = os.path.join(SITE_DIR, "index.html")
    index_html = "<h1>欢迎来到我的文档网站！</h1><ul>" + generate_nav(structure['nav']) + "</ul>"
    write_page(index_path, TEMPLATE.format(
        title="首页",
        nav_html=generate_nav(structure['nav']),
        outline_html="",
        content=index_html
    ))

    # 写入 CSS（简洁风格）
    with open(os.path.join(SITE_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write("""
body { font-family: sans-serif; display: flex; margin: 0; }
nav { width: 220px; background: #f0f0f0; padding: 1rem; height: 100vh; overflow: auto; }
main { flex: 1; padding: 2rem; }
article { max-width: 800px; }
.toc { background: #f9f9f9; border-left: 4px solid #ccc; padding: 0.5rem 1rem; margin-bottom: 2rem; }
        """)

    print("🎉 所有页面生成完成！你可以打开 site/index.html 查看网站")

if __name__ == "__main__":
    build_site()
