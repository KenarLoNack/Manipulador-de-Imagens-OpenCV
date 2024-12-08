import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtCore import Qt
from io import BytesIO
from HistogramaInterface import Ui_Histograma


class ViewInterface(QMainWindow, Ui_Histograma):
    def __init__(self, main_window):
        super(ViewInterface, self).__init__()
        self.setupUi(self)
        self.main_window = main_window

        # Conectar o evento de roda do mouse diretamente ao GraphicHisto
        self.GraphicHisto.wheelEvent = self.wheelEvent
        self.imagemequalizada = None
        self.grafqualizado = None

        self.ButtonEqualizar.clicked.connect(self.equalizehistogram)

    def equalizehistogram(self):
        # Exibir o QPixmap no QGraphicsView
        self.exibir_imagem_histograma(self.grafqualizado)
        self.main_window.aplicar_edicao(self.imagemequalizada.copy())

    def plot_to_pixmap(self, image):
        self.image = image.copy()
        self.grafqualizado = self.generate_equalized_histogram(image)

        # Gerar o histograma normal
        qimage = self.generate_histogram(image)

        # Exibir o QPixmap no QGraphicsView
        self.exibir_imagem_histograma(QPixmap(qimage))

    def generate_histogram(self, image):
        # Função para gerar o histograma normal
        if len(image.shape) == 3:
            # Calcular o histograma para cada canal
            colors = ('b', 'g', 'r')
            fig, ax = plt.subplots()
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                ax.plot(hist, color=color)
            ax.set_title('Histograma de Cores')
        else:
            # Calcular o histograma para cinza
            fig, ax = plt.subplots()
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            ax.plot(hist)
            ax.set_title('Histograma de Cinza')

        # Salvar a imagem do gráfico no buffer
        buf = BytesIO()
        fig.savefig(buf, format='png')  # Salvar diretamente como PNG
        buf.seek(0)

        # Converter o buffer PNG para QImage
        qimage = QImage()
        qimage.loadFromData(buf.getvalue())

        # Fechar a figura do matplotlib para liberar memória
        plt.close(fig)

        return qimage

    def generate_equalized_histogram(self, image):
        # Função para gerar o histograma equalizado
        if len(image.shape) == 3:
            # Separar os canais (B, G, R) e equalizar
            b, g, r = cv2.split(image)
            equalized_b = cv2.equalizeHist(b)
            equalized_g = cv2.equalizeHist(g)
            equalized_r = cv2.equalizeHist(r)

            equalized_image = cv2.merge(
                [equalized_b, equalized_g, equalized_r])
            colors = ('b', 'g', 'r')
            fig, ax = plt.subplots()
            for i, color in enumerate(colors):
                histeq = cv2.calcHist([equalized_image], [
                                      i], None, [256], [0, 256])
                ax.plot(histeq, color=color)
            ax.set_title('Histograma Equalizado de Cores')
        else:
            # Equalizar imagem cinza
            equalized_image = cv2.equalizeHist(image)
            fig, ax = plt.subplots()
            histeq = cv2.calcHist([equalized_image], [0],
                                  None, [256], [0, 256])
            ax.plot(histeq)
            ax.set_title('Histograma Equalizado de Cinza')

        # Salvar a imagem do gráfico no buffer
        buf = BytesIO()
        fig.savefig(buf, format='png')  # Salvar diretamente como PNG
        buf.seek(0)

        # Converter o buffer PNG para QImage
        qimageeq = QImage()
        qimageeq.loadFromData(buf.getvalue())

        # Fechar a figura do matplotlib para liberar memória
        plt.close(fig)
        self.imagemequalizada = equalized_image.copy()
        return QPixmap(qimageeq)

    def exibir_imagem_histograma(self, imagem):
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(imagem)
        scene.addItem(pixmap_item)

        self.GraphicHisto.setScene(scene)
        self.GraphicHisto.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.GraphicHisto.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform)
        self.GraphicHisto.fitInView(
            scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            scale_factor = 1.2
            if event.angleDelta().y() < 0:
                scale_factor = 1.0 / scale_factor
            self.GraphicHisto.scale(scale_factor, scale_factor)
        elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            if self.GraphicHisto.horizontalScrollBar().isVisible():
                scroll_bar = self.GraphicHisto.horizontalScrollBar()
                scroll_bar.setValue(
                    int(scroll_bar.value() - event.angleDelta().y() / 8))
        else:
            if self.GraphicHisto.verticalScrollBar().isVisible():
                scroll_bar = self.GraphicHisto.verticalScrollBar()
                scroll_bar.setValue(
                    int(scroll_bar.value() + event.angleDelta().y() / 8))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ViewInterface()
    window.show()
    sys.exit(app.exec())
