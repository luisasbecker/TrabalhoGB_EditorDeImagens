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

            cv.imwrite("./img.png", transparent_image)
            # Retornar a imagem com o sticker aplicado
            return transparent_image
        else:
            raise IndexError("Índice do sticker inválido.")
