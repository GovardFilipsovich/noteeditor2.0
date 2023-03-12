from gen import Gen
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Thems(Gen):
    """Класс работы с темами"""
    
    def __init__(self, parent=None):
        super().__init__("thems_widget", parent)
        self.initThems()
        self.thems_list.itemClicked.connect(self.transit_page)
        self.toMenu.clicked.connect(self.transit_menu)

        
    def transit_page(self):
        """Переход на саму теорию. В главный класс передается id темы"""
        self.parent.theme_id = self.thems_list.currentRow() + 1
        self.parent.theme_name = self.thems_list.currentItem().text()
        self.parent.Stack.setCurrentIndex(4)

        
    def transit_menu(self):
        """Переход к меню"""
        self.parent.Stack.setCurrentIndex(2)
        

    def initThems(self):
        """Заполнение тем"""
        cur = self.parent.cur
        thems = cur.execute("select name_chapter from Theory").fetchall()
        for i in thems:
            text = i[0]
            item = QListWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            font = QFont("Times", 25)
            item.setFont(font)
            self.thems_list.addItem(item)
