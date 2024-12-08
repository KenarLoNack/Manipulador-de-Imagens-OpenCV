import sys
import numpy as np
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from SobelInterface import Ui_SobelWindow


class SobelInterface(QMainWindow, Ui_SobelWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Conectar o evento de roda do mouse diretamente ao Graphic
        self.GraphicViewSobel.wheelEvent = self.wheelEvent

    def atualizar_imagem(self, imagem):
        # Verificar o tipo de profundidade da imagem
        if imagem.dtype == np.float64:
            # Converter para 8 bits se for CV_64F
            imagem = cv2.convertScaleAbs(imagem)
        elif imagem.dtype == np.float32:
            # Converter para 8 bits se for CV_32F
            imagem = cv2.convertScaleAbs(imagem)
        elif imagem.dtype == np.int16:
            # Converter para 8 bits se for CV_16S
            imagem = cv2.convertScaleAbs(imagem)

        # Garantir que a imagem esteja no formato esperado (8-bit ou 16-bit)
        if imagem.ndim == 2:
            # Imagem em escala de cinza
            imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_GRAY2RGB)
        elif imagem.ndim == 3 and imagem.shape[2] == 3:
            # Imagem colorida (BGR para RGB)
            imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        else:
            raise ValueError("Formato de imagem não suportado")

        altura, largura, canais = imagem_rgb.shape
        bytes_per_line = canais * largura

        # Converte a imagem para o formato QImage
        qimage = QImage(imagem_rgb.data, largura, altura,
                        bytes_per_line, QImage.Format.Format_RGB888)

        # Converte o QImage para QPixmap
        pixmap = QPixmap.fromImage(qimage)

        # Exibe a imagem no QGraphicsView
        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.GraphicViewSobel.setScene(scene)

        # Ajustar o QGraphicsView para encaixar a imagem
        self.GraphicViewSobel.fitInView(
            scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event):
        # Verificar os modificadores de teclado corretamente
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Zoom com a roda do mouse
            scale_factor = 1.2
            if event.angleDelta().y() < 0:
                scale_factor = 1.0 / scale_factor
            self.GraphicViewSobel.scale(scale_factor, scale_factor)
        elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            # Scroll horizontal com a roda do mouse
            if self.GraphicViewSobel.horizontalScrollBar().isVisible():
                scroll_bar = self.GraphicViewSobel.horizontalScrollBar()
                scroll_bar.setValue(int(scroll_bar.value() -
                                        event.angleDelta().y() / 8))
        else:
            # Scroll vertical com a roda do mouse
            if self.GraphicViewSobel.verticalScrollBar().isVisible():
                scroll_bar = self.GraphicViewSobel.verticalScrollBar()
                scroll_bar.setValue(int(scroll_bar.value() +
                                        event.angleDelta().y() / 8))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SobelInterface()
    window.show()
    sys.exit(app.exec())
