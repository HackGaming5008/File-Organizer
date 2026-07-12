from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QHBoxLayout, QWidget, 
    QFileDialog
    )
from PyQt6.QtCore import Qt

import sys
from main import functionMain
from pathlib import Path

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.path = None

        self.setWindowTitle("File Organizer")
        self.resize(1200, 760)
        self.setMinimumSize(800, 560)

        main_layout = QHBoxLayout(self)        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.folder_lable = QLabel("No folder selected")
        self.folder_lable.setStyleSheet(
            """
            max-height: 30px; max-width: 420px; font:12px; 
            border: 1px solid #757575;
            border-radius: 5px;
            padding: 2px;
            """
            )
        if self.path:
            self.folder_lable.setText(str(self.path))

        self.sel_folder = QPushButton("Select Folder")
        self.sel_folder.clicked.connect(self.selectFolder)
        self.sel_folder.setStyleSheet("height: 30px; max-width: 120px; font:15px")

        run_btn = QPushButton("Orgonize Files")
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.clicked.connect(self.orgonize_files)
        run_btn.setStyleSheet("height: 30px; max-width: 120px; font:15px")

        main_layout.addWidget(self.folder_lable)
        main_layout.addWidget(self.sel_folder)
        main_layout.addWidget(run_btn)

    def orgonize_files(self):
        functionMain(self.path)
    
    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if folder:
            self.path = Path(folder)
            self.folder_lable.setText(str(self.path))
        else:
            self.folder_lable.setText(str(self.path))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())