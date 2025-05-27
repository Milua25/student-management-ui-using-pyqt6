import sys
from PyQt6.QtWidgets import QApplication, QToolBar, QStatusBar, QGridLayout, QLabel, QMessageBox
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from PyQt6.QtCore import  Qt
import sqlite3

class InsertDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses_list = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses_list)
        layout.addWidget(self.course_name)

        # Add mobile Widget

        self.mobile_name = QLineEdit()
        self.mobile_name.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_name)

        # Add Submit button
        button = QPushButton("Insert")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_name.text()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (name, course, mobile) VALUES (?, ? ,?)",
                       (name, course, mobile))
        conn.commit()
        cursor.close()
        conn.close()
        window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        # Add Submit button
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM Students WHERE name = ?", (name,)).fetchall()
        print(result)
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        conn.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        index = window.table.currentRow()
        student_name  = window.table.item(index, 1).text()

        # Get id from selected row
        self.student_id = window.table.item(index, 0).text()

        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        course_name  = window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses_list = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses_list)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile Widget
        mobile = window.table.item(index, 3).text()
        self.mobile_name = QLineEdit(mobile)
        self.mobile_name.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_name)

        # Add Submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",(self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()), self.mobile_name.text(), self.student_id))
        conn.commit()
        cursor.close()
        conn.close()

        window.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation_message = QLabel("Are you sure you want to delete this student?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        layout.addWidget(confirmation_message, 0, 0, 1,2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        self.setLayout(layout)

        yes_button.clicked.connect(self.delete_student)
        no_button.clicked.connect(self.delete_student)



    def delete_student(self):
        # Get index and student from selected row
        index = window.table.currentRow()
        self.student_id = window.table.item(index, 0).text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (self.student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        window.load_data()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Student data deleted")
        confirmation_widget.setText("The record has been deleted successfully")
        confirmation_widget.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add Student
        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # About
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Search Menu
        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Create Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        self.load_data()

        # Add toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create Status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)


        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM Students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        conn.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()


    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
