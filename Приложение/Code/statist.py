from gen import Gen
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem


class Stat(Gen):
    """Класс организован для работы с окном статистики"""
    def __init__(self, parent=None):
        super().__init__("stat_widget", parent)
        self.toMenu.clicked.connect(self.transit_back)



    def transit_back(self):
        self.parent.Stack.setCurrentIndex(2)
        
    def onTransit(self):
        self.updateData()
        

    def updateData(self):
        cur = self.parent.cur

        self.tab.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        res = cur.execute("""SELECT Test, numb, sum
                             FROM  Results
                             INNER  JOIN
                             Tests ON Results.id_test = Tests.id_test
                             Where id_user = ?
                             """, (self.parent.user[0],)).fetchall()
        rows = len(res)
        print(res)
        print(rows)
        self.tab.setRowCount(rows+2)
        for i in range(rows):
            print(i+1)
            self.tab.setItem(i+1, 0, QTableWidgetItem(res[i][0]))
            self.tab.setItem(i+1, 1, QTableWidgetItem(str(res[i][1])))
            self.tab.setItem(i+1, 2, QTableWidgetItem(str(round(res[i][2]/res[i][1], 2))))
            


        # В этой строке определяется среднее значение оценок ученика за тесты
        self.tab.setItem(rows+1, 0, QTableWidgetItem("Итого:"))
        self.tab.setItem(rows+1, 2, QTableWidgetItem(str(round(sum([res[i][2]/res[i][1] for i in range(rows)])/rows, 2))))

        self.tab.setVerticalHeaderLabels(["" for i in range(rows+2)])

        # Выравнивание таблицы
        self.tab.resizeColumnsToContents()
        self.tab.resizeRowsToContents()

        
        
