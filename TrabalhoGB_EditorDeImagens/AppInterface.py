import cv2 as cv
import numpy as np
from ImageProcessor import ImageProcessor
from StickerManager import StickerManager
from VideoCaptureManager import VideoCaptureManager
from Utils import resize_image

class AppInterface:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.sticker_manager = StickerManager()
        self.video_manager = VideoCaptureManager()
        self.image_original = None  # Imagem original carregada
        self.image_processed = None  # Imagem processada
        self.sticker_layer = None # Camada de stickers
        self.filters = [
            "gaussian_blur",
            "sepia",
            "brightness",
            "negative",
            "motion_blur",
            "color_inversion",
            "contrast",
            "sharpen",
            "emboss",
            "edge_detection"
        ]
        self.stickers = [
            "bunny.png",
            "car.png",
            "drift_king.png",
            "hat.png",
            "money.png",
        ]
        self.total_menu_height = 240  # Altura do menu para os botões

    def mouse_callback(self, event, x, y, flags, param):
        """Callback para capturar cliques no menu de filtros."""
        if event == cv.EVENT_LBUTTONDOWN:  # Clique com o botão esquerdo do mouse
            menu_rows = 2  # Número de linhas no menu (filtros e adesivos)
            button_filters_width = param.shape[1] // len(self.filters)  # Largura dos botões para filtros
            button_stickers_width = param.shape[1] // len(self.stickers) # Langura dos botões para stickers
            button_height = self.total_menu_height // menu_rows  # Altura de cada linha do menu
            if y < self.total_menu_height:  # Verifica se o clique foi no menu
                row_index = y // button_height  # Determina a linha clicada
                if row_index == 0:  # Primeira linha: Filtros
                    button_index = x // button_filters_width  # Determina o índice do botão clicado
                    if button_index < len(self.filters):
                        filter_name = self.filters[button_index]
                        print(f"Aplicando filtro: {filter_name}")
                        self.apply_filter(filter_name)
                elif row_index == 1:  # Segunda linha: Stickers
                    button_index = x // button_stickers_width  # Determina o índice do botão clicado
                    if button_index < len(self.stickers):
                        sticker_name = self.stickers[button_index]
                        print(f"Aplicando adesivo: {sticker_name}")
                        self.apply_sticker(button_index, 0, 0)

    def apply_filter(self, filter_name):
        """Aplica um filtro à imagem original."""
        try:
            if self.image_original is None:
                print("Erro: Nenhuma imagem carregada.")
                return

            processed_image = self.image_processor.apply_filter(self.image_original.copy(), filter_name) # Aplique o filtro à imagem base (sem alterar a camada de stickers)
            resized_image = resize_image(processed_image, self.total_menu_height) # Redimensione a imagem para ajustar o menu
            self.image_processed = resized_image  # Atualiza apenas a imagem processada exibida
            combined_image = self.combine_layers() # Combina a imagem processada com a camada de stickers
            self.show_image_with_menu(combined_image) # Exibe a imagem com os stickers e o menu
        except ValueError as e:
            print(f"Erro ao aplicar o filtro: {e}")

    def apply_sticker(self, sticker_index, x, y):
        """Adiciona um adesivo à imagem."""
        try:
            if self.image_original is None:
                print("Erro: Nenhuma imagem carregada.")
                return
            
            # Verificar imagem disponível
            if self.image_processed is None:
                self.image_processed = self.image_original.copy()
            
            # Garantir que a camada de stickers está inicializada com 4 canais (RGBA)
            if self.sticker_layer is None:
                self.sticker_layer = np.zeros((self.image_original.shape[0], self.image_original.shape[1], 4), dtype=np.uint8)
            
            # Carregar o adesivo
            self.sticker_manager.load_stickers("TrabalhoGB_EditorDeImagens/Stickers") # Carrega os stickers
            self.sticker_layer = self.sticker_manager.apply_sticker(self.image_processed.copy(), sticker_index, x, y)

            # Atualiza a imagem com a camada de stickers
            combined_image = self.combine_layers()  # Combina as camadas (filtro + adesivo)
            resized_image = resize_image(combined_image, self.total_menu_height)
            self.show_image_with_menu(resized_image)  # Exibe a imagem com o menu
        except ValueError as e:
            print(f"Erro ao aplicar adesivo: {e}")

    def show_image_with_menu(self, image):
        """Exibe a imagem com o menu de filtros."""
        row_height = self.total_menu_height // 2
        menu = np.zeros((self.total_menu_height, image.shape[1], 3), dtype=np.uint8)

        button_filters_width = image.shape[1] // len(self.filters)
        # Primeira linha: desenha os botões numerados
        for i in range(len(self.filters)):
            x_start = i * button_filters_width
            x_end = x_start + button_filters_width
            cv.rectangle(menu, (x_start, 0), (x_end, row_height), (200, 200, 200), -1) # Altura total da primeira linha
            cv.rectangle(menu, (x_start + 10, 10), (x_end - 10, row_height - 10), (150, 150, 150), -1)
            
            # Adiciona o número ao botão
            text = str(i + 1)
            text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = x_start + (button_filters_width - text_size[0]) // 2
            text_y = (row_height + text_size[1]) // 2
            cv.putText(menu, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        button_stickers_width = image.shape[1] // len(self.stickers)
        # Segunda linha: desenho botões stickers
        for i in range(len(self.stickers)):
            x_start = i * button_stickers_width
            x_end = x_start + button_stickers_width
            y_start = row_height # Comeca depois da primeira linha
            y_end = y_start + row_height
            cv.rectangle(menu, (x_start, y_start), (x_end, y_end), (200, 200, 200), -1)  # Altura total da segunda linha
            cv.rectangle(menu, (x_start + 10, y_start + 10), (x_end - 10, y_end - 10), (150, 150, 150), -1)
            
            # Adiciona o número ao botão
            text = str(i + 1)
            text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = x_start + (button_stickers_width - text_size[0]) // 2
            text_y = y_start + (row_height + text_size[1]) // 2
            cv.putText(menu, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Concatena o menu acima da imagem
        combined = np.vstack((menu, image))
        cv.imshow("Editor de Imagens", combined)
        cv.setMouseCallback("Editor de Imagens", self.mouse_callback, param=combined)

    def combine_layers(self):
        """Combina a imagem de base, a camada de filtros, e a camada de stickers"""
        combined_image = self.image_original.copy()  # Start with the base image

        if self.image_processed is not None:
            combined_image = self.image_processed.copy()  # Use the processed image as the base
        
        if self.sticker_layer is not None:
            # Overlay the sticker layer
            if self.sticker_layer.shape[2] == 4:  # RGBA (sticker with transparency)
                alpha = self.sticker_layer[..., 3] / 255.0  # Extract the alpha channel
            else:  # If no alpha channel, assume the sticker is fully opaque
                alpha = np.ones_like(self.sticker_layer[..., 0], dtype=np.float32)

            # Blend the sticker onto the processed image
            for c in range(0, 3):  # Blend for each color channel
                combined_image[..., c] = (
                    alpha * self.sticker_layer[..., c] +
                    (1 - alpha) * combined_image[..., c]
                )
        
        return combined_image

    def image_input(self):
        """Permite ao usuário carregar uma imagem e usar filtros com menu interativo."""
        path = input("Digite o caminho da imagem: ")
        self.image_original = cv.imread(path)
        if self.image_original is None:
            print("Erro: não foi possível carregar a imagem. Verifique o caminho.")
            return

        print("Use o menu de filtros clicando nos botões! Aperte S para salvar o resultado!")
        resized_image = resize_image(self.image_original, self.total_menu_height)
        self.show_image_with_menu(resized_image)

        # Adicionar opção de salvamento ao pressionar 's'
        key = cv.waitKey(0)
        if key == ord('s'):  # Se a tecla 's' for pressionada
            self.save_image()
        cv.destroyAllWindows()

    def video_input(self):
        """Permite capturar um frame de vídeo e salvá-lo."""
        print("Iniciando captura de vídeo...")
        try:
            frame = self.video_manager.capture_frame()
            cv.imshow("Frame Capturado", frame)
            cv.waitKey(0)

            output_path = input("Digite o caminho para salvar o frame (com extensão): ")
            cv.imwrite(output_path, frame)
            print(f"Frame salvo em {output_path}")
        finally:
            self.video_manager.release()
            cv.destroyAllWindows()

    def save_image(self):
        """Salva a imagem processada."""
        if self.image_processed is not None:
            output_path = input("Digite o caminho e o nome para salvar a imagem (ex.: output.jpg): ")
            cv.imwrite(output_path, self.image_processed)
            print(f"Imagem salva em: {output_path}")
        else:
            print("Nenhuma imagem processada disponível para salvar.")

    def run(self):
        """Inicia a interface principal."""
        print("Bem-vindo ao editor de imagens com menu de filtros!")
        while True:
            print("\nMenu Principal:")
            print("[1] Carregar uma imagem")
            print("[2] Capturar um frame de vídeo")
            print("[3] Sair")
            
            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.image_input()
            elif choice == "2":
                self.video_input()
            elif choice == "3":
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")
