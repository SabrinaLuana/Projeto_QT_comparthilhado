import sys
import random
from PyQt5 import QtWidgets, uic, QtGui
from jogomemoria import Ui_MainWindow

class JogoMemoria(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("jogomemoria.ui", self)
        
        self.cartas = [getattr(self, f"label_{i}") for i in range(16)]
        self.movimentos = 0
        self.label_Movimentos.setText("Movimentos: 0")
        self.imagens = [f"imagens/carta{i}.png" for i in range(1, 9)] * 2
        random.shuffle(self.imagens)
        self.estado_cartas = [False] * 16
        self.cartas_reveladas = []
        for i, carta in enumerate(self.cartas):
            carta.setPixmap(QtGui.QPixmap("imagens/verso.png"))
            carta.mousePressEvent = lambda e, i=i: self.virar_carta(i)

    def virar_carta(self, i):
        if self.estado_cartas[i] or len(self.cartas_reveladas) == 2:
            return
        self.cartas[i].setPixmap(QtGui.QPixmap(self.imagens[i]))
        self.estado_cartas[i] = True
        self.cartas_reveladas.append(i)
        if len(self.cartas_reveladas) == 2:
            self.movimentos += 1
            self.label_Movimentos.setText(f"Movimentos: {self.movimentos}")
            QtWidgets.QApplication.processEvents()
            QtCore.QTimer.singleShot(800, self.verificar_par)

    def verificar_par(self):
        i1, i2 = self.cartas_reveladas
        if self.imagens[i1] != self.imagens[i2]:
            self.cartas[i1].setPixmap(QtGui.QPixmap("imagens/verso.png"))
            self.cartas[i2].setPixmap(QtGui.QPixmap("imagens/verso.png"))
            self.estado_cartas[i1] = False
            self.estado_cartas[i2] = False
        self.cartas_reveladas = []

if __name__ == "__main__":
    from PyQt5 import QtCore
    app = QtWidgets.QApplication(sys.argv)
    window = JogoMemoria()
    window.show()
    sys.exit(app.exec_())
