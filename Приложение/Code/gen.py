from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class Gen(QWidget):
    def __init__(self, ui, parent=None):
        super(Gen, self).__init__()
        self.parent = parent
        uic.loadUi(f'../UI/{ui}.ui', self)

    def onTransit(self):
        pass
