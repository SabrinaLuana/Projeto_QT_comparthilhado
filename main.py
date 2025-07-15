import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from jogomemoria import Ui_MainWindow

class JogoMemoria(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setupUi(self)

        # essa linha busca todas as Qlabels
        self.cartas = [getattr(self, f"label_{i}") for i in range(16)]

        # essas duas linhas iniciam o contador de movimentos
        self.movimentos = 0
        self.label_Movimentos.setText("Movimentos: 0")

        # aqui cria 8 pares de imagens e embaralha
        self.imagens = [f"imagens/carta{i}.png" for i in range(1, 9)] * 2
        random.shuffle(self.imagens)

        # lista que indica se cada carta ja esta virada
        self.estado_cartas = [False] * 16

        # guarda as atuais cartas viradas, temporariamente
        self.cartas_reveladas = []


        # coloca a imagem do verso
        # mousePressEvent executa virar_carta quando clicado
        for i, carta in enumerate(self.cartas):
            carta.setPixmap(QtGui.QPixmap("imagens/verso.png"))
            carta.mousePressEvent = lambda e, i=i: self.virar_carta(i)



    # esse def é chamado quando alguem clica em uma carta
    def virar_carta(self, i):
        # ele ignora o clique se a carta ja estar fixada ou se tem duas cartas viradas esperando verificação
        if self.estado_cartas[i] or len(self.cartas_reveladas) == 2:
            return
        
        # mostra a imagem da carta, marca ela como virada e adtciona o indice à lista
        self.cartas[i].setPixmap(QtGui.QPixmap(self.imagens[i]))
        self.estado_cartas[i] = True
        self.cartas_reveladas.append(i)

        # quando as cartas se viram ele adiciona o número de movimento, atualiza e chama verificar_par()
        if len(self.cartas_reveladas) == 2:
            self.movimentos += 1
            self.label_Movimentos.setText(f"Movimentos: {self.movimentos}")
            QtWidgets.QApplication.processEvents()
            QtCore.QTimer.singleShot(800, self.verificar_par)


    
    def verificar_par(self):
        # pega o indice das duas cartas viradas, se não forem iguais ela vira as cartas novamente, 
        # marca que elas estão disponiveis e limpa a lista de cartas viradas
        i1, i2 = self.cartas_reveladas
        if self.imagens[i1] != self.imagens[i2]:
            self.cartas[i1].setPixmap(QtGui.QPixmap("imagens/verso.png"))
            self.cartas[i2].setPixmap(QtGui.QPixmap("imagens/verso.png"))
            self.estado_cartas[i1] = False
            self.estado_cartas[i2] = False
        self.cartas_reveladas = []

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JogoMemoria()
    window.show()
    sys.exit(app.exec_())
