from gen import Gen
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TestList(Gen):
    """Класс работы с темами"""
    def __init__(self, parent=None):
        super().__init__("test_list_widget", parent)
        self.initTests()
        self.test_list.itemClicked.connect(self.transit_test)
        self.toMenu.clicked.connect(self.transit_back)

        
    def transit_back(self):
        self.parent.Stack.setCurrentIndex(2)
        

        
    def transit_test(self):
        """Переход на саму теорию. В главный класс передается id темы"""
        self.parent.test_id = self.test_list.currentRow() + 1
        print(self.parent.test_id)
        self.parent.Stack.setCurrentIndex(10)

        
    def initTests(self):
        """Заполнение тем"""
        cur = self.parent.cur
        tests = cur.execute("select Test from Tests").fetchall()
        for i in tests:
            text = i[0]
            item = QListWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            font = QFont("Times", 25)
            item.setFont(font)
            self.test_list.addItem(item)
