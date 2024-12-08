import cv2
import numpy as np
from SobelInterface import Ui_SobelWindow
from PyQt6.QtWidgets import QSlider, QSpinBox
from PyQt6.QtCore import Qt

from SobelWindow import SobelInterface


class PassaAlta:
    def __init__(self, main_window):
        self.main_window = main_window

        self.imagemnova = None
        self.sobelwindow1 = None
        self.sobelwindow2 = None
        self.sobelx = None
        self.sobely = None
        self.imagemaplicada = 0

        self.main_window.AplicarAlta.clicked.connect(self.salvarfiltros)

    def laplace(self, imagem):
        if imagem is not None:
            try:
                ddepth = self.main_window.ComboAlta.currentData()

                # Aplicar o filtro Laplaciano
                self.imagemnova = cv2.Laplacian(imagem, ddepth)
                self.main_window.atualizar_imagem(self.imagemnova)

            except Exception as e:
                print(f"Erro ao aplicar o filtro Laplaciano: {e}")
                imagemconvertida = self.converterbits(imagem)
                self.laplace(imagemconvertida)

    def converterbits(self, imagem):
        ddepth = self.main_window.ComboAlta.currentData()
        tipoimage = imagem.dtype

        imagemconvertida = None

        # Mapear ddepth para tipo NumPy
        if ddepth == cv2.CV_8U:
            target_dtype = np.uint8
        elif ddepth == cv2.CV_16S:
            target_dtype = np.int16
        elif ddepth == cv2.CV_32F:
            target_dtype = np.float32
        elif ddepth == cv2.CV_64F:
            target_dtype = np.float64
        else:
            print("ddepth não reconhecido")
            return imagem  # Retorna a imagem original se o ddepth não for reconhecido

        # Verificar se é necessário converter
        if tipoimage != target_dtype:
            if ddepth == cv2.CV_8U:
                imagemconvertida = cv2.convertScaleAbs(imagem)
            elif ddepth == cv2.CV_16S:
                imagemconvertida = np.int16(imagem)
            elif ddepth == cv2.CV_32F:
                imagemconvertida = np.float32(imagem)
            elif ddepth == cv2.CV_64F:
                imagemconvertida = np.float64(imagem)
        else:
            imagemconvertida = imagem  # Se o tipo já for o desejado, não precisa converter

        return imagemconvertida

    def sobel(self, value, imagem):
        if imagem is not None:
            try:
                ddepth = self.main_window.ComboAlta.currentData()
                # Filtros Sobel (detecção de bordas horizontais e verticais)
                self.sobelx = cv2.Sobel(imagem, ddepth, 1, 0, ksize=value)
                self.sobely = cv2.Sobel(imagem, ddepth, 0, 1, ksize=value)

                if self.sobelwindow1 is None:
                    self.sobelwindow1 = SobelInterface()
                    self.sobelwindow1.move(400, 200)
                else:
                    self.sobelwindow1.raise_()

                self.sobelwindow1.SobelLabel.setText("Sobel X")
                self.sobelwindow1.show()
                self.sobelwindow1.raise_()
                self.sobelwindow1.atualizar_imagem(self.sobelx)

                if self.sobelwindow2 is None:
                    self.sobelwindow2 = SobelInterface()
                    self.sobelwindow2.move(1000, 200)
                else:
                    self.sobelwindow2.raise_()

                self.sobelwindow2.SobelLabel.setText("Sobel Y")
                self.sobelwindow2.show()
                self.sobelwindow2.raise_()
                self.sobelwindow2.atualizar_imagem(self.sobely)

                self.sobelwindow1.AplicarSobel.clicked.connect(
                    lambda: self.alterada(0))
                self.sobelwindow2.AplicarSobel.clicked.connect(
                    lambda: self.alterada(1))

            except Exception as e:
                print(f"Erro ao aplicar o filtro Sobel: {e}")
                imagemconvertida = self.converterbits(imagem)
                self.sobel(value, imagemconvertida)

    def alterada(self, value):
        self.imagemaplicada = value
        self.aplicarfiltros()

    def salvarfiltros(self):
        if self.imagemnova is not None:
            self.main_window.aplicar_edicao(self.imagemnova)
        elif self.sobelx is not None and self.imagemaplicada == 0:
            self.main_window.aplicar_edicao(self.sobelx)
        elif self.sobely is not None and self.imagemaplicada == 1:
            self.main_window.aplicar_edicao(self.sobely)

    def aplicarfiltros(self):
        if self.imagemaplicada is not None and self.sobelx is not None and self.sobely is not None:
            if self.imagemaplicada == 0:
                self.main_window.atualizar_imagem(self.sobelx)
            else:
                self.main_window.atualizar_imagem(self.sobely)
        if self.sobelwindow1 is not None and self.sobelwindow2 is not None:
            self.sobelwindow1.close()
            self.sobelwindow2.close()
