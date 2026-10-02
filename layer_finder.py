import os

from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QAction,
    QDialog,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)
from qgis.core import QgsProject, QgsLayerTreeLayer, QgsLayerTreeGroup


class SearchLineEdit(QLineEdit):
    """Campo di ricerca con navigazione dei risultati tramite frecce."""

    def __init__(self, dialog):
        super().__init__(dialog)
        self.dialog = dialog

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.dialog.move_selection(1)
            return

        if event.key() == Qt.Key_Up:
            self.dialog.move_selection(-1)
            return

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.dialog.select_current_layer()
            return

        super().keyPressEvent(event)


class LayerSearchDialog(QDialog):
    """Finestra minimale per cercare e selezionare i layer del progetto."""

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.items = []

        self.setWindowTitle("Cerca layer")
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(500)
        self.resize(600, 350)

        self.search_edit = SearchLineEdit(self)
        self.search_edit.setPlaceholderText("Cerca layer...")
        self.search_edit.textChanged.connect(self.update_results)

        self.results = QListWidget()
        self.results.setAlternatingRowColors(True)
        self.results.itemDoubleClicked.connect(
            lambda item: self.select_current_layer()
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.addWidget(self.search_edit)
        layout.addWidget(self.results)

        self.refresh_layers()
        self.search_edit.setFocus()

    def refresh_layers(self):
        """Legge layer e gruppi presenti nel Layer Tree."""
        self.items = []
        root = QgsProject.instance().layerTreeRoot()

        def collect_nodes(parent):
            for node in parent.children():
                if isinstance(node, QgsLayerTreeLayer):
                    layer = node.layer()

                    if layer is not None:
                        self.items.append(
                            ("layer", layer.id(), layer.name())
                        )

                elif isinstance(node, QgsLayerTreeGroup):
                    self.items.append(
                        ("group", node, node.name())
                    )
                    collect_nodes(node)

        collect_nodes(root)
        self.update_results(self.search_edit.text())

    def update_results(self, text):
        query = text.casefold().strip()

        self.results.blockSignals(True)
        self.results.clear()

        for item_type, item_data, name in self.items:
            if not query or query in name.casefold():
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, item_data)
                item.setData(Qt.UserRole + 1, item_type)
                self.results.addItem(item)

        self.results.blockSignals(False)

        if self.results.count():
            self.results.setCurrentRow(0)

    def move_selection(self, step):
        count = self.results.count()

        if count == 0:
            return

        row = self.results.currentRow()

        if row < 0:
            row = 0
        else:
            row = max(0, min(count - 1, row + step))

        self.results.setCurrentRow(row)

    def select_current_layer(self):
        item = self.results.currentItem()

        if item is None:
            return

        item_type = item.data(Qt.UserRole + 1)

        if item_type == "layer":
            layer_id = item.data(Qt.UserRole)
            layer = QgsProject.instance().mapLayer(layer_id)

            if layer is None:
                self.refresh_layers()
                return

            if self.iface.setActiveLayer(layer):
                self.iface.layerTreeView().setCurrentLayer(layer)
                self.iface.layerTreeView().setFocus()
                self.accept()

        elif item_type == "group":
            group = item.data(Qt.UserRole)

            if group is not None:
                self.iface.layerTreeView().setCurrentNode(group)
                self.iface.layerTreeView().setFocus()
                self.accept()


class LayerFinder(QObject):
    """Plugin QGIS Layer Finder."""

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")

        self.action = QAction(
            QIcon(icon_path),
            "Cerca layer",
            self.iface.mainWindow(),
        )
        self.action.setObjectName("layerFinderAction")
        self.action.setToolTip("Cerca layer")
        self.action.setStatusTip("Cerca rapidamente un layer nel progetto")
        self.action.triggered.connect(self.run)

        # Icona nella barra degli strumenti Plugin di QGIS.
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Layer Finder", self.action)


    def unload(self):
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None

        if self.action is not None:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&Layer Finder", self.action)
            self.action.deleteLater()
            self.action = None

    def run(self):
        if self.dialog is not None:
            self.dialog.refresh_layers()
            self.dialog.show()
            self.dialog.raise_()
            self.dialog.activateWindow()
            self.dialog.search_edit.setFocus()
            self.dialog.search_edit.selectAll()
            return

        self.dialog = LayerSearchDialog(self.iface)
        self.dialog.finished.connect(self._dialog_closed)
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def _dialog_closed(self):
        self.dialog = None
