import cv2 as cv
import numpy as np
from ImageProcessor import ImageProcessor

class AppInterface:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.image_original = None  # Imagem original carregada
        self.image = None  # Imagem processada
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
        self.menu_height = 120  # Altura do menu para os botões

    def mouse_callback(self, event, x, y, flags, param):
        """Callback para capturar cliques no menu de filtros."""
        if event == cv.EVENT_LBUTTONDOWN:  # Clique com o botão esquerdo do mouse
            if y < self.menu_height:  # Verifica se o clique foi no menu
                button_width = param.shape[1] // len(self.filters)  # Largura dinâmica dos botões
                button_index = x // button_width  # Índice do botão clicado
                if button_index < len(self.filters):
                    filter_name = self.filters[button_index]
                    print(f"Aplicando filtro: {filter_name}")
                    self.apply_filter(filter_name)

    def apply_filter(self, filter_name):
        """Aplica um filtro à imagem original."""
        try:
            if self.image_original is None:
                print("Erro: Nenhuma imagem carregada.")
                return

            # Aplica o filtro na imagem original
            processed_image = self.image_processor.apply_filter(self.image_original.copy(), filter_name)
            resized_image = self.resize_image(processed_image)
            self.show_image_with_menu(resized_image)
            self.image = processed_image  # Atualiza apenas a imagem processada exibida
        except ValueError as e:
            print(f"Erro ao aplicar o filtro: {e}")

    def resize_image(self, image, max_width=1200, max_height=900):
        """Redimensiona a imagem para caber na tela."""
        height, width = image.shape[:2]
        scale = min(max_width / width, (max_height - self.menu_height) / height)
        new_dimensions = (int(width * scale), int(height * scale))
        return cv.resize(image, new_dimensions)

    def show_image_with_menu(self, image):
        """Exibe a imagem com o menu de filtros."""
        menu = np.zeros((self.menu_height, image.shape[1], 3), dtype=np.uint8)
        button_width = image.shape[1] // len(self.filters)

        # Desenha os botões numerados
        for i in range(len(self.filters)):
            x_start = i * button_width
            x_end = x_start + button_width
            cv.rectangle(menu, (x_start, 0), (x_end, self.menu_height), (200, 200, 200), -1)
            cv.rectangle(menu, (x_start + 10, 10), (x_end - 10, self.menu_height - 10), (150, 150, 150), -1)
            
            # Adiciona o número ao botão
            text = str(i + 1)
            text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = x_start + (button_width - text_size[0]) // 2
            text_y = (self.menu_height + text_size[1]) // 2
            cv.putText(menu, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Concatena o menu acima da imagem
        combined = np.vstack((menu, image))
        cv.imshow("Editor de Imagens", combined)
        cv.setMouseCallback("Editor de Imagens", self.mouse_callback, param=combined)

    def image_input(self):
        """Permite ao usuário carregar uma imagem e usar filtros com menu interativo."""
        path = input("Digite o caminho da imagem: ")
        self.image_original = cv.imread(path)
        if self.image_original is None:
            print("Erro: não foi possível carregar a imagem. Verifique o caminho.")
            return

        print("Use o menu de filtros clicando nos botões! Aperte S para salvar o resultado!")
        resized_image = self.resize_image(self.image_original)
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
        if self.image is not None:
            output_path = input("Digite o caminho e o nome para salvar a imagem (ex.: output.jpg): ")
            cv.imwrite(output_path, self.image)
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
