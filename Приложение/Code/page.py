from gen import Gen
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import os.path


class Page(Gen):
    """Класс отображения теории"""
    
    def __init__(self, parent=None):
        super().__init__("page_widget", parent)
        self.curPage = 1
        self.num_pages = 0
        self.forward.clicked.connect(self.transForw)
        self.end.clicked.connect(self.transEnd)
        self.back.clicked.connect(self.transBack)
        self.start.clicked.connect(self.transStart)
        self.toThem.clicked.connect(self.transit_themes)

        
    def initPage(self):
        """Инициализация страницы из БД"""
        pages = self.parent.cur.execute("select * from Pages where id_theory = ?", (self.parent.theme_id,)).fetchall()

        #Отбражение кол-ва страниц
        self.num_pages = len(pages)
        self.number.setText(str(self.curPage) + " из " + str(self.num_pages))
        
        page = [i for i in pages if i[-1] == self.curPage][0]
        self.name.setText(self.parent.theme_name)
        self.subname.setText(page[1])
        self.initText(page[2])

        
    def initText(self, text):
        """Отображает текст и картинки на странице"""
        labels = text.split("\r\n")
        self.page.setStretch(0, 0)
        for i in labels:
            label = QLabel()
            if "img" in i and os.path.isfile(f"../img/{i}.png"):
                img = QPixmap(f"../img/{i}.png")
                img.scaled(label.width(), label.height(), Qt.KeepAspectRatio)
                label.setPixmap(img)
                label.setAlignment(Qt.AlignHCenter)
            elif "audio" in i:
                pass
            else:
                font = QFont("Times", 20)
                label.setFont(font)
                label.setText(i)
                label.setWordWrap(True)
            self.page.addWidget(label)

            
    def clear(self):
        """Очищает элементы в layout"""
        for i in reversed(range(self.page.count())): 
            self.page.itemAt(i).widget().deleteLater()

            
    def transForw(self):
        """Переход между страницами"""
        self.clear()
        self.curPage += 1
        if(self.curPage > self.num_pages): self.curPage = self.num_pages
        self.initPage()

        
    def transBack(self):
        """Переход между страницами"""
        self.clear()
        self.curPage -= 1
        if(self.curPage < 1): self.curPage = 1
        self.initPage()

        
    def transStart(self):
        """Переход между страницами"""
        self.clear()
        self.curPage = 1
        self.initPage()

        
    def transEnd(self):
        """Переход между страницами"""
        self.clear()
        self.curPage = self.num_pages
        self.initPage()
    
    
    def transit_themes(self):
        """Переход к темам"""
        self.clear()
        self.curPage = 1
        self.parent.Stack.setCurrentIndex(3)

        
    def onTransit(self):
        self.initPage()



class Parent(Gen):
    """Окно выбора тренажера"""

    def __init__(self, parent=None):
        super().__init__("train_widget", parent)
        #Подключение к БД
        import sqlite3 
        self.db = sqlite3.connect("../db/db.db")
        self.cur = self.db.cursor()

        self.user = None
        self.theme_id = 4
        self.theme_name = ""
       
        


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Page(Parent())
    window.onTransit()
    window.show()
    sys.exit(app.exec_())
