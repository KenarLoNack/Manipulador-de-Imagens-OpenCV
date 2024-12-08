import cv2
from PyQt6.QtWidgets import QSlider, QSpinBox
from PyQt6.QtCore import Qt


class Passabaixa:
    def __init__(self, main_window):
        self.main_window = main_window

        self.imagemnova = None

        self.main_window.AplicarBaixa.clicked.connect(self.aplicarfiltros)

    def blur(self, value, imagem):
        if imagem is not None:
            # Filtro Média
            self.imagemnova = cv2.blur(imagem, (value, value))
            self.main_window.atualizar_imagem(self.imagemnova)

    def gaussianblur(self, value, imagem):
        if imagem is not None:
            # Filtro Média
            self.imagemnova = cv2.GaussianBlur(imagem, (value, value), 0)
            self.main_window.atualizar_imagem(self.imagemnova)

    def medianblur(self, value, imagem):
        if imagem is not None:
            # Filtro Média
            self.imagemnova = cv2.medianBlur(imagem,  value)
            self.main_window.atualizar_imagem(self.imagemnova)

    def aplicarfiltros(self):
        if self.imagemnova is not None:
            self.main_window.aplicar_edicao(self.imagemnova)
