import cv2 as cv
import numpy as np

class ImageProcessor:
    def __init__(self):
        pass

    def apply_filter(self, image, filter_name):
        """Aplica um filtro predefinido na imagem."""
        # Converter para uint8, caso necessário
        if image.dtype != np.uint8:
            image = cv.normalize(image, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)

        # Garantir que a imagem seja colorida
        if len(image.shape) == 2:  # Se for escala de cinza, converte para RGB
            image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)

        if filter_name == "gaussian_blur":
            return cv.GaussianBlur(image, (5, 5), 1.5)
        elif filter_name == "sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            sepia_image = cv.transform(image, kernel)
            return cv.normalize(sepia_image, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
        elif filter_name == "brightness":
            return cv.convertScaleAbs(image, alpha=1.2, beta=30)  # Aumenta brilho
        elif filter_name == "negative":
            return cv.bitwise_not(image)
        elif filter_name == "motion_blur":
            kernel_size = 15
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
            kernel = kernel / kernel_size
            return cv.filter2D(image, -1, kernel)
        elif filter_name == "color_inversion":
            b, g, r = cv.split(image)
            return cv.merge((255-b, 255-g, 255-r))
        elif filter_name == "contrast":
            return cv.convertScaleAbs(image, alpha=1.5, beta=0)  # Aumenta contraste
        elif filter_name == "sharpen":
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            return cv.filter2D(image, -1, kernel)
        elif filter_name == "emboss":
            kernel = np.array([[-2, -1, 0],
                               [-1, 1, 1],
                               [0, 1, 2]])
            return cv.filter2D(image, -1, kernel)
        elif filter_name == "edge_detection":
            kernel = np.array([[-1, -1, -1],
                               [-1, 8, -1],
                               [-1, -1, -1]])
            return cv.filter2D(image, -1, kernel)
        else:
            raise ValueError(f"Filtro '{filter_name}' não implementado.")
