from gen import Gen
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QPushButton

class Reg(Gen):
    def __init__(self, parent=None):
        super().__init__("reg_widget", parent)
        self.enter.clicked.connect(self.transit_menu)
        self.back.clicked.connect(self.transit_auth)


    def transit_auth(self):
        """Переход на окно авторизации"""
        self.parent.Stack.setCurrentIndex(0)
        
    def check(self):
        """Проверка введенных данных на пустоту и проверка уникальности имени пользователя"""
        name = self.name_ed.text()
        pass1 = self.pass_ed.text()
        pass2 = self.pass_ed2.text()

        dialog = QMessageBox()
        dialog.resize(500, 350)
        but = QPushButton("Хорошо")
        dialog.addButton(but, QMessageBox.AcceptRole)    

        #Проверка на пустоту
        if name == "" or pass1 == "" or pass2 == "":
            dialog.setText("Не до конца заполнены поля!")
            dialog.setWindowTitle("Ошибка регистрации")
            dialog.exec()
            return False

        #Проверка на совпадение паролей
        if pass1 != pass2:
            dialog.setText("Пароли не совпадают!")
            dialog.setWindowTitle("Ошибка регистрации")
            dialog.exec()
            return False

        names = self.parent.cur.execute("select name from Users").fetchall()

        #Проверка на существование пользователя
        if (name,) in names:
            dialog.setText("Такой пользователь уже существует!")
            dialog.setWindowTitle("Ошибка регистрации")
            dialog.exec()
            return False
        return True

    
    def add(self):
        user = (self.name_ed.text(), self.pass_ed.text())
        self.parent.cur.execute("Insert into Users (name, password) values(?,?)", user)
        self.parent.db.commit()

        
    def transit_menu(self):
        """Переход к меню"""
        if self.check():
            self.add()
            self.parent.Stack.setCurrentIndex(2)
