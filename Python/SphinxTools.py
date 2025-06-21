import os
import json
import shutil
import subprocess

# 获取项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

JSON_PATH = os.path.join(PROJECT_ROOT, 'jsonFile', '文档.json')
DOC_SRC = os.path.join(PROJECT_ROOT, 'Document', '文档')
SPHINX_ROOT = os.path.join(PROJECT_ROOT, 'sphinx_site')
SPHINX_SOURCE = os.path.join(SPHINX_ROOT, 'source')

def load_ue_outline():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('ue_outline') or data.get('typora_outline')

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def copy_md_file(rel_path):
    src = os.path.join(DOC_SRC, rel_path)
    dst = os.path.join(SPHINX_SOURCE, rel_path)
    ensure_dir(os.path.dirname(dst))
    if os.path.exists(src):
        shutil.copy2(src, dst)
    else:
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(f'# {os.path.basename(rel_path)}\n')

def write_index_rst(dir_path, entries, title='目录'):
    rst_path = os.path.join(dir_path, 'index.rst')
    with open(rst_path, 'w', encoding='utf-8') as f:
        f.write(f'{title}\n')
        f.write('=' * len(title) + '\n\n')
        f.write('.. toctree::\n   :maxdepth: 2\n   :caption: 目录\n\n')
        for entry in entries:
            f.write(f'   {entry}\n')

def build_tree_from_outline(outline):
    tree = {}
    for file_outline in outline:
        parts = file_outline['file'].split('/')
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = file_outline
    return tree

def generate_rst_and_copy(tree, parent_path):
    entries = []
    for name, value in tree.items():
        if isinstance(value, dict) and 'file' in value:
            rel_md = os.path.join(parent_path, name)
            copy_md_file(rel_md)
            entries.append(rel_md.replace('\\', '/'))
        else:
            dir_path = os.path.join(SPHINX_SOURCE, parent_path, name)
            ensure_dir(dir_path)
            sub_entries = generate_rst_and_copy(value, os.path.join(parent_path, name))
            write_index_rst(dir_path, sub_entries, title=name)
            entries.append(f'{os.path.join(parent_path, name)}/index')
    return entries

def generate_sphinx_docs():
    ensure_dir(SPHINX_SOURCE)
    outline = load_ue_outline()
    if not outline:
        return False, '未找到ue_outline或typora_outline'
    tree = build_tree_from_outline(outline)
    entries = generate_rst_and_copy(tree, '')
    write_index_rst(SPHINX_SOURCE, entries, title='文档')
    return True, 'Sphinx 文档目录和导航已生成。'

def build_sphinx_html():
    source = os.path.join(SPHINX_ROOT, 'source')
    outdir = os.path.join(SPHINX_ROOT, '_build', 'html')
    try:
        result = subprocess.run(['sphinx-build', '-b', 'html', source, outdir], capture_output=True, text=True)
        if result.returncode == 0:
            return True, 'Sphinx静态站点已生成！'
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e) 