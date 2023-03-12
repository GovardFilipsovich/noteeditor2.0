from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys
import sqlite3

#Импортирование окон
from train import *
from page import Page
from thems import Thems
from menu import Menu
from gen import Gen
from auth import Auth
from reg import Reg
from testlist import TestList
from test import Test
from statist import Stat

                                           
class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi('../UI/main.ui', self)

        #Подключение к БД
        self.db = sqlite3.connect("../db/db.db")
        self.cur = self.db.cursor()

        self.user = None
        self.theme_id = 0
        self.theme_name = ""
        self.level = 1
        self.test_id = 0
        
        self.auth_wid = Auth(self)
        self.reg_wid = Reg(self)
        self.menu_wid = Menu(self)
        self.thems_wid = Thems(self)
        self.page_wid = Page(self)
        self.train_wid = Train(self)
        self.train_levels_wid = TrainLevels(self)
        self.music_ear_wid = MusicEar(self)
        self.music_read_wid = MusicRead(self)
        self.test_list_wid = TestList(self)
        self.stat_wid = Stat(self)
        self.test_wid = Test(self)
        
        self.Stack.addWidget(self.auth_wid)
        self.Stack.addWidget(self.reg_wid)
        self.Stack.addWidget(self.menu_wid)
        self.Stack.addWidget(self.thems_wid)
        self.Stack.addWidget(self.page_wid)
        self.Stack.addWidget(self.train_wid)
        self.Stack.addWidget(self.train_levels_wid)
        self.Stack.addWidget(self.music_ear_wid)
        self.Stack.addWidget(self.music_read_wid)
        self.Stack.addWidget(self.test_list_wid)
        self.Stack.addWidget(self.test_wid)
        self.Stack.addWidget(self.stat_wid)
        self.Stack.setCurrentIndex(0)


        self.Stack.currentChanged.connect(self.onTransit)

        
    def onTransit(self):
        """Функция вызывает необходимые действия при переходе на экран"""
        self.Stack.currentWidget().onTransit()
        

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())

db.close()


        
    


