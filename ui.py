from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QHBoxLayout, QWidget, 
    QFileDialog, QVBoxLayout, QCheckBox
    )
from PyQt6.QtCore import Qt

import sys
from main import functionMain
from pathlib import Path

FOLDER_LABEL_STYLE_DEFAULT = """
            max-height: 30px; min-height: 30px; max-width: 420px; min-width: 420px;
            border: 3px dashed #575757;
            border-radius: 13px;
            padding: 2px;
            font: 15px;
            """

FOLDER_LABEL_STYLE_ACTIVE = """
                max-height: 30px; min-height: 30px; max-width: 420px; min-width: 420px;  
                background:#737373;
                border: 3px dashed #575757;
                border-radius: 13px;
                padding: 2px;
                font: 15px;
            """

FOLDER_LABEL_STYLE_SELECTED = """
                    max-height: 30px; min-height: 30px; max-width: 420px; min-width: 420px;
                    border: 1px solid #575757;
                    border-radius: 5px;
                    padding: 2px;
                    font: 15px;
                    """


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.path = None

        self.setWindowTitle("File Organizer")
        # self.resize(1200, 760)
        self.setMinimumSize(650, 560)
        self.setAcceptDrops(True)
        self.setup_ui()


    def setup_ui(self):

        folder_drop_layout = QHBoxLayout()
        checkBox_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.folder_lable = QLabel("No folder selected")
        self.folder_lable.setStyleSheet(FOLDER_LABEL_STYLE_DEFAULT)
        if self.path:
            self.folder_lable.setText(str(self.path))

        self.sel_folder = QPushButton("Select Folder")
        self.sel_folder.clicked.connect(self.selectFolder)
        self.sel_folder.setStyleSheet("height: 30px; max-width: 120px; font:15px; padding: 2px 8px; margin:0px 10px 0px 0px;")

        folder_drop_layout.addStretch()
        folder_drop_layout.addWidget(self.folder_lable)
        folder_drop_layout.addWidget(self.sel_folder)
        folder_drop_layout.addStretch()


        moveEnabled_checkBox = QCheckBox("Enable Moving files")
        checkBox_layout.addWidget(moveEnabled_checkBox, alignment=Qt.AlignmentFlag.AlignLeft)

        run_btn = QPushButton("Orgonize Files")
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.clicked.connect(self.orgonize_files)
        run_btn.setStyleSheet("height: 30px; max-width: 120px; font:15px; padding: 2px 8px; margin:0px 10px 5px 0px;")
        
        bottom_layout.addWidget(run_btn, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(folder_drop_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(checkBox_layout)
        main_layout.addStretch(8)
        main_layout.addLayout(bottom_layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.folder_lable.setStyleSheet(FOLDER_LABEL_STYLE_ACTIVE)
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.folder_lable.setStyleSheet(FOLDER_LABEL_STYLE_DEFAULT)
    
    def dropEvent(self, event):
        """Triggered when the object is dropped."""
        # Loop through the dropped URLs (in case multiple are dropped)
        for url in event.mimeData().urls():
            # Convert the QUrl to a local file system path string
            self.path = Path(url.toLocalFile())
            
            # Verify if the path is actually a directory/folder
            if self.path.is_dir():
                self.folder_lable.setText(str(self.path))
                self.folder_lable.setStyleSheet(FOLDER_LABEL_STYLE_SELECTED)
                print(f"Successfully grabbed folder path: {self.path}")
            else:
                self.folder_lable.setText("That was a file, not a folder! Try again.")
                print(f"Dropped item is a file, ignored: {self.path}")

    def orgonize_files(self):
        functionMain(self.path)
    
    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if folder:
            self.path = Path(folder)
            self.folder_lable.setText(str(self.path))
            self.folder_lable.setStyleSheet(FOLDER_LABEL_STYLE_SELECTED)
        else:
            self.folder_lable.setText(str(self.path))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())