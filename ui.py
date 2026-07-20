from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QHBoxLayout, QWidget, 
    QFileDialog, QVBoxLayout, QCheckBox, QFrame
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

PANEL_LABEL = "margin:0px 0px 12px 0px"

CATAGORIES_CHECK_STYLE = """
QCheckBox{

font: 14px bold;

}
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

        # TOP LAYOUT

        top_frame = QFrame()
        top_frame.setFrameShape(QFrame.Shape.NoFrame)
        top_frame.setStyleSheet("padding: 0px; margin:0px")

        top_layout = QHBoxLayout(top_frame)
        
        self.folder_lable = QLabel("No folder selected")
        self.folder_lable.setStyleSheet(FOLDER_LABEL_STYLE_DEFAULT)
        if self.path:
            self.folder_lable.setText(str(self.path))

        self.sel_folder = QPushButton("Select Folder")
        self.sel_folder.clicked.connect(self.selectFolder)
        self.sel_folder.setStyleSheet("height: 30px; max-width: 120px; font:15px; padding: 2px 8px; margin:0px 10px 0px 0px;")

        top_layout.addWidget(self.folder_lable)
        top_layout.addWidget(self.sel_folder)


        # MIDDLE LAYOUT

            # panel 1 - options 

        panel1 = QFrame()
        panel1.setFrameShape(QFrame.Shape.StyledPanel)
        panel1.setFrameShadow(QFrame.Shadow.Plain)

        options_layout = QVBoxLayout(panel1)

        options_label= QLabel("Options")
        options_label.setStyleSheet(PANEL_LABEL)
        options_layout.addWidget(options_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.deleteEmpty = QCheckBox("Delete empty folder")
        
        categories_check = QCheckBox("Sort Categories")
        categories_check.setStyleSheet(CATAGORIES_CHECK_STYLE)

        catego_ui = self.categories_ui()

        options_layout.addWidget(self.deleteEmpty, alignment=Qt.AlignmentFlag.AlignLeft)
        options_layout.addWidget(categories_check, alignment=Qt.AlignmentFlag.AlignLeft)
        options_layout.addWidget(catego_ui, alignment=Qt.AlignmentFlag.AlignLeft)

        categories_check.toggled.connect(catego_ui.setVisible)

        options_layout.addStretch()


        # panel 2 - preview

        panel2 = QFrame()
        panel2.setFrameShape(QFrame.Shape.StyledPanel)
        panel2.setFrameShadow(QFrame.Shadow.Plain)
        panel2.setStyleSheet("background-color:#121212; border-radius:5px;")
        preview_layout = QVBoxLayout(panel2)

        preview_label = QLabel("Preview")
        preview_label.setStyleSheet(PANEL_LABEL)


        preview_layout.addWidget(preview_label, alignment=Qt.AlignmentFlag.AlignTop)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(panel1,1)
        middle_layout.addWidget(panel2,2)


        #BOTTOM LAYOUT

        bottom_layout = QHBoxLayout()

        run_btn = QPushButton("Orgonize Files")
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.clicked.connect(self.orgonize_files)
        run_btn.setStyleSheet("height: 30px; max-width: 120px; font:15px; padding: 2px 8px; margin:0px 10px 5px 0px;")
        
        bottom_layout.addWidget(run_btn, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(top_frame)
        main_layout.addLayout(middle_layout,2)
        main_layout.addLayout(bottom_layout,1)

    def categories_ui(self):

        categories_frame = QFrame()
        categories_layout = QVBoxLayout(categories_frame)
        self.images = QCheckBox("Images")
        self.pdfs = QCheckBox("PDFs")
        self.documents = QCheckBox("Documents")
        categories_layout.addWidget(self.images)
        categories_layout.addWidget(self.pdfs)
        categories_layout.addWidget(self.documents)
        categories_frame.setVisible(False)
        return categories_frame
    
    # def preview_ui():


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