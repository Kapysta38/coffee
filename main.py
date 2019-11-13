import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.update_table()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setMouseTracking(True)
        self.pushButton.clicked.connect(self.edit)
        self.pushButton_2.clicked.connect(self.update_table_btn)

    def update_table(self):
        con = sqlite3.connect('coffee.db')
        result = con.execute(f"""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def edit(self):
        self.new_win = EditWin(self, self.update_table())
        self.new_win.show()

    def update_table_btn(self):
        self.update_table()


class EditWin(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Редактирование')
        self.con = sqlite3.connect('coffee.db')
        self.value = 0
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.create_row)
        self.update_table()

    def update_table(self):
        result = self.con.execute(f"""SELECT * FROM coffee""").fetchall()
        self.value = len(result)
        self.tableWidget.setRowCount(self.value)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def save(self):
        for i in range(self.value):
            info_list = []
            for j in range(7):
                info_list.append(self.tableWidget.item(i, j).text())
            id = int(info_list[0])
            name = info_list[1]
            roast = info_list[2]
            type = info_list[3]
            description = info_list[4]
            price = float(info_list[5])
            packaging = float(info_list[6])
            self.con.execute(f"""UPDATE coffee SET name = '{name}', roast = '{roast}', type = '{type}',
             description = '{description}', price = {price}, packaging = {packaging} WHERE ID = {id}""")
            self.con.commit()
        self.update_table()

    def create_row(self):
        name = self.lineEdit.text()
        roast = self.lineEdit_2.text()
        type = self.lineEdit_3.text()
        description = self.lineEdit_4.text()
        price = float(self.lineEdit_5.text())
        packaging = float(self.lineEdit_6.text())
        self.con.execute(f"""INSERT INTO coffee (name, roast, type, description, price, packaging) VALUES('{name}', 
        '{roast}', '{type}', '{description}', {price}, {packaging})""")
        self.con.commit()
        self.update_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
