import os
import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, \
    QFileDialog, QMessageBox, QScrollArea, QTextEdit
from PyQt6.QtCore import Qt
import WSOLA


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Speed Converter")
        self.setMinimumSize(800, 500)  # set the initial window size

        # Algorithm dropdown
        algorithm_label = QLabel("Algorithm:")
        self.algorithm_dropdown = QComboBox()
        self.algorithm_dropdown.addItems(["WSOLA", "PSOLA"])

        algorithm_layout = QHBoxLayout()
        algorithm_layout.addWidget(algorithm_label)
        algorithm_layout.addWidget(self.algorithm_dropdown)

        # Target speed text area
        target_speed_label = QLabel("Target Speed (ratio):")
        self.target_speed_text = QLineEdit()
        self.target_speed_text.setValidator(QtGui.QDoubleValidator())
        self.target_speed_text.setFixedWidth(100)

        target_speed_layout = QHBoxLayout()
        target_speed_layout.addWidget(target_speed_label)
        target_speed_layout.addWidget(self.target_speed_text)

        # Source path selection
        source_path_label = QLabel("Source Path:")
        self.source_path_button = QPushButton("Select Files")
        self.source_path_button.clicked.connect(self.selectSourcePath)
        self.source_path_display = QTextEdit()
        self.source_path_display.setReadOnly(True)
        self.source_path_display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.source_path_display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        source_path_layout = QVBoxLayout()
        source_path_layout.addWidget(source_path_label)
        source_path_layout.addWidget(self.source_path_button)
        source_path_layout.addWidget(self.source_path_display)

        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convertFiles)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(algorithm_layout)
        main_layout.addLayout(target_speed_layout)
        main_layout.addLayout(source_path_layout)
        main_layout.addWidget(self.source_path_display)
        main_layout.addWidget(self.convert_button)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(main_layout)
        scroll_area.setWidget(scroll_widget)

        # Set layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

        self.show()

    def selectSourcePath(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if file_dialog.exec():
            self.source_path_list = file_dialog.selectedFiles()
            self.source_path_display.setText(
                f"{len(self.source_path_list)} file(s) selected:\n" + "\n".join(self.source_path_list))

    def selectSavePath(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        if folder_dialog.exec():
            self.save_path = folder_dialog.selectedFiles()[0]
            self.save_path_display.setText(self.save_path)
            self.same_as_source_checkbox.setChecked(False)

    def updateSavePath(self):
        if self.same_as_source_checkbox.isChecked():
            if self.source_path_list:
                self.save_path = os.path.dirname(self.source_path_list[0])
                self.save_path_display.setText(self.save_path)
            else:
                self.same_as_source_checkbox.setChecked(False)
        else:
            folder_dialog = QFileDialog()
            folder_dialog.setFileMode(QFileDialog.Directory)
            if folder_dialog.exec():
                self.save_path = folder_dialog.selectedFiles()[0]
                self.save_path_display.setText(self.save_path)

    def convertFiles(self):
        algorithm = self.algorithm_dropdown.currentText()
        target_speed = float(self.target_speed_text.text())
        source_paths = self.source_path_list

        if algorithm == 'WSOLA':
            for source_path in source_paths:
                speed = self.target_speed_text
                WSOLA.convert(source_path, target_speed)
            # conversion successful
            QMessageBox.information(self, "Success", "Convert Successful!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())
