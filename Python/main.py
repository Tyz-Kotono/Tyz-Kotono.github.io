import sys
import os
import re
import time

# 保证无论从哪里启动都能找到jsonFile等目录
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 将项目根目录添加到sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import webbrowser
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QMessageBox, QDockWidget, QSplitter, QTreeWidget, QTreeWidgetItem, QTextEdit, QLabel, QVBoxLayout
from DataJsonManager import DataJsonManager
from TreePanel import TreePanel
from FunctionPanel import FunctionPanel
from PreviewPanel import PreviewPanel
from PySide6.QtCore import Qt

JSONFILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'jsonFile')
DOCUMENT_PATH = os.path.join(os.path.dirname(__file__), '..', 'Document')

class UEDocDock(QDockWidget):
    def __init__(self, data_manager, document_path):
        super().__init__('UE文档大纲')
        self.data_manager = data_manager
        self.document_path = document_path
        self.current_cat_name = None
        self.file_outline_map = {}
        self.init_ui()

    def init_ui(self):
        splitter = QSplitter()
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel('文件大纲')
        self.file_tree.itemClicked.connect(self.on_file_selected)
        splitter.addWidget(self.file_tree)
        self.outline_tree = QTreeWidget()
        self.outline_tree.setHeaderLabel('层级大纲')
        splitter.addWidget(self.outline_tree)
        self.content_view = QTextEdit()
        self.content_view.setReadOnly(True)
        splitter.addWidget(self.content_view)
        splitter.setSizes([200, 200, 400])
        self.setWidget(splitter)

    def show_for_category(self, cat_name):
        self.data_manager.load_all_jsons()
        self.current_cat_name = cat_name
        self.file_tree.clear()
        self.outline_tree.clear()
        self.content_view.clear()
        self.file_outline_map = {}
        cat_json = self.data_manager.category_jsons.get(cat_name, {})
        ue_outline = cat_json.get('ue_outline', [])
        # 构建文件大纲树（支持多级文件夹）
        file_tree_root = {}
        for file_outline in ue_outline:
            path_parts = file_outline['file'].split('/')
            self.insert_file_tree(file_tree_root, path_parts, file_outline['file'], file_outline['outline'])
        self.populate_file_tree(self.file_tree, file_tree_root)

    def insert_file_tree(self, node, path_parts, file_path, outline):
        if not path_parts:
            node['__file__'] = file_path
            node['__outline__'] = outline
            return
        part = path_parts[0]
        if part not in node:
            node[part] = {}
        self.insert_file_tree(node[part], path_parts[1:], file_path, outline)

    def populate_file_tree(self, parent, node):
        for key, value in node.items():
            if key.startswith('__'):
                continue
            item = QTreeWidgetItem([key])
            parent.addTopLevelItem(item) if isinstance(parent, QTreeWidget) else parent.addChild(item)
            if '__file__' in value:
                item.setData(0, 1, value['__file__'])
                self.file_outline_map[value['__file__']] = value['__outline__']
            self.populate_file_tree(item, value)

    def on_file_selected(self, item, col):
        # 只在叶子节点（文件）上响应
        file_name = item.data(0, 1)
        self.outline_tree.clear()
        if file_name:
            outline = self.file_outline_map.get(file_name, [])
            for node in outline:
                self.add_outline_node(self.outline_tree, node)
            # 显示文档内容
            cat_name = self.current_cat_name
            file_path = os.path.join(self.document_path, cat_name, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.content_view.setText(f.read())
            else:
                self.content_view.setText('(文件不存在)')

    def add_outline_node(self, parent, node):
        item = QTreeWidgetItem([f"{'#' * node['level']} {node['title']}"])
        parent.addTopLevelItem(item) if isinstance(parent, QTreeWidget) else parent.addChild(item)
        for child in node.get('children', []):
            self.add_outline_node(item, child)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Blog 分类管理工具')
        self.resize(1500, 800)
        self.data_manager = DataJsonManager(JSONFILE_PATH)
        self.http_server_process = None
        # 自动生成UE大纲用于测试
        for cat in self.data_manager.categories:
            cat_name = cat['name']
            typora_outline = self.data_manager.category_jsons.get(cat_name, {}).get('typora_outline', [])
            self.data_manager.category_jsons[cat_name]['ue_outline'] = typora_outline
            self.data_manager.save_category_json(cat_name)
        self.init_ui()

    def init_ui(self):
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks)

        # 实例化所有面板
        self.tree_panel = TreePanel(self.data_manager, self.on_category_selected)
        self.func_panel = FunctionPanel(
            self.data_manager,
            on_refresh_tree=self.refresh_tree,
            on_generate_outline=self.generate_typora_outline,
            on_generate_ue=self.show_ue_dock,
            on_preview_sphinx=self.preview_sphinx_site,
            on_stop_server=self.stop_http_server
        )
        self.preview_panel = PreviewPanel()

        # 创建Dock
        tree_dock = QDockWidget("文档分类")
        tree_dock.setWidget(self.tree_panel)
        func_dock = QDockWidget("功能面板")
        func_dock.setWidget(self.func_panel)
        preview_dock = QDockWidget("内容预览")
        preview_dock.setWidget(self.preview_panel)
        self.ue_dock = UEDocDock(self.data_manager, DOCUMENT_PATH)
        self.ue_dock.setWindowTitle("UE文档大纲")

        # 水平并排布局
        self.addDockWidget(Qt.LeftDockWidgetArea, tree_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, func_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, preview_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ue_dock)
        self.ue_dock.hide()

        # 让三个左侧Dock并排
        self.splitDockWidget(tree_dock, func_dock, Qt.Horizontal)
        self.splitDockWidget(func_dock, preview_dock, Qt.Horizontal)

        # 建立func_panel对tree_panel的引用
        self.func_panel.set_tree_panel(self.tree_panel)

        # 默认Dock可见
        tree_dock.setVisible(True)
        func_dock.setVisible(True)
        preview_dock.setVisible(True)
        self.ue_dock.setVisible(False)

        # Dock可浮动、可关闭
        for dock in [tree_dock, func_dock, preview_dock, self.ue_dock]:
            dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)

    def refresh_tree(self):
        self.data_manager.load_all_jsons()
        self.tree_panel.refresh_tree()

    def on_category_selected(self, cat_name):
        # 默认显示typora大纲
        outline = self.data_manager.category_jsons.get(cat_name, {}).get('typora_outline', [])
        self.preview_panel.show_typora_outline(outline)

    def generate_typora_outline(self):
        self.data_manager.generate_typora_outline(DOCUMENT_PATH)
        QMessageBox.information(self, '完成', 'Typora大纲已生成并写入各分类json！')
        self.refresh_tree()

    def show_ue_dock(self):
        cat_item = self.tree_panel.tree.currentItem()
        if not cat_item:
            QMessageBox.warning(self, '提示', '请先选择一个大分类！')
            return
        cat_name = cat_item.text(0)
        self.ue_dock.show()
        self.ue_dock.raise_()
        self.ue_dock.show_for_category(cat_name)

    def generate_ue_outline(self):
        # 全量同步所有分类的typora_outline为ue_outline
        for cat in self.data_manager.categories:
            cat_name = cat['name']
            typora_outline = self.data_manager.category_jsons.get(cat_name, {}).get('typora_outline', [])
            self.data_manager.category_jsons[cat_name]['ue_outline'] = typora_outline
            self.data_manager.save_category_json(cat_name)
        QMessageBox.information(self, '完成', '所有分类的UE文档大纲已生成！')
        self.refresh_tree()

    def preview_sphinx_site(self):
        # 1. 立即停止任何正在运行的服务器，释放文件锁
        self.stop_http_server(silent=True)

        SPHINX_ROOT = 'sphinx_site'
        SPHINX_SOURCE = os.path.join(SPHINX_ROOT, 'source')
        SPHINX_BUILD = os.path.join(SPHINX_ROOT, '_build')
        HTML_DIR = os.path.join(SPHINX_BUILD, 'html')

        try:
            # 2. 清理旧的构建 (带重试机制)
            if os.path.exists(SPHINX_BUILD):
                import shutil
                import time
                for i in range(5):
                    try:
                        shutil.rmtree(SPHINX_BUILD)
                        self.func_panel.log_output.append(f'已清理旧的构建目录: {SPHINX_BUILD}')
                        break
                    except OSError as e:
                        if hasattr(e, 'winerror') and e.winerror == 32 and i < 4:
                            self.func_panel.log_output.append(f'无法删除目录（可能被占用），将在1秒后重试... ({i+1}/5)')
                            time.sleep(1.0)
                        else:
                            raise e
            
            # 3. (重新)生成rst和拷贝md文件
            from generate_sphinx_docs import main as generate_docs_main
            generate_docs_main()
            self.func_panel.log_output.append('已生成Sphinx源文件（.rst）。')
            
            # 4. 运行sphinx-build
            build_command = [
                sys.executable, '-m', 'sphinx',
                '-b', 'html',
                SPHINX_SOURCE,
                HTML_DIR
            ]
            self.func_panel.log_output.append(f'正在运行: {" ".join(build_command)}')
            result = subprocess.run(build_command, capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                self.func_panel.log_output.append('Sphinx构建成功。')
                self.func_panel.log_output.append(result.stdout)
            else:
                self.func_panel.log_output.append('Sphinx构建失败。')
                self.func_panel.log_output.append(result.stderr)
                error_msg = f'Sphinx构建失败，请查看日志获取详细信息。\n{result.stderr}'
                self.func_panel.log_output.append(error_msg)
                QMessageBox.critical(self, '构建失败', error_msg)
                return
        
        except Exception as e:
            error_msg = f'准备预览时发生错误: {e}'
            self.func_panel.log_output.append(error_msg)
            QMessageBox.critical(self, '错误', error_msg)
            return

        # 5. 验证构建内容
        self.func_panel.log_output.append("正在验证构建内容...")
        try:
            index_html_path = os.path.join(HTML_DIR, 'index.html')
            theme_css_path = os.path.join(HTML_DIR, '_static', 'css', 'theme.css')
            
            if not os.path.exists(index_html_path) or not os.path.exists(theme_css_path):
                error_msg = '内容验证失败：未找到 index.html 或主题CSS文件。'
                self.func_panel.log_output.append(error_msg)
                QMessageBox.warning(self, '构建内容错误', error_msg)
                return
            
            with open(index_html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            project_name = 'MyDocs' 
            conf_py_path = os.path.join(SPHINX_SOURCE, 'conf.py')
            if os.path.exists(conf_py_path):
                with open(conf_py_path, 'r', encoding='utf-8') as f:
                    conf_content = f.read()
                    match = re.search(r"project\s*=\s*['\"]([^'\"]+)['\"]", conf_content)
                    if match:
                        project_name = match.group(1)
            
            title_pattern = f'<title>.*{re.escape(project_name)}.*</title>'
            if re.search(title_pattern, content, re.IGNORECASE):
                self.func_panel.log_output.append(f"内容验证成功：在index.html中找到了项目标题 '{project_name}'。")
            else:
                error_msg = f"内容验证失败：未在 index.html 中找到预期的项目标题 '{project_name}'。"
                self.func_panel.log_output.append(error_msg)
                QMessageBox.warning(self, '构建内容错误', error_msg)
                return
        except Exception as e:
            error_msg = f"验证构建内容时发生错误: {e}"
            self.func_panel.log_output.append(error_msg)
            QMessageBox.critical(self, '错误', error_msg)
            return

        # 6. 启动新服务器
        if self.http_server_process is None or self.http_server_process.poll() is not None:
            try:
                port = 8888  # 使用一个不常用的端口避免冲突
                self.http_server_process = subprocess.Popen(
                    [sys.executable, '-m', 'http.server', str(port)],
                    cwd=HTML_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW # Windows下不显示黑窗口
                )
                log_msg = f'HTTP服务器已在 http://localhost:{port} 启动...'
                self.func_panel.log_output.append(log_msg)
                webbrowser.open(f'http://localhost:{port}')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'启动服务器失败: {e}')
                return
        else:
             # 如果服务器已在运行，直接打开浏览器
            webbrowser.open(f'http://localhost:8888')

    def stop_http_server(self, silent=False):
        if self.http_server_process and self.http_server_process.poll() is None:
            pid = self.http_server_process.pid
            self.func_panel.log_output.append(f"准备停止服务器进程 PID: {pid}...")
            try:
                if sys.platform == "win32":
                    kill_command = ['taskkill', '/F', '/T', '/PID', str(pid)]
                    subprocess.run(kill_command, capture_output=True, text=True, check=False)
                    # 等待直到进程确认被终止
                    for _ in range(5):
                        check_command = ['tasklist', '/FI', f'PID eq {pid}']
                        result = subprocess.run(check_command, capture_output=True, text=True, encoding='utf-8')
                        if str(pid) not in result.stdout:
                            self.func_panel.log_output.append(f"确认进程 PID: {pid} 已被终止。")
                            break
                        import time
                        time.sleep(0.5)
                    else:
                        self.func_panel.log_output.append(f"警告: 进程 PID: {pid} 在2.5秒后仍未确认停止。")
                else: 
                    self.http_server_process.kill()
                    self.http_server_process.wait()

            except Exception as e:
                log_msg = f"停止服务器时发生未知错误: {e}"
                self.func_panel.log_output.append(log_msg)
            
            self.http_server_process = None
            if not silent:
                self.func_panel.log_output.append("本地HTTP服务器已停止。")
        else:
            if not silent:
                self.func_panel.log_output.append("本地HTTP服务器未在运行。")

    def closeEvent(self, event):
        self.stop_http_server(silent=True)
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main() 