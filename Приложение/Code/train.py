from gen import Gen
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QMessageBox, QRadioButton, QHBoxLayout
from player import Player
from enter import *
from music import *
from random import randrange, shuffle, choice


class Train(Gen):
    """Окно выбора тренажера"""

    def __init__(self, parent=None):
        super().__init__("train_widget", parent)
        self.toMenu.clicked.connect(self.transit_menu)
        self.train_ear.clicked.connect(self.transit_levels)
        self.train_read.clicked.connect(self.transit_levels)

        
    def transit_levels(self):
        if self.sender().objectName() == "train_ear":
            self.parent.train_levels_wid.mode = 0
        else:
            self.parent.train_levels_wid.mode = 1
        self.parent.Stack.setCurrentIndex(6)

        
    def transit_menu(self):
        """Переход к меню"""
        self.parent.Stack.setCurrentIndex(2)


class TrainLevels(Gen):
    def __init__(self, parent=None):
        super().__init__("train_levels_widget", parent)
        self.toMenu.clicked.connect(self.transit_menu)
        self.mode = 0
        for i in range(self.buttons.count()):
            self.buttons.itemAt(i).widget().clicked.connect(self.transit_mode)

        
    def transit_menu(self):
        """Переход к меню"""
        self.parent.Stack.setCurrentIndex(5)

        
    def transit_mode(self):
        """Переход к тренировки слуха"""
        sender = self.sender()
        self.parent.level = sender.objectName()
        if self.mode == 0:
            self.parent.Stack.setCurrentIndex(7)
        else:
            self.parent.Stack.setCurrentIndex(8)

        
class MusicEar(Gen):
    """Окно тренировки слуха"""
    def __init__(self, parent=None):
        super().__init__("music_ear_widget", parent)
        self.toMenu.clicked.connect(self.transit_menu)
               
        self.player = Player(self)
        self.player.setGeometry(QRect(150, 170, 600, 150))
        self.player.setObjectName("player")



        self.musicScene = MusicScene(100, 600)
        
        self.musicView = MusicView(self)
        self.musicView.setScene(self.musicScene)
        self.musicView.setSceneRect(self.musicScene.sceneRect())
        self.musicView.setGeometry(QRect(150, 400, 620, 120))
        
        self.check.clicked.connect(self.checkClicked)
        self.cont.clicked.connect(self.onTransit)


    def onTransit(self):
        self.musicScene.clear()
        self.player.clear()
        self.cont.setVisible(False)
        self.init_melody()
        self.player.setSong(f"../temp/{self.parent.level}.mid")

        
    def checkClicked(self):
        """Выполняет проверку введенной мелодии"""
        print(self.musicScene.getMelody())
        print(self.melody)
        if self.musicScene.getMelody() == self.melody:
            dialog = QMessageBox()
            dialog.setText("Вы успешно выполнили упражнение")
            dialog.resize(500, 350)
            dialog.setWindowTitle("Поздравляем!")
            but = QPushButton("Хорошо")
            dialog.addButton(but, QMessageBox.AcceptRole)
            dialog.exec()
            self.cont.setVisible(True)
        else:
            dialog = QMessageBox()
            dialog.setText("Попробуйте еще")
            dialog.resize(500, 350)
            dialog.setWindowTitle("Не верно")
            but = QPushButton("Хорошо")
            dialog.addButton(but, QMessageBox.AcceptRole)
            dialog.exec()
        
        
    def transit_menu(self):
        """Переход к меню"""
        self.parent.Stack.setCurrentIndex(6)

        
    def init_melody(self):
        """Дает мелодию для тренировки"""
        generate = {"lev1": generateMelLevel1, "lev2": generateMelLevel2,
                    "lev3": generateMelLevel3, "lev4": generateMelLevel4,
                    "lev5": generateMelLevel5}
        self.melody = generate[self.parent.level]()
        createMusFile(self.melody, self.parent.level)
        


class MusicRead(Gen):
    """Окно выбора тренажера"""

    def __init__(self, parent=None):
        super().__init__("music_read_widget", parent)
        self.toMenu.clicked.connect(self.transit_menu)
        
        self.musicScene = MusicScene(100, 600)
        
        self.musicView = MusicView(self)
        self.musicView.setScene(self.musicScene)
        self.musicView.setGeometry(QRect(100, 100, 700, 120))

        self.players = []
        self.rad = []

        for i in range(2):
            for j in range(2):
                p = Player()
                r = QRadioButton()
                lay = QHBoxLayout()
                lay.addWidget(r)
                lay.addWidget(p)
                self.vars.addLayout(lay, i, j, Qt.AlignHCenter)
                self.players.append(p)
                self.rad.append(r)

        self.check.clicked.connect(self.checkAnsw)
        self.cont.clicked.connect(self.onTransit)

    def transit_menu(self):
        """Переход к меню"""
        self.parent.Stack.setCurrentIndex(6)
        
    def onTransit(self):
        self.musicScene.clear()
        for i in self.players:
            i.clear()
        self.cont.setVisible(False)
        self.init_melody()
        self.musicScene.setMelody(self.melody)


    def checkAnsw(self):
         dialog = QMessageBox()

         dialog.resize(500, 350)

         but = QPushButton("Хорошо")
         dialog.addButton(but, QMessageBox.AcceptRole)

            
         for i in range(4):
            lay = self.vars.itemAt(i)
            if lay.itemAt(0).widget().isChecked():
                if lay.itemAt(1).widget() == self.rightPlay:
                    dialog.setText("Вы успешно выполнили упражнение")
                    dialog.setWindowTitle("Поздравляем!")
                    dialog.exec()
                    self.cont.setVisible(True)
                else:
                    dialog.setText("Попробуйте еще")
                    dialog.setWindowTitle("Не верно")
                    dialog.exec()
                return
        


    
    def init_melody(self):
        generate = {"lev1": generateMelLevel1, "lev2": generateMelLevel2,
                    "lev3": generateMelLevel3, "lev4": generateMelLevel4,
                    "lev5": generateMelLevel5}
        
        vars = list(generate.keys())
        if self.parent.level == 'lev1' or self.parent.level == "lev2":
            vars.remove(self.parent.level)
            vars.pop(randrange(0, 3))
        elif self.parent.level == "lev3":
            vars.remove("lev1")
            vars.remove("lev2")
        elif self.parent.level == "lev4":
            vars.remove("lev1")
            vars.remove("lev2")
            vars.remove("lev3")
            vars.append(choice(vars))
        elif self.parent.level == "lev5":
            vars = ["lev5"]+["lev5"]+["lev5"]
        # В список добавлен правильный ответ для упращения работы
        vars = [self.parent.level] + vars
        
        for i in range(4):
            if i == 0:
                self.melody = generate[vars[i]]()
                createMusFile(self.melody, str(i))
                continue
            createMusFile(generate[vars[i]](), str(i))
        
        shuffle(self.players)
        for i in range(4):
            self.players[i].clear()
            self.players[i].setSong(f"../temp/{i}.mid")
            if i == 0:
                self.rightPlay = self.players[i]
            

        


        

class Parent(Gen):
    """Окно выбора тренажера"""

    def __init__(self, parent=None):
        super().__init__("train_widget", parent)
        self.level = "lev1"
        

        
        

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MusicRead(Parent())
    window.onTransit()
    window.show()
    sys.exit(app.exec_())

