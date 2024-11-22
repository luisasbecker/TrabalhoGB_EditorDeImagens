import cv2 as cv
import numpy as np

class StickerManager:
    def __init__(self):
        self.stickers = []  # Lista de stickers carregados

    def load_stickers(self, paths):
        """Carrega stickers com canal alpha a partir de uma lista de caminhos."""
        for path in paths:
            sticker = cv.imread(path, cv.IMREAD_UNCHANGED)
            self.stickers.append(sticker)

    def apply_sticker(self, background, sticker_index, x, y):
        """Aplica um sticker na imagem de fundo."""
        if sticker_index < len(self.stickers):
            sticker = self.stickers[sticker_index]

            # Separar canais do sticker
            b, g, r, a = cv.split(sticker)
            mask = a
            mask_inv = cv.bitwise_not(mask)

            # Dimensões
            h, w, _ = sticker.shape
            roi = background[y:y+h, x:x+w]

            # Combinação
            img_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
            img_fg = cv.bitwise_and(sticker[:, :, :3], sticker[:, :, :3], mask=mask)
            combined = cv.add(img_bg, img_fg)

            # Atualizar o ROI na imagem de fundo
            background[y:y+h, x:x+w] = combined
            return background
        else:
            raise IndexError("Índice do sticker inválido.")
