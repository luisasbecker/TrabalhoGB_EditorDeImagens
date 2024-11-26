import cv2 as cv

def resize_image(image, total_menu_height, max_width=1200, max_height=900):
    """Redimensiona a imagem para caber na tela."""
    height, width = image.shape[:2]
    scale = min(max_width / width, (max_height - total_menu_height) / height)
    new_dimensions = (int(width * scale), int(height * scale))
    return cv.resize(image, new_dimensions)