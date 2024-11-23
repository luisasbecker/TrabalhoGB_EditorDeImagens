import cv2 as cv
import numpy as np

class ImageProcessor:
    def __init__(self):
        pass

    def apply_filter(self, image, filter_name):
        """Aplica um filtro predefinido na imagem."""
        if filter_name == "sobel":
            kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
            return cv.filter2D(image, -1, kernel)
        elif filter_name == "laplacian":
            return cv.Laplacian(image, cv.CV_64F)
        elif filter_name == "grayscale":
            return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        elif filter_name == "gaussian_blur":
            return cv.GaussianBlur(image, (5, 5), 1.5)
        elif filter_name == "sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            return cv.transform(image, kernel)
        elif filter_name == "canny":
            return cv.Canny(image, 100, 200)
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
        else:
            raise ValueError(f"Filtro '{filter_name}' não implementado.")

    def adjust_saturation(self, image, scale):
        """Ajusta a saturação da imagem."""
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * scale, 0, 255).astype(np.uint8)
        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    def combine_filters(self, image, filters):
        """Combina múltiplos filtros aplicados na imagem."""
        for filter_name in filters:
            image = self.apply_filter(image, filter_name)
        return image
