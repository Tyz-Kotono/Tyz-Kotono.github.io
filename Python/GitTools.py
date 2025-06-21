import subprocess
import os

# 获取项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def push_to_github(commit_msg, repo_url='https://github.com/Tyz-Kotono/Tyz-Kotono.github.io.git'):
    html_dir = os.path.join(PROJECT_ROOT, 'sphinx_site', '_build', 'html')
    cmds = [
        ['git', 'init'],
        ['git', 'remote', 'remove', 'origin'],  # 先尝试移除origin
        ['git', 'remote', 'add', 'origin', repo_url],
        ['git', 'add', '.'],
        ['git', 'commit', '-m', commit_msg],
        ['git', 'branch', '-M', 'gh-pages'],
        ['git', 'push', '-f', 'origin', 'gh-pages']
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=html_dir, capture_output=True, text=True)
        # remote remove origin 可能会报错（如果没有origin），忽略即可
        if result.returncode != 0 and not (cmd[:3] == ['git', 'remote', 'remove'] and 'No such remote' in result.stderr):
            return False, result.stderr
    return True, '推送成功' 