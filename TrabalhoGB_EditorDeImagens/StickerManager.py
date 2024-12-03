import cv2 as cv
import numpy as np
import os
from Utils import resize_image

class StickerManager:
    def __init__(self):
        self.stickers = []  # Lista de stickers carregados

    def load_stickers(self, path):
        """Carrega stickers com canal alpha a partir de uma lista de caminhos."""
        files = [f for f in os.listdir(path) if f.endswith('.png')]
        for file in files:
            sticker = cv.imread(path + "/" + file, cv.IMREAD_UNCHANGED)
            self.stickers.append(sticker)

    def apply_sticker(self, background, sticker_index, x, y):
        """Aplica um sticker na imagem de fundo."""
        if sticker_index < len(self.stickers):
            sticker = self.stickers[sticker_index]

            # Dimensoes da imagem de fundo
            bg_height, bg_width = background.shape[:2]

            # Criar uma nova imagem transparente com as mesmas dimensões da imagem de fundo
            transparent_image = np.zeros((bg_height, bg_width, 4), dtype=np.uint8)  # RGBA (com fundo transparente)

            # Redimensionar o sticker
            sticker = resize_image(sticker, 0 ,bg_width // 4, bg_height // 4)

            # Dimensões do sticker
            h, w, _ = sticker.shape

            # Verificar limites para evitar erro ao acessar ROI
            if y + h > transparent_image.shape[0] or x + w > transparent_image.shape[1]:
                raise ValueError("Sticker ultrapassa os limites da imagem de fundo.")

            # Colocar o sticker diretamente na imagem transparente no local especificado (x, y)
            transparent_image[y:y+h, x:x+w] = sticker

            # Retornar a imagem com o sticker aplicado
            return transparent_image
        else:
            raise IndexError("Índice do sticker inválido.")

class StickerLayer:
    def __init__(self, image = None, metadata = None):
        self.id = None  # Identifier for the sticker
        self.position = (0, 0)  # Position of the sticker (x, y)
        self.size = (0, 0)  # Size of the sticker (width, height)
        self.is_sticker_selected = False  # Whether a sticker is selected
        self.layer = None  # The sticker layer (image data)
        self.shape = (0, 0, 4)  # Shape of the sticker layer (height, width, channels)

    def load(self, sticker_image):
        """Loads a sticker image into the layer."""
        self.layer = sticker_image
        self.size = (sticker_image.shape[1], sticker_image.shape[0])  # Width, height
        self.shape = sticker_image.shape

    def set_position(self, x, y):
        """Sets the position of the sticker."""
        self.position = (x, y)