import os
import json
import re

class DataJsonManager:
    def __init__(self, jsonfile_path):
        self.jsonfile_path = jsonfile_path
        self.categories = []
        self.category_jsons = {}
        self.categories_json = os.path.join(jsonfile_path, 'categories.json')
        self.load_all_jsons()

    def load_all_jsons(self):
        if not os.path.exists(self.jsonfile_path):
            os.makedirs(self.jsonfile_path)
        # 加载分类
        if os.path.exists(self.categories_json):
            with open(self.categories_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.categories = data.get('categories', [])
        else:
            self.categories = []
        # 加载所有分类json
        self.category_jsons = {}
        for cat in self.categories:
            cat_json_path = os.path.join(self.jsonfile_path, f"{cat['name']}.json")
            if os.path.exists(cat_json_path):
                with open(cat_json_path, 'r', encoding='utf-8') as f:
                    self.category_jsons[cat['name']] = json.load(f)
            else:
                self.category_jsons[cat['name']] = {'category': cat['name'], 'items': []}

    def save_categories(self):
        with open(self.categories_json, 'w', encoding='utf-8') as f:
            json.dump({'categories': self.categories, 'count': len(self.categories)}, f, ensure_ascii=False, indent=2)

    def save_category_json(self, cat_name):
        cat_json_path = os.path.join(self.jsonfile_path, f"{cat_name}.json")
        with open(cat_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.category_jsons[cat_name], f, ensure_ascii=False, indent=2)

    def add_category(self, name):
        new_id = max([cat['id'] for cat in self.categories], default=0) + 1
        self.categories.append({'id': new_id, 'name': name})
        self.save_categories()
        self.category_jsons[name] = {'category': name, 'items': []}
        self.save_category_json(name)

    def delete_category(self, name):
        self.categories = [cat for cat in self.categories if cat['name'] != name]
        self.save_categories()
        if name in self.category_jsons:
            del self.category_jsons[name]
        cat_json_path = os.path.join(self.jsonfile_path, f"{name}.json")
        if os.path.exists(cat_json_path):
            os.remove(cat_json_path)

    def generate_typora_outline(self, document_path):
        for cat in self.categories:
            cat_name = cat['name']
            cat_folder = os.path.join(document_path, cat_name)
            outline = []
            if os.path.exists(cat_folder):
                for root, dirs, files in os.walk(cat_folder):
                    for file in files:
                        if file.endswith('.md'):
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, cat_folder)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            headings = self.parse_md_headings(content)
                            outline.append({
                                'file': rel_path.replace('\\', '/'),
                                'outline': headings
                            })
            if cat_name in self.category_jsons:
                self.category_jsons[cat_name]['typora_outline'] = outline
                self.save_category_json(cat_name)

    def parse_md_headings(self, content):
        lines = content.splitlines()
        stack = []
        root = []
        for line in lines:
            m = re.match(r'^(#+)\s+(.*)', line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                node = {'title': title, 'level': level, 'children': []}
                while stack and stack[-1]['level'] >= level:
                    stack.pop()
                if stack:
                    stack[-1]['children'].append(node)
                else:
                    root.append(node)
                stack.append(node)
        return root 