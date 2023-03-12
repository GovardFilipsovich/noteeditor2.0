from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox, QPushButton
from PyQt5.QtCore import pyqtSignal
from gen import Gen


class ClickLabel(QLabel):
    clicked = pyqtSignal()
 
    def mousePressEvent(self, e):
        self.clicked.emit()     

        
class Auth(Gen):
    def __init__(self, parent=None):
        super().__init__("auth_widget", parent)
        self.link.__class__ = ClickLabel
        self.link.clicked.connect(self.transit_reg)
        self.enter.clicked.connect(self.transit_menu)

    def onTransit(self):
        """При переходе на страницу очищает данные"""
        self.name_ed.setText("")
        self.pass_ed.setText("")
        

    def transit_reg(self):
        """Переход на окно регистрации"""
        self.link.setText('<html><head/><body><p><span style=" color:#55007f;">Зарегистрироваться</span></p></body></html>')
        self.parent.Stack.setCurrentIndex(1)

        
    def check(self):
        name = self.name_ed.text()
        passw = self.pass_ed.text()

        total = False

        #Запрос к БД
        cur = self.parent.cur
        user = cur.execute(f"select id_user, name, password from Users where name = '%s'" % name).fetchone()
            
        if user:
            total = user[2] == passw

        if total:
            self.parent.user = user
                
        return total
        

    def transit_menu(self):
        """Переход к меню"""
        if self.check():
            self.parent.Stack.setCurrentIndex(2)
        else:
            dialog = QMessageBox()
            dialog.resize(500, 350)
            but = QPushButton("Хорошо")
            dialog.addButton(but, QMessageBox.AcceptRole)
            dialog.setText("Неправильный логин или пароль!")
            dialog.setWindowTitle("Ошибка авторизации")
            dialog.exec()
            return
