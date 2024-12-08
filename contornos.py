import cv2
from PyQt6.QtWidgets import QSlider, QSpinBox
from PyQt6.QtCore import Qt


class ContornosProcessor:
    def __init__(self, main_window):
        self.main_window = main_window

        self.imagemcontornada = None

        self.main_window.AplicarContorn.clicked.connect(lambda:
                                                        self.main_window.aplicar_edicao(self.imagemcontornada))

    def detect_draw_contours(self, image):
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

            # Encontrar contornos na imagem
            contours, _ = cv2.findContours(
                threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # RETR_TREE = Recupera todos os contornos e organiza em hierarquias
            # CHAIN_APPROX_SIMPLE = Remove todos os pontos redundantes

            for contour in contours:
                # Calcular a área e o perímetro do contorno
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                # True = Considera o contorno como fechado

                # Desenhar o contorno
                cv2.drawContours(image_copy, [
                    contour], -1, (self.main_window.BValue.value(), self.main_window.GValue.value(), self.main_window.RValue.value()), self.main_window.EspessuraValue.value())
                # -1 desenha todos, cor deles BGR, 2 espessura

            self.imagemcontornada = image_copy.copy()
            self.main_window.atualizar_imagem(image_copy)
