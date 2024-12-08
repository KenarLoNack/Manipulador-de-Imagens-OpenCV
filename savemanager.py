class ImageUndoRedoManager:
    def __init__(self, max_undos):
        self.undo_stack = []  # Pilha de imagens para desfazer (undo)
        self.redo_stack = []  # Pilha de imagens para refazer (redo)
        self.max_undos = max_undos  # Limite de quantos undos podem ser feitos

    def save_image(self, image):
        # Limitar o número de undos
        if len(self.undo_stack) >= self.max_undos:
            self.undo_stack.pop(0)  # Remove a imagem mais antiga
        self.undo_stack.append(image.copy())  # Salva uma cópia da imagem
        self.redo_stack.clear()  # Limpa o redo após uma nova ação

    def undo(self):
        if self.undo_stack and len(self.undo_stack) > 1:
            # Move a imagem atual para a pilha de redo e retorna a última imagem salva
            last_image = self.undo_stack.pop()
            self.redo_stack.append(last_image)
            return self.undo_stack[-1] if self.undo_stack else last_image
        return None

    def redo(self):
        if self.redo_stack:
            # Move a imagem do redo para a pilha de undo e retorna a imagem refeita
            redone_image = self.redo_stack.pop()
            self.undo_stack.append(redone_image)
            return redone_image
        return None
