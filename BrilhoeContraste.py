import cv2
import numpy as np
from PyQt6.QtWidgets import QSlider, QSpinBox
from PyQt6.QtCore import Qt


class ImageProcessor:
    def __init__(self, main_window):
        self.main_window = main_window

        # Configurar sliders e spinboxes
        # Definir intervalo do slider de brilho
        self.main_window.BrilhoSlider_4.setRange(-127, 127)
        self.main_window.BrilhoSlider_4.setValue(0)
        # Definir intervalo do slider de contraste
        self.main_window.ConstrasteSlider_4.setRange(1, 30)
        # Definir intervalo do spinbox de contraste
        self.main_window.ContrasteValue.setRange(0.1, 3)
        self.main_window.ContrasteValue.setValue(1)
        # Definir intervalo do spinbox de brilho
        self.main_window.BrilhoValue.setRange(-127, 127)
        self.main_window.BrilhoValue.setValue(0)

        # Conectar sliders e spinboxes
        self.main_window.BrilhoSlider_4.valueChanged.connect(
            self.atualizar_spin_brilho)
        self.main_window.ConstrasteSlider_4.valueChanged.connect(
            self.atualizar_spinbox_contraste)
        self.main_window.BrilhoValue.valueChanged.connect(
            self.atualizar_slider_brilho)
        self.main_window.ContrasteValue.valueChanged.connect(
            self.atualizar_slider_contraste)

        self.main_window.AplicarBeC.clicked.connect(
            lambda: self.on_aplicar_clicked())

    def atualizar_spin_brilho(self, valor):
        # Garantir que o valor esteja correto
        self.main_window.BrilhoValue.setValue(valor)
        self.aplicar_efeitos()

    def atualizar_spinbox_contraste(self, valor):
        # Converter o valor do slider para o intervalo do spinbox
        spinbox_valor = valor / 10.0
        if self.main_window.ContrasteValue.value() != spinbox_valor:
            self.main_window.ContrasteValue.setValue(spinbox_valor)
            self.aplicar_efeitos()

    def atualizar_slider_brilho(self, valor):
        self.main_window.BrilhoSlider_4.setValue(valor)
        self.aplicar_efeitos()

    def atualizar_slider_contraste(self, valor):
        # Converter o valor do spinbox para o intervalo do slider
        slider_valor = int(round(valor * 10))
        if self.main_window.ConstrasteSlider_4.value() != slider_valor:
            self.main_window.ConstrasteSlider_4.setValue(slider_valor)
            self.aplicar_efeitos()

    def aplicar_efeitos(self):
        brilho = self.main_window.BrilhoValue.value()
        contraste = self.main_window.ContrasteValue.value()

        if self.main_window.imagem_editada is not None:
            imagem_ajustada = cv2.convertScaleAbs(
                self.main_window.imagem_editada, alpha=contraste, beta=brilho)
            self.main_window.atualizar_imagem(imagem_ajustada)

    def on_aplicar_clicked(self):
        if self.main_window.ContrasteValue.value() != 1 or self.main_window.BrilhoValue.value() != 0:
            imagem_ajustada = cv2.convertScaleAbs(
                self.main_window.imagem_editada, alpha=self.main_window.ContrasteValue.value(), beta=self.main_window.BrilhoValue.value()
            )
            # cv2.imshow("imagemajust", imagem_ajustada)
            if not np.array_equal(self.main_window.imagem_editada, imagem_ajustada):
                self.main_window.aplicar_edicao(imagem_ajustada)
