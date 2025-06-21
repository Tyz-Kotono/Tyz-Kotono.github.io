from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem

class TreePanel(QWidget):
    def __init__(self, data_manager, on_category_selected=None):
        super().__init__()
        self.data_manager = data_manager
        self.on_category_selected = on_category_selected
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel('分类')
        self.refresh_tree()
        self.tree.currentItemChanged.connect(self.handle_item_changed)
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def refresh_tree(self):
        self.tree.clear()
        for cat in self.data_manager.categories:
            item = QTreeWidgetItem([cat['name']])
            self.tree.addTopLevelItem(item)

    def handle_item_changed(self, current, previous):
        if current and self.on_category_selected:
            self.on_category_selected(current.text(0)) 