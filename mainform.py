from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

from sintaxAnalysis import do_it_now_beach

#  import lexicalAnalysis


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainform.ui', self)

        self.tables = [self.identifiers_tableWidget, self.constants_tableWidget,
                       self.keywords_tableWidget, self.seporators_tableWidget]

        self.all_keywords = ["end", "loop", "int", "let", "if", "then", "else",
                                "elsif", "for", "do_while", "readln", "writeln"]
        self.all_seporators = [">", "<", ">=", "<=", "+", "-", "*", "/", "!", "=",
                               "==", "{", "}", ";", ",", "(", ")"]

        self.identifiers = set()
        self.keywords = set()
        self.constants = set()
        self.seporators = set()

        self.compile_pushButton.clicked.connect(self.compile)
        self.sintax_pushButton.clicked.connect(self.sintax)

    def sintax(self):
        code = self.code_textEdit.toPlainText()
        respons = do_it_now_beach(code)
        self.sintaxlAnalysis_textEdit.setText(respons)

    def table_settings(self):
        for table in self.tables:
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["N", "Значения"])
            table.verticalHeader().setVisible(False)
            table.setColumnWidth(0, 50)
            table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

    def add_value_to_table(self, ind_table, word):
        table = self.tables[ind_table - 1]

        row_position = table.rowCount()
        table.insertRow(row_position)
        item = QTableWidgetItem(str(row_position + 1))
        table.setItem(row_position, 0, item)
        item = QTableWidgetItem(word)
        table.setItem(row_position, 1, item)

        cursor = self.lexicalAnalysis_textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(f"({ind_table}, {row_position + 1}) ")

    def compile(self):
        self.table_settings()

        text_code = self.code_textEdit.toPlainText()
        text_code.replace("\n", " ")
        code = text_code.split()
        len_code = len(code)
        comment_flag = False

        for word in code:
            if word == "(*":
                comment_flag = True

            if comment_flag:
                if word == "*)":
                    comment_flag = False
                continue
            elif word in self.all_keywords:
                ind_table = 3

                if word not in self.keywords:
                    self.add_value_to_table(ind_table, word)

                    self.keywords.add(word)
            elif word.isdigit():
                ind_table = 2

                if word not in self.constants:
                    self.add_value_to_table(ind_table, word)

                    self.constants.add(word)
            elif word in self.all_seporators:
                ind_table = 4

                if word not in self.seporators:
                    self.add_value_to_table(ind_table, word)

                    self.seporators.add(word)
            else:
                ind_table = 1

                if word not in self.identifiers:
                    self.add_value_to_table(ind_table, word)

                    self.identifiers.add(word)

        '''self.keywords_tableWidget.resizeColumnsToContents()
        self.keywords_tableWidget.resizeRowsToContents()

        self.seporators_tableWidget.resizeColumnsToContents()
        self.seporators_tableWidget.resizeRowsToContents()

        self.constants_tableWidget.resizeColumnsToContents()
        self.constants_tableWidget.resizeRowsToContents()

        self.identifiers_tableWidget.resizeColumnsToContents()
        self.identifiers_tableWidget.resizeRowsToContents()'''
