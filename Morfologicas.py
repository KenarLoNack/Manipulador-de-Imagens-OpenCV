import cv2
from PyQt6.QtWidgets import QSlider, QSpinBox
from PyQt6.QtCore import Qt
import numpy as np


class OPMorf:
    def __init__(self, main_window):
        self.main_window = main_window

        self.imagethres = None
        self.imageprocessada = None

        # operacao morfologica
        self.main_window.ButtonErosao.clicked.connect(
            lambda: self.main_window.kernel_impar(self.main_window.KernelValueMorf))
        self.main_window.ButtonAbertura.clicked.connect(
            lambda: self.main_window.kernel_impar(self.main_window.KernelValueMorf))
        self.main_window.ButtonGradiente.clicked.connect(
            lambda: self.main_window.kernel_impar(self.main_window.KernelValueMorf))
        self.main_window.ButtonFechamento.clicked.connect(
            lambda: self.main_window.kernel_impar(self.main_window.KernelValueMorf))
        self.main_window.ButtonDilatacao.clicked.connect(
            lambda: self.main_window.kernel_impar(self.main_window.KernelValueMorf))

        self.main_window.ButtonErosao.clicked.connect(
            lambda: self.preparaimg(self.main_window.imagem_editada))
        self.main_window.ButtonAbertura.clicked.connect(
            lambda: self.preparaimg(self.main_window.imagem_editada))
        self.main_window.ButtonGradiente.clicked.connect(
            lambda: self.preparaimg(self.main_window.imagem_editada))
        self.main_window.ButtonFechamento.clicked.connect(
            lambda: self.preparaimg(self.main_window.imagem_editada))
        self.main_window.ButtonDilatacao.clicked.connect(
            lambda: self.preparaimg(self.main_window.imagem_editada))

        self.main_window.ButtonErosao.clicked.connect(
            lambda: self.erosao(self.main_window.KernelValueMorf.value(), self.imagethres))
        self.main_window.ButtonAbertura.clicked.connect(
            lambda: self.abertura(self.main_window.KernelValueMorf.value(), self.imagethres))
        self.main_window.ButtonGradiente.clicked.connect(
            lambda: self.gradiente(self.main_window.KernelValueMorf.value(), self.imagethres))
        self.main_window.ButtonFechamento.clicked.connect(
            lambda: self.fechamento(self.main_window.KernelValueMorf.value(), self.imagethres))
        self.main_window.ButtonDilatacao.clicked.connect(
            lambda: self.dilatacao(self.main_window.KernelValueMorf.value(), self.imagethres))

        self.main_window.AplicarMorf.clicked.connect(
            lambda: self.main_window.aplicar_edicao(self.imageprocessada))

    def preparaimg(self, image):
        if image is not None:
            image_copy = image.copy()
            if len(image.shape) == 3:
                # Imagem em cinza para binarizar
                gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = image_copy.copy()
            # Binarização (thresholding)
            _, threshold_img = cv2.threshold(
                gray_image, 127, 255, cv2.THRESH_BINARY)
            self.imagethres = threshold_img.copy()

    def erosao(self, value, image):
        kernel = np.ones((value, value))
        if image is not None:
            self.imageprocessada = cv2.erode(
                image, kernel, iterations=1)

            self.main_window.atualizar_imagem(self.imageprocessada)

    def abertura(self, value, image):
        kernel = np.ones((value, value))
        if image is not None:
            self.imageprocessada = cv2.morphologyEx(
                image, cv2.MORPH_OPEN, kernel)
            self.main_window.atualizar_imagem(self.imageprocessada)

    def dilatacao(self, value, image):
        kernel = np.ones((value, value))
        if image is not None:
            self.imageprocessada = cv2.dilate(
                image, kernel, iterations=1)
            self.main_window.atualizar_imagem(self.imageprocessada)

    def fechamento(self, value, image):
        kernel = np.ones((value, value))
        if image is not None:
            self.imageprocessada = cv2.morphologyEx(
                image, cv2.MORPH_CLOSE, kernel)
            self.main_window.atualizar_imagem(self.imageprocessada)

    def gradiente(self, value, image):
        kernel = np.ones((value, value))
        if image is not None:
            self.imageprocessada = cv2.morphologyEx(
                image, cv2.MORPH_GRADIENT, kernel)
            self.main_window.atualizar_imagem(self.imageprocessada)
