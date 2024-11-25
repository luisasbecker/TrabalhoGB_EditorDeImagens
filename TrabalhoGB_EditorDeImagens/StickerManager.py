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

            print(sticker.shape[:2])
            # Redimensionar o sticker
            sticker = resize_image(sticker, 0 ,bg_width // 4, bg_height // 4)
            print(sticker.shape[:2])

            # Separar canais do sticker
            b, g, r, a = cv.split(sticker)
            mask = a
            mask_inv = cv.bitwise_not(mask)

            # Dimensões do sticker
            h, w, _ = sticker.shape

            # Verificar limites para evitar erro ao acessar ROI
            if y + h > background.shape[0] or x + w > background.shape[1]:
                raise ValueError("Sticker ultrapassa os limites da imagem de fundo.")

            # ROI da imagem de fundo
            roi = background[y:y+h, x:x+w]

            # Garantir que a máscara é do tipo correto (CV_8U)
            if mask_inv.dtype != "uint8":
                mask_inv = mask_inv.astype("uint8")
            if mask.dtype != "uint8":
                mask = mask.astype("uint8")

            # Combinação
            img_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
            img_fg = cv.bitwise_and(sticker[:, :, :3], sticker[:, :, :3], mask=mask)
            combined = cv.add(img_bg, img_fg)

            # Atualizar o ROI na imagem de fundo
            background[y:y+h, x:x+w] = combined
            return background
        else:
            raise IndexError("Índice do sticker inválido.")
