from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QGridLayout, QSpinBox, QVBoxLayout,
    QHBoxLayout, QPushButton
)
import sys
import numpy as np
import cv2


class KernelApp(QMainWindow):
    def __init__(self, mainwindow):
        super().__init__()

        self.main_window = mainwindow

        # Configurando a janela
        self.setWindowTitle('Kernel Customizado')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)

        self.imagemcustom = None
        self.kernel_values = None

        # aplica os efeitos de filtro a imagem
        self.main_window.AplicarCustom.clicked.connect(
            lambda: self.main_window.aplicar_edicao(self.imagemcustom))

        # # Rótulo e SpinBox para o tamanho do kernel
        # self.label = QLabel("Tamanho do kernel (ímpar maior que 1):")
        # self.top_layout.addWidget(self.label)

        # self.kernel_size_spinbox = QSpinBox()
        # self.kernel_size_spinbox.setRange(3, 99)  # Aceita valores ímpares maiores que 1
        # self.kernel_size_spinbox.setSingleStep(2)  # Passo de 2 para garantir que seja ímpar
        # self.kernel_size_spinbox.setValue(3)  # Valor inicial de 3x3
        # self.top_layout.addWidget(self.kernel_size_spinbox)

        # # Botão para gerar os SpinBoxes
        # self.generate_button = QPushButton("Gerar Kernel")
        # self.generate_button.clicked.connect(self.generate_spinboxes)
        # self.top_layout.addWidget(self.generate_button)

        # Layout para os SpinBoxes
        self.kernel_layout = QGridLayout()
        self.main_layout.addLayout(self.kernel_layout)

        # Variável para armazenar os spinboxes
        self.spinboxes = []

        # Chamar função para gerar os SpinBoxes inicialmente
        # self.generate_spinboxes()

    def closeEvent(self, event):
        # Em vez de fechar, vamos apenas esconder a janela
        self.setHidden(True)
        # Prevenir o fechamento real da janela
        event.ignore()

    def generate_spinboxes(self, value):
        if value % 2 == 0:
            value = value + 1
        # Limpar SpinBoxes anteriores
        for i in reversed(range(self.kernel_layout.count())):
            widget = self.kernel_layout.itemAt(i).widget()
            if widget:
                # Remove o widget corretamente do layout
                widget.setParent(None)

        self.spinboxes = []

        # Remover o botão se já existir
        if hasattr(self, 'button_layout'):
            for i in reversed(range(self.button_layout.count())):
                widget = self.button_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()  # Remove o widget corretamente do layout
            self.main_layout.removeItem(self.button_layout)
            self.button_layout.deleteLater()

        # Tamanho do kernel (valor da SpinBox)
        kernel_size = value  # self.kernel_size_spinbox.value()

        # Gerar SpinBoxes de acordo com o tamanho do kernel
        for i in range(kernel_size):
            row = []
            for j in range(kernel_size):
                spinbox = QSpinBox()
                # Definir o intervalo de valores do SpinBox
                spinbox.setRange(-10, 10)
                # Definir um tamanho fixo para os SpinBoxes
                spinbox.setFixedSize(50, 30)
                self.kernel_layout.addWidget(spinbox, i, j)
                row.append(spinbox)
            self.spinboxes.append(row)

        # Adicionando um botão abaixo dos SpinBoxes
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # Criar o botão e adicionar ao layout
        self.ButtonPronto = QPushButton("Pronto")
        self.button_layout.addWidget(self.ButtonPronto)

        # Atualizar o layout e ajustar o tamanho da janela
        self.central_widget.adjustSize()
        self.adjustSize()

        self.ButtonPronto.clicked.connect(self.on_button_click)

    def get_kernel_values(self):
        # Obtém o número de linhas/colunas do kernel
        kernel_size = len(self.spinboxes)

        # Cria uma matriz para armazenar os valores
        kernel_values = np.zeros((kernel_size, kernel_size), dtype=np.int32)

        # Itera sobre as spinboxes para coletar os valores
        for i in range(kernel_size):
            for j in range(kernel_size):
                spinbox = self.spinboxes[i][j]
                kernel_values[i, j] = spinbox.value()

        return kernel_values

    def on_button_click(self):
        # Obtém os valores do kernel
        self.kernel_values = np.array(self.get_kernel_values())
        self.Custom_Filter(self.main_window.imagem_editada)
        self.main_window.atualizar_imagem(self.imagemcustom)
        self.hide()

    def Custom_Filter(self, image):
        self.imagemcustom = cv2.filter2D(image, -1, self.kernel_values)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KernelApp()
    window.show()
    sys.exit(app.exec())
