import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QApplication, QWidget
from PyQt5 import uic


class DataBaseCoffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Статистика по кофе')
        self.con = sqlite3.connect("coffee.sqlite")
        self.tableWidget.resizeColumnsToContents()
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM MainTable").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.k = result[-1][0]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        self.flag = True
        self.pushButton.clicked.connect(self.update)
        self.redact.clicked.connect(self.red)
        self.edit.clicked.connect(self.add)
        self.delete_.clicked.connect(self.delete_coffee)

    def update(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM MainTable").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def add(self):
        self.flag = False
        self.second_form = SecondForm(self.k, 0, self.flag)
        self.second_form.show()
        self.flag = True

    def red(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if ids:
            self.second_form = SecondForm(self.k, ids, self.flag)
            self.second_form.show()
        else:
            QMessageBox.about(self, "Ошибка", "Выберите кофе!")

    def delete_coffee(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if ids:
            valid = QMessageBox.question(self, '', "Вы действительно удалить элементы с id " + ",".join(ids),
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                cur = self.con.cursor()
                for i in ids:
                    data = cur.execute("delete FROM MainTable WHERE id = '{}'".format(i)).fetchone()
                self.con.commit()
        else:
            QMessageBox.about(self, "Ошибка", "Вы не выбрали кофе!")


class SecondForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.n = args[0]
        self.i = args[1]
        self.fl = args[2]
        self.con = sqlite3.connect("coffee.sqlite")
        if self.fl:
            cur = self.con.cursor()
            info = cur.execute(
                "SELECT * from MainTable where id = '{}'".format(*self.i)).fetchone()
            self.name.setText(info[1])
            self.degree.setCurrentText(info[2])
            self.text.setText(info[3])
            self.kind.setCurrentText(info[4])
            self.value.setValue(info[5])
            self.volume.setValue(info[6])
        self.pushButton.clicked.connect(self.update_result)

    def update_result(self):
        cur = self.con.cursor()
        self.n += 1
        if self.fl:
            rez = cur.execute("""UPDATE MainTable SET 'название сорта' = '{}', 'степень прожарки' = '{}'
            , 'описание вкуса' = '{}', 'молотый/ в зёрнах' = '{}', 'цена(в рублях)' = '{}'
            , 'объем упаковки(в граммах)' = '{}'  where id = '{}'""".format(self.name.text(),
                                                                            self.degree.currentText(),
                                                                            self.text.text(),
                                                                            self.kind.currentText(),
                                                                            self.value.value(),
                                                                            self.volume.value(),
                                                                            int(*self.i)))
        else:
            rez = cur.execute(
                """insert into MainTable (id, 'название сорта', 'степень прожарки', 'описание вкуса', 'молотый/ в зёрнах', 'цена(в рублях)',
                 'объем упаковки(в граммах)') values('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(self.n,
                                                                                                         self.name.text(),
                                                                                                         self.degree.currentText(),
                                                                                                         self.text.text(),
                                                                                                         self.kind.currentText(),
                                                                                                         int(
                                                                                                             self.value.value()),
                                                                                                         int(
                                                                                                             self.volume.value())))
        self.con.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataBaseCoffee()
    window.show()
    sys.exit(app.exec())
