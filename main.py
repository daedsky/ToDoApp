import os.path
import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from qt_material import apply_stylesheet
from csv_editor import CsvEditor


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        x, y = self.getXYPos()
        self.setGeometry(x, y, 350, 550)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setGeometry(0, 50, 350, 500)

        if os.path.isfile('resources/data/tasks.csv'):
            self.addTasksToWindow()

        self.add_new_btn = QtWidgets.QPushButton("Add new", self)
        self.add_new_btn.setGeometry(5, 7, 90, 25)
        self.add_new_btn.clicked.connect(self.addTaskDialog)

    @staticmethod
    def getXYPos():
        geometry = QtWidgets.QApplication.desktop().screenGeometry()
        width = geometry.width()
        height = geometry.height()
        x = int(width / 2.8)
        y = int(height / 8)
        return x, y

    def addTasksToWindow(self):
        self.groupbox = QtWidgets.QGroupBox('', self.scrollArea)
        self.groupbox.setGeometry(0, 0, 350, 500)

        self.formLayout = QtWidgets.QFormLayout()

        file, data = CsvEditor.read_csv('resources/data/tasks.csv')
        for x in data:
            checkBox = QtWidgets.QCheckBox('')
            checkBox.clicked.connect(self.checkboxFunction)
            label = QtWidgets.QLabel(x.get('task'))
            label.setStyleSheet("font-size:14px;")
            self.formLayout.addRow(checkBox, label)
        file.close()

        self.groupbox.setLayout(self.formLayout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.groupbox)

    def checkboxFunction(self):
        obj = QtCore.QObject()
        sender = obj.sender()
        layout = self.groupbox.layout()
        c = 0
        for x in range(self.formLayout.rowCount()):
            checkbox = layout.itemAt(c).widget()
            if sender == checkbox:
                label = layout.itemAt(c + 1).widget()
                label.setStyleSheet("text-decoration:line-through;")
                checkbox.setDisabled(True)
                break
            c += 2

    def addNewTaskFunction(self):
        task = self.lineEdit.text()

        if not os.path.isfile('resources/data/tasks.csv'):
            CsvEditor.write_csv('resources/data/tasks.csv', ['task'])
        if task == "":
            return
        CsvEditor.append_csv('resources/data/tasks.csv', [task])
        self.dlg.close()
        self.destroyAllItemsInGroupBox()
        self.addTasksToWindow()

    def addTaskDialog(self):
        x, y = self.getXYPosForDialog()

        self.dlg = QtWidgets.QDialog()
        self.dlg.setGeometry(x, y, 300, 165)
        self.dlg.setWindowTitle("Add task")

        label = QtWidgets.QLabel('Task Name', self.dlg)
        label.setStyleSheet("font-size:16px;")
        label.setGeometry(10, 15, 200, 25)

        self.lineEdit = QtWidgets.QLineEdit(self.dlg)
        self.lineEdit.setGeometry(10, 45, 270, 40)
        self.lineEdit.setStyleSheet("font-size:14px;")

        self.btn = QtWidgets.QPushButton('Add', self.dlg)
        self.btn.setGeometry(105, 105, 70, 30)
        self.btn.clicked.connect(self.addNewTaskFunction)

        self.dlg.exec_()

    def getXYPosForDialog(self):
        desktop = QtWidgets.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        x = int(width / 2.5)
        y = int(height / 3.5)
        return x, y

    def destroyAllItemsInGroupBox(self):
        layout = self.groupbox.layout()
        for x in range(layout.rowCount()):
            layout.itemAt(x).widget().deleteLater()
        layout.deleteLater()
        self.groupbox.deleteLater()


app = QtWidgets.QApplication(sys.argv)
apply_stylesheet(app, 'my_dark_lightblue.xml')
window = MainWindow()
window.show()
sys.exit(app.exec_())
