from gen import Gen
from json import loads
from PyQt5.QtWidgets import QRadioButton, QCheckBox, QMessageBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Test(Gen):
    """Класс работы с темами"""
    def __init__(self, parent=None):
        super().__init__("test_widget", parent)
        self.next.clicked.connect(self.transit_quest)
        self.check.clicked.connect(self.check_clicked)
        self.toMenu.clicked.connect(self.transit_back)

        
    def transit_back(self):
        self.parent.Stack.setCurrentIndex(9)
        
        
    def end(self):
        #Вызов окна с результатом
        dialog = QMessageBox()
        dialog.resize(500, 350)
        but = QPushButton("Хорошо")
        dialog.addButton(but, QMessageBox.AcceptRole)
        dialog.setText(f"Вы прошли тест на {self.balls}")
        dialog.setWindowTitle("Поздравляем!")
        dialog.exec()      
       
        # Работа с бд
        db = self.parent.db
        cur = self.parent.cur
        #Проверка на прохождение ранее
        res = cur.execute("select * from Results where id_test = ? and id_user = ?", (self.parent.test_id, self.parent.user[0])).fetchall()
        if res == []:
            print(self.balls)
            cur.execute("insert into Results (id_test, id_user, numb, sum) values (?, ?, ?, ?)", (self.parent.test_id, self.parent.user[0], 1, self.balls))
        else:
            numb, sum = (res[0][-2], res[0][-1])
            numb += 1
            sum += self.balls
            print(numb, sum)
            cur.execute("Update Results set numb = ?, sum = ? where id_test = ? and id_user = ?", (numb, sum, self.parent.test_id, self.parent.user[0]))
        db.commit()
        self.parent.Stack.setCurrentIndex(9)
        
        
    def transit_quest(self):
        self.cur_quest += 1
        self.number.setText(str(self.cur_quest+1) + " из " + str(self.numb_quest))
        if self.cur_quest == len(self.data):
            return self.end()
        self.type = self.data[self.cur_quest]["Type"]
        self.initData()
        

    def onTransit(self):
        """При переходе получает индекс теста и 
        заполняет из таблицы нужную инфу"""
        self.clear()
        self.balls = 0
        self.cur_quest = 0
        cur = self.parent.cur
        name, self.data = cur.execute("Select Test, Data from Tests where id_test = ?", (self.parent.test_id,)).fetchall()[0]
        self.name.setText(name)
        self.data = loads(self.data)
        self.type = self.data[self.cur_quest]["Type"]
        self.numb_quest = len(self.data)
        self.number.setText(str(self.cur_quest+1) + " из " + str(self.numb_quest))
        self.initData()

        
    def clear(self):
        for i in reversed(range(self.butts.count())): 
            self.butts.itemAt(i).widget().setParent(None)
        self.answ_ed.setText("")

            
    def check_clicked(self):
        answ = []
        if self.type == "oneVar" or self.type == "someVar":
            for i in range(self.butts.count()):
                if self.butts.itemAt(i).widget().isChecked():
                    answ.append(self.butts.itemAt(i).widget().text())
            for i in range(self.butts.count()):
                self.butts.itemAt(i).widget().setEnabled(False)
           
        elif self.type == "enterVar":
            answ.append(self.answ_ed.text().lower())
            self.answ_ed.setEnabled(False)


        dialog = QMessageBox()
        dialog.resize(500, 350)
        but = QPushButton("Хорошо")
        dialog.addButton(but, QMessageBox.AcceptRole)

        if self.data[self.cur_quest]["Right"] == answ:
            self.balls += 1
            dialog.setText("Вы правильно ответили на вопрос")
            dialog.setWindowTitle("Поздравляем!")
            dialog.exec()      
        else:
            dialog.setText("Вы неправильно ответили на вопрос")
            dialog.setWindowTitle("")
            dialog.exec()
        
        
    def initData(self):
        """Заполняет текущий вопрос данными из бд"""
        quest = self.data[self.cur_quest]
        self.clear()
        font = QFont("Times", 16)
        if self.type == "oneVar" or self.type == "someVar":
            self.quest.setText(quest["Question"])
            self.types.setCurrentIndex(0)
            cl = QRadioButton if self.type == "oneVar" else QCheckBox
            for i in range(len(quest["Answers"])):
                wid = cl()
                wid.setText(quest["Answers"][i])
                wid.setFont(font)
                self.butts.addWidget(wid, int(i/2), i%2, Qt.AlignHCenter)
        elif self.type == "enterVar":
            self.quest_2.setText(quest["Question"])
            self.types.setCurrentIndex(1) 
        

        
