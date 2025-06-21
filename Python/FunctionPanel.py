from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox, QLineEdit, QLabel, QGroupBox, QHBoxLayout, QTextEdit
import subprocess
import sys
import os
from SphinxTools import generate_sphinx_docs, build_sphinx_html
from GitTools import push_to_github
import webbrowser

class FunctionPanel(QWidget):
    def __init__(self, data_manager, on_refresh_tree=None, on_generate_outline=None, on_generate_ue=None, on_preview_sphinx=None, on_stop_server=None):
        super().__init__()
        self.data_manager = data_manager
        self.on_refresh_tree = on_refresh_tree
        self.on_generate_outline = on_generate_outline
        self.on_generate_ue = on_generate_ue
        self.on_preview_sphinx = on_preview_sphinx
        self.on_stop_server = on_stop_server
        self.init_ui()

    def set_tree_panel(self, tree_panel):
        self.tree_panel = tree_panel

    def init_ui(self):
        layout = QVBoxLayout()
        # 分类管理分区
        cat_group = QGroupBox('分类管理')
        cat_layout = QVBoxLayout()
        self.add_btn = QPushButton('新增分类')
        self.add_btn.clicked.connect(self.add_category)
        cat_layout.addWidget(self.add_btn)
        self.del_btn = QPushButton('删除分类')
        self.del_btn.clicked.connect(self.delete_category)
        cat_layout.addWidget(self.del_btn)
        cat_group.setLayout(cat_layout)
        layout.addWidget(cat_group)
        # 大纲分区
        outline_group = QGroupBox('大纲生成')
        outline_layout = QVBoxLayout()
        self.outline_btn = QPushButton('生成Typora大纲')
        self.outline_btn.clicked.connect(self.generate_outline)
        outline_layout.addWidget(self.outline_btn)
        self.ue_btn = QPushButton('生成UE文档大纲')
        self.ue_btn.clicked.connect(self.generate_ue_outline)
        outline_layout.addWidget(self.ue_btn)
        outline_group.setLayout(outline_layout)
        layout.addWidget(outline_group)
        # Sphinx分区
        sphinx_group = QGroupBox('Sphinx文档')
        sphinx_layout = QVBoxLayout()
        self.sphinx_btn = QPushButton('生成Sphinx文档')
        self.sphinx_btn.clicked.connect(self.generate_sphinx_docs)
        sphinx_layout.addWidget(self.sphinx_btn)
        self.sphinx_build_btn = QPushButton('构建Sphinx静态站点')
        self.sphinx_build_btn.clicked.connect(self.build_sphinx_html)
        sphinx_layout.addWidget(self.sphinx_build_btn)
        self.preview_btn = QPushButton('本地预览Sphinx网页')
        self.preview_btn.clicked.connect(self.preview_local_sphinx)
        sphinx_layout.addWidget(self.preview_btn)
        self.stop_server_btn = QPushButton('停止本地服务器')
        self.stop_server_btn.clicked.connect(self.stop_local_server)
        sphinx_layout.addWidget(self.stop_server_btn)
        sphinx_group.setLayout(sphinx_layout)
        layout.addWidget(sphinx_group)
        
        # 自动化测试分区
        test_group = QGroupBox('自动化测试')
        test_layout = QVBoxLayout()
        self.test_btn = QPushButton('一键测试 (生成并预览)')
        self.test_btn.clicked.connect(self.preview_local_sphinx)
        test_layout.addWidget(self.test_btn)
        test_group.setLayout(test_layout)
        layout.addWidget(test_group)

        # Git分区
        git_group = QGroupBox('GitHub部署')
        git_layout = QVBoxLayout()
        self.commit_input = QLineEdit()
        self.commit_input.setPlaceholderText('输入Commit信息')
        git_layout.addWidget(QLabel('Commit信息:'))
        git_layout.addWidget(self.commit_input)
        self.git_btn = QPushButton('推送到GitHub')
        self.git_btn.clicked.connect(self.push_to_github)
        git_layout.addWidget(self.git_btn)
        self.open_repo_btn = QPushButton('打开仓库位置')
        self.open_repo_btn.clicked.connect(self.open_repository_location)
        git_layout.addWidget(self.open_repo_btn)
        git_group.setLayout(git_layout)
        layout.addWidget(git_group)
        # 日志输出区
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(QLabel('命令输出日志:'))
        layout.addWidget(self.log_output)
        layout.addStretch()
        self.setLayout(layout)

    def add_category(self):
        name, ok = QInputDialog.getText(self, '新增分类', '请输入新分类名称:')
        if ok and name:
            if any(cat['name'] == name for cat in self.data_manager.categories):
                QMessageBox.warning(self, '提示', '该分类已存在！')
                return
            self.data_manager.add_category(name)
            if self.on_refresh_tree:
                self.on_refresh_tree()

    def delete_category(self):
        if not hasattr(self, 'tree_panel') or not self.tree_panel:
            QMessageBox.warning(self, '错误', '未关联到分类树！')
            return

        selected_item = self.tree_panel.tree.currentItem()
        if not selected_item or selected_item.parent() is not None:
            QMessageBox.warning(self, '提示', '请先在左侧选择一个要删除的根分类！')
            return
        
        cat_name = selected_item.text(0)
        
        reply = QMessageBox.question(self, '确认删除', 
            f'确定要删除分类 "{cat_name}" 吗？\n这将同时删除对应的 {cat_name}.json 文件，此操作不可恢复！',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.data_manager.delete_category(cat_name)
            if self.on_refresh_tree:
                self.on_refresh_tree()
            QMessageBox.information(self, '成功', f'分类 "{cat_name}" 已被删除。')

    def generate_outline(self):
        if self.on_generate_outline:
            self.on_generate_outline()

    def generate_ue_outline(self):
        if self.on_generate_ue:
            self.on_generate_ue()

    def generate_sphinx_docs(self):
        try:
            ok, msg = generate_sphinx_docs()
            self.log_output.append(msg)
            if ok:
                QMessageBox.information(self, '成功', msg)
            else:
                QMessageBox.warning(self, '失败', msg)
        except Exception as e:
            self.log_output.append(str(e))
            QMessageBox.warning(self, '异常', str(e))

    def build_sphinx_html(self):
        try:
            ok, msg = build_sphinx_html()
            self.log_output.append(msg)
            if ok:
                QMessageBox.information(self, '成功', msg)
            else:
                QMessageBox.warning(self, '失败', msg)
        except Exception as e:
            self.log_output.append(str(e))
            QMessageBox.warning(self, '异常', str(e))

    def push_to_github(self):
        commit_msg = self.commit_input.text().strip()
        if not commit_msg:
            QMessageBox.warning(self, '提示', '请填写Commit信息！')
            return
        try:
            self.log_output.append('正在推送到GitHub...')
            ok, msg = push_to_github(commit_msg)
            self.log_output.append(msg)
            if ok:
                QMessageBox.information(self, '成功', msg)
            else:
                QMessageBox.warning(self, '失败', msg)
        except Exception as e:
            self.log_output.append(str(e))
            QMessageBox.warning(self, '异常', str(e))

    def preview_local_sphinx(self):
        if self.on_preview_sphinx:
            self.on_preview_sphinx()

    def stop_local_server(self):
        if self.on_stop_server:
            self.on_stop_server()

    def open_repository_location(self):
        try:
            # 打开GitHub网页仓库
            repo_url = 'https://github.com/Tyz-Kotono/Tyz-Kotono.github.io'
            webbrowser.open(repo_url)
            self.log_output.append(f'已打开GitHub仓库: {repo_url}')
        except Exception as e:
            self.log_output.append(f'打开GitHub仓库失败: {str(e)}')
            QMessageBox.warning(self, '错误', f'打开GitHub仓库失败: {str(e)}') 