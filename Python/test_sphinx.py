import sys
import os

from SphinxTools import generate_sphinx_docs, build_sphinx_html

print("测试Sphinx文档生成...")
ok, msg = generate_sphinx_docs()
print(f"生成结果: {ok}, {msg}")

if ok:
    print("测试Sphinx构建...")
    ok, msg = build_sphinx_html()
    print(f"构建结果: {ok}, {msg}")
else:
    print("生成失败，跳过构建测试") 