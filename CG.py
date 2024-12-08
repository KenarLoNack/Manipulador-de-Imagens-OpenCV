import sys
import cv2
import mimetypes
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QPainter, QImage, QIcon
from PyQt6.QtCore import Qt, QTimer

# importando interfaces e extensoes da tela principal
from Interface import Ui_MainWindow
from OrigInterface import Ui_ImagemOriginal
from BrilhoeContraste import ImageProcessor
from CustomFilter import KernelApp
from HistogramaWindow import ViewInterface
from PassaBaixa import Passabaixa
from PassaAlta import PassaAlta
from contornos import ContornosProcessor
from savemanager import ImageUndoRedoManager
from Morfologicas import OPMorf

# Variável global para armazenar o caminho do arquivo
global_image_path = None


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('Icons/logoeditor.png'))

        self.undo_redo_manager = ImageUndoRedoManager(
            max_undos=5)  # Limita a 5 undos

        # inicializa comobox
        self.ComboAlta.addItem("8-bit Unsigned (CV_8U)", cv2.CV_8U)
        self.ComboAlta.addItem("16-bit Signed (CV_16S)", cv2.CV_16S)
        self.ComboAlta.addItem("32-bit Float (CV_32F)", cv2.CV_32F)
        self.ComboAlta.addItem("64-bit Float (CV_64F)", cv2.CV_64F)

        # Configurar o ImageProcessor
        self.BrilhoeContraste = ImageProcessor(self)
        self.passabaixa = Passabaixa(self)
        self.passaalta = PassaAlta(self)
        self.contorno = ContornosProcessor(self)
        self.OPMorf = OPMorf(self)
        self.CustomFilter = None

        # Conectar o evento de roda do mouse diretamente ao GraphicEdit
        self.GraphicEdit.wheelEvent = self.wheelEvent
        # Atributo para armazenar a instância da segunda janela

        self.second_window = ImagemOriginal()
        self.second_window.setHidden(False)

        # imagem editada em cv2
        self.imagemOriginal = None
        self.imagem_editada = None
        self.imagem_terminada = None
        self.histograma = None

        # Chamar a função para escolher um arquivo logo na inicialização
        # self.escolher_arquivo()

        # Se nenhum arquivo for escolhido, fechar o programa
        # if not global_image_path:
        #     print("Nenhum arquivo escolhido. Fechando o programa.")
        #     sys.exit()

        # Exibir a imagem no QGraphicsView existente após configurar a interface
        # self.exibir_imagem_editing(global_image_path)

        # Inicializar a variável de imagem
        self.image_path = None
        self.updating_value = False

        # Conectar o botão à função que abre a segunda janela
        self.actionImgOriginal.triggered.connect(self.abrir_segunda_janela)

        # botao de escolher arquivo
        self.actionAbrir_Arquivo.triggered.connect(self.escolher_arquivo)

        # if global_image_path is not None or self.imagem_editada is not None:
        self.actionSalvar.triggered.connect(self.salvar_arquivo)
        self.actionHistogram.triggered.connect(self.abrir_histograma)

        # botoes de desfazer e refazer
        self.actionDesfazer.triggered.connect(self.undo)
        self.actionRefazer.triggered.connect(self.redo)

        # botao para mudar para tons de cinza
        self.actionConverter_em_Cinza.triggered.connect(
            lambda: self.cinzaconverter())

        # Abrir custom kernel
        self.ButtonCustomize.clicked.connect(
            lambda: self.kernel_impar(self.KernelValueCustom_4))
        self.ButtonCustomize.clicked.connect(self.abrir_custom_filter)

        # botoes de Passa baixa
        self.ButtonMedia_4.clicked.connect(
            lambda: self.kernel_impar(self.KernelValueBaixa_4))

        self.ButtonMediana_4.clicked.connect(
            lambda: self.kernel_impar(self.KernelValueBaixa_4))

        self.ButtonGaus_4.clicked.connect(
            lambda: self.kernel_impar(self.KernelValueBaixa_4))

        self.ButtonMedia_4.clicked.connect(lambda: self.passabaixa.blur(
            self.KernelValueBaixa_4.value(), self.imagem_editada))

        self.ButtonMediana_4.clicked.connect(lambda: self.passabaixa.medianblur(
            self.KernelValueBaixa_4.value(), self.imagem_editada))

        self.ButtonGaus_4.clicked.connect(lambda: self.passabaixa.gaussianblur(
            self.KernelValueBaixa_4.value(), self.imagem_editada))

        # botoes de passa alta
        self.ButtonLaplace_4.clicked.connect(
            lambda: self.kernel_impar(self.KernelValueAlta_4))

        self.ButtonSobel_4.clicked.connect(
            lambda: self.kernel_impar(self.KernelValueAlta_4))

        self.ButtonLaplace_4.clicked.connect(
            lambda: self.passaalta.laplace(self.imagem_editada))

        self.ButtonSobel_4.clicked.connect(lambda: self.passaalta.sobel(
            self.KernelValueBaixa_4.value(), self.imagem_editada))

        # deteccao de contornos
        self.ButtonDetec_4.clicked.connect(
            lambda: self.contorno.detect_draw_contours(self.imagem_editada))

        # Configurar as barras de rolagem para aparecer quando necessário
        self.GraphicEdit.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.GraphicEdit.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Exibir a segunda janela após a construção da principal
        QTimer.singleShot(0, self.abrir_segunda_janela)

    def undo(self):
        # Tenta desfazer e atualiza a imagem
        imagem_desfeita = self.undo_redo_manager.undo()
        if imagem_desfeita is not None:
            self.imagem_editada = imagem_desfeita.copy()
            # Atualiza o QGraphicsView com a imagem desfeita
            self.atualizar_imagem(self.imagem_editada)

    def redo(self):
        # Tenta refazer e atualiza a imagem
        imagem_refeita = self.undo_redo_manager.redo()
        if imagem_refeita is not None:
            self.imagem_editada = imagem_refeita.copy()
            # Atualiza o QGraphicsView com a imagem refeita
            self.atualizar_imagem(self.imagem_editada)

    def abrir_histograma(self):
        if self.imagem_editada is not None:
            if self.histograma is None:
                self.histograma = ViewInterface(self)
            self.histograma.show()
            self.histograma.raise_()
            self.histograma.plot_to_pixmap(self.imagem_editada)

    def kernel_impar(self, spinbox):

        current_value = spinbox.value()

        # Ajustar o valor conforme a condição
        if current_value % 2 == 0 and current_value != 0:
            spinbox.setValue(current_value + 1)
        elif current_value == 0 or current_value == 1:
            spinbox.setValue(3)

    def abrir_custom_filter(self):

        # if self.KernelValueCustom_4.changeEvent() and self.KernelValueCustom_4.value() % 2 == 0:
        #     self.KernelValueCustom_4.setValue(
        #         self.KernelValueCustom_4.value()+1)

        customkernelvalue = self.KernelValueCustom_4.value()

        # Método para abrir o filtro customizado em uma nova janela.
        if self.CustomFilter is None:  # Verificar se a janela do KernelApp ainda não foi criada
            # Cria a nova janela do filtro customizado
            self.CustomFilter = KernelApp(self)
        self.CustomFilter.generate_spinboxes(customkernelvalue)
        self.CustomFilter.show()
        self.CustomFilter.raise_()  # Mostra a janela do filtro customizado

    def closeEvent(self, event):
        # Fechar a segunda janela quando a principal for fechada
        if self.second_window:
            self.second_window.close()
        if self.CustomFilter:
            self.CustomFilter.close()
        if self.histograma:
            self.histograma.close()
        if self.passaalta.sobelwindow1:
            self.passaalta.sobelwindow1.close()
        if self.passaalta.sobelwindow2:
            self.passaalta.sobelwindow2.close()

        event.accept()  # Continuar com o fechamento da janela principal

    def cinzaconverter(self):
        if self.imagem_editada is not None and len(self.imagem_editada.shape) == 3:
            self.imagem_editada = cv2.cvtColor(
                self.imagem_editada, cv2.COLOR_BGR2GRAY)
            self.aplicar_edicao(self.imagem_editada)

    def resetsliders(self):
        self.BrilhoSlider_4.setValue(0)
        self.ConstrasteSlider_4.setValue(10)
        self.ContrasteValue.setValue(1)
        self.BrilhoValue.setValue(0)

    def escolher_arquivo(self):

        # Abrir o diálogo para o usuário escolher um arquivo de imagem
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            'Escolher Arquivo de Imagem',
            '',
            'Imagens (*.png *.jpg *.jpeg *.bmp)'
        )

        if arquivo:
            global global_image_path
            global_image_path = arquivo
            self.imagemOriginal = cv2.imread(arquivo)
            self.imagem_editada = self.imagemOriginal.copy()
            self.undo_redo_manager.save_image(self.imagem_editada)
            print(f"Arquivo escolhido: {arquivo}")

            # Exibir a imagem no QGraphicsView existente após configurar a interface
            self.exibir_imagem_editing(global_image_path)

            # Atualizar a imagem na segunda janela, se ela estiver aberta
            if self.second_window:
                self.abrir_segunda_janela()
            self.resetsliders()
        else:
            print("Nenhum arquivo foi escolhido.")

    def salvar_arquivo(self):
        formato_arquivo = self.detectar_formato_arquivo()
        nome_arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Arquivo",
            f"Untitle.{formato_arquivo}",
            f"Arquivos de Texto (*.{formato_arquivo});;Arquivos de Imagem (*.png *.jpg *.jpeg *.bmp);;Todos os Arquivos (*.*)"
        )
        if nome_arquivo:
            if self.imagem_terminada is not None:
                # Salvar a imagem editada
                cv2.imwrite(nome_arquivo, self.imagem_terminada)
            else:
                self.aplicar_edicao(self.imagem_terminada)
                cv2.imwrite(nome_arquivo, self.imagem_terminada)

    def detectar_formato_arquivo(self):
        mimetypes.init()
        tipo_arquivo = mimetypes.guess_type(global_image_path)[0]
        if tipo_arquivo:
            return tipo_arquivo.split("/")[-1]
        else:
            return "Formato desconhecido"

    def exibir_imagem_editing(self, caminho_imagem):
        ImagemEditing = cv2.imread(caminho_imagem)
        altura, largura, canais = ImagemEditing.shape
        self.InfoEdit.setText(
            f"Tamanho: ({largura}x{altura}) Canais: ({canais})")
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
        self.GraphicEdit.fitInView(
            scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

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
        if self.second_window.isHidden():
            # Exibir a imagem na segunda janela, se a imagem foi carregada
            if global_image_path:
                self.second_window.exibir_imagem_original(global_image_path)
            # Mostrar a segunda janela
            self.second_window.setHidden(False)
            self.second_window.raise_()
            self.second_window.activateWindow()
        else:
            if global_image_path:
                self.second_window.exibir_imagem_original(global_image_path)
            self.second_window.raise_()
            self.second_window.activateWindow()

    # Função para atualizar a imagem no QGraphicsView
    def aplicar_edicao(self, image):
        if image is not None:
            self.imagem_editada = image.copy()

        if not np.array_equal(self.imagem_editada, self.imagemOriginal):
            if self.imagem_editada is not None and image is not None:
                self.imagem_editada = image.copy()
                self.imagem_terminada = image.copy()
                self.atualizar_imagem(self.imagem_editada)
                self.undo_redo_manager.save_image(self.imagem_editada)
            elif image is None and self.imagem_editada is not None:
                self.imagem_terminada = self.imagem_editada.copy()

    def atualizar_imagem(self, imagem):
        if imagem is None:
            print("Imagem é none")

            return

        # Verificar o tipo de profundidade da imagem
        if imagem.dtype not in [np.float64, np.float32, np.int16, np.uint8]:
            raise ValueError("Tipo de dado da imagem não suportado")

        if imagem.dtype == np.float64 or imagem.dtype == np.float32:
            # Converter para 8 bits se for CV_64F ou CV_32F
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
        self.InfoEdit.setText(
            f"Tamanho: ({largura}x{altura}) Canais: {canais}")
        bytes_per_line = canais * largura

        # Converte a imagem para o formato QImage
        qimage = QImage(imagem_rgb.data, largura, altura,
                        bytes_per_line, QImage.Format.Format_RGB888)

        # Converte o QImage para QPixmap
        pixmap = QPixmap.fromImage(qimage)

        # Exibe a imagem no QGraphicsView
        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.GraphicEdit.setScene(scene)

        # Ajustar o QGraphicsView para encaixar a imagem
        self.GraphicEdit.fitInView(
            scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    # def iniciar_segunda_janela(self):
    #     # Criar e mostrar a segunda janela após a janela principal ser exibida
    #     if global_image_path:
    #         self.second_window = ImagemOriginal()
    #         self.second_window.exibir_imagem_original(global_image_path)
    #         self.second_window.show()
    #         self.second_window.raise_()
    #         self.second_window.activateWindow()


class ImagemOriginal(QMainWindow, Ui_ImagemOriginal):
    def __init__(self):
        super(ImagemOriginal, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('Icons/logoeditor.png'))

        # Conectar o evento de roda do mouse diretamente ao GraphicOrig
        self.GraphicOrig.wheelEvent = self.wheelEvent

        # Configurar as barras de rolagem para aparecer quando necessário
        self.GraphicOrig.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.GraphicOrig.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Sobrescrevendo o evento de fechamento
    def closeEvent(self, event):
        # Em vez de fechar, vamos apenas esconder a janela
        self.setHidden(True)
        # Prevenir o fechamento real da janela
        event.ignore()

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
        self.GraphicOrig.fitInView(
            scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        self.setHidden(False)

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
    # if global_image_path:
    #     main_window.iniciar_segunda_janela()

    sys.exit(app.exec())
