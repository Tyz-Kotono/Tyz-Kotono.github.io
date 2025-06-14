import os
import shutil
import re
from datetime import datetime

# 定义源目录和目标目录
UE_DIR = 'Typora/UE'
CONTENT_DIR = 'content'

def generate_front_matter(file_path, categories):
    """
    生成或更新文章的 Hugo Front Matter。
    """
    title = os.path.splitext(os.path.basename(file_path))[0]
    # 如果文件名以 .md 结尾（例如 Typora 可能保存为 xxx.md.md），则去除
    if title.lower().endswith('.md'):
        title = title[:-3]
    
    # 获取当前时间并格式化为 ISO 8601，带时区
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00') # 假设北京时间
    
    fm_content = f"""---
title: "{title}"
date: {current_date}
draft: false
"""
    if categories:
        fm_content += 'categories:\n'
        for cat in categories:
            fm_content += f'- "{cat}"\n'
    
    fm_content += '---\n\n'
    return fm_content

def fix_image_paths(content, md_file_path):
    """
    修复 Markdown 文件中 Typora 可能生成的绝对路径图片引用，
    将其转换为相对于文章所在目录的 'assets/' 相对路径。
    """
    # 匹配 Markdown 图片链接的正则表达式：![alt_text](image_path)
    # 捕获 alt_text (组1) 和 image_path (组2)
    # image_path 进一步捕获完整的绝对路径 (组3) 和文件名 (组4)
    # 确保只修改绝对路径，保留 Web URL 和已有的相对路径
    
    # 匹配 Windows 绝对路径，例如 C:/Users/.../image.png 或 C:\Users\...\image.png
    # 并且捕获最终的文件名
    absolute_path_pattern = r'(!\[.*?\]\()((?:[A-Za-z]:[\\/](?:[^\\/:*?"<>|\r\n]+[\\/])*)([^\\/:*?"<>|\r\n]+\.(?:png|jpg|jpeg|gif|bmp|svg|webp)))\)'

    def replace_func(match):
        alt_text = match.group(1) # ![alt_text](
        original_full_path = match.group(2) # e.g., C:/Users/tyz/.../image.png
        image_filename = match.group(3)      # e.g., image.png

        # 检查是否为 Web URL，如果是则不修改
        if original_full_path.lower().startswith(('http://', 'https://', '//')):
            return match.group(0) # 返回原始匹配的完整字符串

        # 检查是否为绝对路径 (例如 C:/ 或 D:/ 开头)
        if re.match(r'^[A-Za-z]:[\\/]', original_full_path):
            # 将绝对路径转换为相对于当前文章目录的 assets/ 路径
            # 假设所有图片都应被放置在各自文章的 assets/ 子目录中
            new_relative_path = os.path.join('assets', image_filename).replace('\\', '/') # 统一使用正斜杠
            print(f"  Fixing image path in {os.path.relpath(md_file_path, UE_DIR)}: '{original_full_path}' -> '{new_relative_path}'")
            return f'{alt_text}{new_relative_path})'
        
        # 如果不是绝对路径也不是 Web URL，且不是以 assets/ 或 ./assets/ 开头的，
        # 可能是简单的文件名引用或不带 assets/ 的相对路径。
        # 考虑到 Hugo 的 resource bundle 模式，通常图片会放在 assets/ 目录下。
        # 这里统一处理为 assets/filename。
        if not original_full_path.lower().startswith(('assets/', './assets/')):
            image_filename_from_path = os.path.basename(original_full_path)
            new_relative_path = os.path.join('assets', image_filename_from_path).replace('\\', '/')
            print(f"  Adjusting relative image path in {os.path.relpath(md_file_path, UE_DIR)}: '{original_full_path}' -> '{new_relative_path}'")
            return f'{alt_text}{new_relative_path})'

        return match.group(0) # 其他情况（例如已经正确的相对路径），不修改

    return re.sub(absolute_path_pattern, replace_func, content)


def process_markdown_file(source_file_path):
    """
    处理单个 Markdown 文件：读取、添加/更新 Front Matter、修复图片路径、写入目标位置。
    """
    try:
        relative_path = os.path.relpath(source_file_path, UE_DIR)
        dest_file_path = os.path.join(CONTENT_DIR, relative_path)
        
        dest_dir = os.path.dirname(dest_file_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        print(f"Processing Markdown: {relative_path}")

        # 从文件路径确定分类
        categories = []
        # 分割路径，去除文件名部分
        path_parts = relative_path.split(os.sep)[:-1] 
        for part in path_parts:
            if part.lower() != 'assets': # 排除 'assets' 目录作为分类
                categories.append(part)

        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified_content = content
        # 检查是否已有 Front Matter (以 '---' 开头)
        if not modified_content.strip().startswith('---'):
            front_matter = generate_front_matter(source_file_path, categories)
            modified_content = front_matter + modified_content
        else:
            # 如果已有 Front Matter，尝试更新 title 和 categories (简单更新)
            # 这部分实现是简化的，更严谨的需要 YAML 解析器。
            # 这里仅保证 title 和 categories 的存在，不会覆盖原有复杂配置。
            
            # 查找第二个 '---' 的位置，以分离 Front Matter 和正文
            fm_end_index = modified_content.find('---', 3) 
            if fm_end_index != -1:
                existing_fm = modified_content[:fm_end_index + 3]
                body = modified_content[fm_end_index + 3:]

                # 简单更新 title
                new_title = os.path.splitext(os.path.basename(source_file_path))[0].replace('.md', '')
                if 'title:' not in existing_fm:
                    # 如果没有 title 字段，则插入
                    existing_fm = existing_fm.replace('---', f'---\ntitle: "{new_title}"\n', 1)
                else:
                    # 如果有 title 字段，则替换
                    existing_fm = re.sub(r'title: ".*?"', f'title: "{new_title}"', existing_fm)

                # 简单更新 categories
                if categories and 'categories:' not in existing_fm:
                    new_categories_str = 'categories:\n' + ''.join([f'- "{cat}"\n' for cat in categories])
                    # 尝试在 Front Matter 结束符之前插入 categories
                    existing_fm = existing_fm.replace('---', f'{new_categories_str}---', 1)
                    
                modified_content = existing_fm + body
            else:
                # 如果 Front Matter 格式不完整，也重新生成
                front_matter = generate_front_matter(source_file_path, categories)
                modified_content = front_matter + modified_content


        # 修复图片路径
        modified_content = fix_image_paths(modified_content, source_file_path)

        with open(dest_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
    except Exception as e:
        print(f"Error processing markdown file {source_file_path}: {e}")

def sync_hugo_content():
    """
    主同步函数，将 UE 目录下的内容同步到 content 目录，并进行清理。
    """
    print(f"Starting synchronization from '{UE_DIR}' to '{CONTENT_DIR}'...")
    
    # 用于追踪 UE_DIR 中所有存在的文件和目录，以便后续清理 CONTENT_DIR
    ue_items = set()

    # 第一次遍历：复制文件和目录，并处理 Markdown
    for root, dirs, files in os.walk(UE_DIR):
        # 过滤掉 .git 和 .vs 等不应该复制的目录
        dirs[:] = [d for d in dirs if d not in ['.git', '.vs']] 

        for file_name in files:
            source_file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(source_file_path, UE_DIR)
            dest_file_path = os.path.join(CONTENT_DIR, relative_path)
            
            # 将文件相对路径添加到已处理集合中
            ue_items.add(relative_path) 

            # 确保目标目录存在
            dest_dir = os.path.dirname(dest_file_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            if file_name.lower().endswith('.md'):
                process_markdown_file(source_file_path)
            else:
                # 对于非 Markdown 文件 (例如图片)，直接复制
                try:
                    shutil.copy2(source_file_path, dest_file_path, follow_symlinks=True)
                    print(f"Copied non-Markdown: {relative_path}")
                except Exception as e:
                    print(f"Error copying non-Markdown {relative_path}: {e}")

    # 第二次遍历：清理 CONTENT_DIR 中 UE_DIR 不再存在的文件和目录
    print(f"\nCleaning up '{CONTENT_DIR}'...")
    # topdown=False 确保先删除子文件/目录，再删除父目录
    for root, dirs, files in os.walk(CONTENT_DIR, topdown=False): 
        # 过滤掉不应该被清理的目录，例如 .git 目录 (如果它被误复制过来)
        if os.path.basename(root) in ['.git', '.vs']:
            continue
            
        for file_name in files:
            dest_file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(dest_file_path, CONTENT_DIR)
            
            # 排除 _index.md 文件不被删除
            if relative_path.lower() == '_index.md':
                continue

            if relative_path not in ue_items:
                try:
                    os.remove(dest_file_path)
                    print(f"Deleted old file: {relative_path}")
                except Exception as e:
                    print(f"Error deleting old file {relative_path}: {e}")
        
        # 删除空目录（只删除 CONTENT_DIR 内部的空子目录）
        if not os.listdir(root): # 检查目录是否为空
            # 确保不是 CONTENT_DIR 本身被删除
            if root != CONTENT_DIR: 
                try:
                    os.rmdir(root)
                    print(f"Deleted empty directory: {os.path.relpath(root, CONTENT_DIR)}")
                except Exception as e:
                    print(f"Error deleting empty directory {os.path.relpath(root, CONTENT_DIR)}: {e}")

    print("\nSynchronization complete!")

# 脚本主入口
if __name__ == "__main__":
    sync_hugo_content() 