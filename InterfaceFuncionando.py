import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

from Interface import Ui_MainWindow  # Importe a classe gerada pelo pyuic6
from OrigInterface import Ui_ImagemOriginal

# Variável global para armazenar o caminho do arquivo
global_image_path = None


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Conectar o evento de roda do mouse diretamente ao GraphicEdit
        self.GraphicEdit.wheelEvent = self.wheelEvent

        # Chamar a função para escolher um arquivo logo na inicialização
        global global_image_path
        global_image_path = self.escolher_arquivo()

        # Se nenhum arquivo for escolhido, fechar o programa
        if not global_image_path:
            print("Nenhum arquivo escolhido. Fechando o programa.")
            sys.exit()

        # Exibir a imagem no QGraphicsView existente após configurar a interface
        self.exibir_imagem_editing(global_image_path)

        # Atributo para armazenar a instância da segunda janela
        self.second_window = None

        # Conectar o botão à função que abre a segunda janela
        self.actionImgOriginal.triggered.connect(self.abrir_segunda_janela)

        # Configurar as barras de rolagem para aparecer quando necessário
        self.GraphicEdit.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.GraphicEdit.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def escolher_arquivo(self):
        # Abrir o diálogo para o usuário escolher um arquivo de imagem
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            'Escolher Arquivo de Imagem',
            '',
            'Imagens (*.png *.jpg *.jpeg *.bmp)'
        )

        if arquivo:
            print(f"Arquivo escolhido: {arquivo}")
            return arquivo
        else:
            print("Nenhum arquivo foi escolhido.")
            return None

    def exibir_imagem_editing(self, caminho_imagem):
        ImagemEditing = cv2.imread(caminho_imagem)
        altura, largura, canais = ImagemEditing.shape
        self.InfoEdit.setText(
            f"Tamanho: ({largura}x{altura}) Canais: {canais}")
        # Criar um QPixmap com a imagem
        pixmap = QPixmap(caminho_imagem)

        # Criar e configurar a QGraphicsScene
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        # Definir a cena no QGraphicsView existente
        self.GraphicEdit.setScene(scene)

        # Ajustar o QGraphicsView para se ajustar à imagem
        self.GraphicEdit.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.GraphicEdit.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform)
        self.GraphicEdit.maximumViewportSize()

    def wheelEvent(self, event):
        # Verificar os modificadores de teclado corretamente
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Zoom com a roda do mouse
            scale_factor = 1.2
            if event.angleDelta().y() < 0:
                scale_factor = 1.0 / scale_factor
            self.GraphicEdit.scale(scale_factor, scale_factor)
        elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            # Scroll horizontal com a roda do mouse
            if self.GraphicEdit.horizontalScrollBar().isVisible():
                scroll_bar = self.GraphicEdit.horizontalScrollBar()
                scroll_bar.setValue(int(scroll_bar.value() -
                                    event.angleDelta().y() / 8))
        else:
            # Scroll vertical com a roda do mouse
            if self.GraphicEdit.verticalScrollBar().isVisible():
                scroll_bar = self.GraphicEdit.verticalScrollBar()
                scroll_bar.setValue(int(scroll_bar.value() +
                                    event.angleDelta().y() / 8))

    def abrir_segunda_janela(self):
        if self.second_window is None or not self.second_window.isVisible():
            self.second_window = ImagemOriginal()

            # Exibir a imagem na segunda janela, se a imagem foi carregada
            if global_image_path:
                self.second_window.exibir_imagem_original(global_image_path)

            # Mostrar a segunda janela sobre a janela principal
            self.second_window.show()
            self.second_window.raise_()
            self.second_window.activateWindow()
        else:
            # Se a janela ainda está aberta, apenas trazê-la para o foco
            self.second_window.raise_()
            self.second_window.activateWindow()

    def iniciar_segunda_janela(self):
        # Criar e mostrar a segunda janela após a janela principal ser exibida
        if global_image_path:
            self.second_window = ImagemOriginal()
            self.second_window.exibir_imagem_original(global_image_path)
            self.second_window.show()
            self.second_window.raise_()
            self.second_window.activateWindow()


class ImagemOriginal(QMainWindow, Ui_ImagemOriginal):
    def __init__(self):
        super(ImagemOriginal, self).__init__()
        self.setupUi(self)

        # Conectar o evento de roda do mouse diretamente ao GraphicOrig
        self.GraphicOrig.wheelEvent = self.wheelEvent

        # Configurar as barras de rolagem para aparecer quando necessário
        self.GraphicOrig.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.GraphicOrig.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def exibir_imagem_original(self, caminho_imagem):
        ImagemOriginal = cv2.imread(caminho_imagem)
        altura, largura, canais = ImagemOriginal.shape
        self.InfoOrig.setText(
            f"Tamanho: ({largura}x{altura}) Canais: {canais}")
        # Criar um QPixmap com a imagem
        pixmap = QPixmap(caminho_imagem)

        # Criar e configurar a QGraphicsScene
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        # Definir a cena no QGraphicsView existente
        self.GraphicOrig.setScene(scene)

        # Ajustar o QGraphicsView para se ajustar à imagem
        self.GraphicOrig.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.GraphicOrig.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform)
        self.GraphicOrig.maximumViewportSize()

    def wheelEvent(self, event):
        # Verificar os modificadores de teclado corretamente
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Zoom com a roda do mouse
            scale_factor = 1.2
            if event.angleDelta().y() < 0:
                scale_factor = 1.0 / scale_factor
            self.GraphicOrig.scale(scale_factor, scale_factor)
        elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            # Scroll horizontal com a roda do mouse
            if self.GraphicOrig.horizontalScrollBar().isVisible():
                scroll_bar = self.GraphicOrig.horizontalScrollBar()
                scroll_bar.setValue(int(scroll_bar.value() -
                                    event.angleDelta().y() / 8))
        else:
            # Scroll vertical com a roda do mouse
            if self.GraphicOrig.verticalScrollBar().isVisible():
                scroll_bar = self.GraphicOrig.verticalScrollBar()
                scroll_bar.setValue(int(scroll_bar.value() +
                                    event.angleDelta().y() / 8))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Criar e mostrar a janela principal
    main_window = MainWindow()
    main_window.show()

    # Criar a segunda janela e garantir que seja exibida corretamente sobre a janela principal
    if global_image_path:
        main_window.iniciar_segunda_janela()

    sys.exit(app.exec())
