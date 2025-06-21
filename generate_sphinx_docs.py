import os
import json
import shutil

# 配置
JSON_PATH = os.path.join('jsonFile', '文档.json')
DOC_SRC = os.path.join('Document', '文档')  # 假设所有md都在Document/文档下
SPHINX_ROOT = 'sphinx_site'
SPHINX_SOURCE = os.path.join(SPHINX_ROOT, 'source')

# 读取ue_outline
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
        # 生成空md
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
            # 文件节点
            rel_md = os.path.join(parent_path, name)
            copy_md_file(rel_md)
            entries.append(rel_md.replace('\\', '/'))
        else:
            # 文件夹节点
            dir_path = os.path.join(SPHINX_SOURCE, parent_path, name)
            ensure_dir(dir_path)
            sub_entries = generate_rst_and_copy(value, os.path.join(parent_path, name))
            # 目录下有index.rst
            write_index_rst(dir_path, sub_entries, title=name)
            entries.append(f'{os.path.join(parent_path, name)}/index')
    return entries

def main():
    # 1. 初始化Sphinx目录
    ensure_dir(SPHINX_SOURCE)
    # 2. 读取大纲
    outline = load_ue_outline()
    if not outline:
        print('未找到ue_outline或typora_outline')
        return
    # 3. 构建树
    tree = build_tree_from_outline(outline)
    # 4. 生成index.rst和拷贝md
    entries = generate_rst_and_copy(tree, '')
    write_index_rst(SPHINX_SOURCE, entries, title='文档')
    print('Sphinx 文档目录和导航已生成。')
    print('请在sphinx_site目录下运行sphinx-quickstart和sphinx-build。')

if __name__ == '__main__':
    main()
 