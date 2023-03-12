from gen import Gen


class Menu(Gen):
    """Класс меню. Организован для работы с меню"""

    def __init__(self, parent=None):
        super().__init__("menu_widget", parent)
        self.theory_but.clicked.connect(self.transit_theory)
        self.train_but.clicked.connect(self.transit_train)
        self.exit.clicked.connect(self.transit_auth)
        self.toTests.clicked.connect(self.transit_tests)
        self.stat.clicked.connect(self.transit_stat)

    def transit_stat(self):
        self.parent.Stack.setCurrentIndex(11)        


    def transit_auth(self):
        """Переход на окно авторизации"""
        self.parent.Stack.setCurrentIndex(0)

        
    def transit_theory(self):
        """Переход на теорию"""
        self.parent.Stack.setCurrentIndex(3)

        
    def transit_train(self):
        self.parent.Stack.setCurrentIndex(5)

    def transit_tests(self):
        self.parent.Stack.setCurrentIndex(9)
        
