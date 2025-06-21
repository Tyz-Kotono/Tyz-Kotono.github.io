from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import json

class PreviewPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)
        self.setLayout(layout)

    def show_typora_outline(self, outline):
        if outline:
            tree_text = self.format_outline_tree(outline)
            self.text.setText(tree_text)
        else:
            self.text.setText('(无Typora大纲)')

    def show_ue_outline(self, ue_outline):
        # 假设ue_outline为树状结构
        if ue_outline:
            tree_text = self.format_outline_tree(ue_outline)
            self.text.setText(tree_text)
        else:
            self.text.setText('(无UE文档大纲)')

    def format_outline_tree(self, outline, indent=0):
        lines = []
        for file_outline in outline:
            if isinstance(file_outline, dict) and 'file' in file_outline:
                lines.append('  ' * indent + f"[文件] {file_outline['file']}")
                for node in file_outline['outline']:
                    lines.extend(self.format_outline_node(node, indent + 1))
            else:
                lines.extend(self.format_outline_node(file_outline, indent))
        return '\n'.join(lines)

    def format_outline_node(self, node, indent):
        lines = []
        lines.append('  ' * indent + f"{'#' * node.get('level', 1)} {node.get('title', '')}")
        for child in node.get('children', []):
            lines.extend(self.format_outline_node(child, indent + 1))
        return lines 