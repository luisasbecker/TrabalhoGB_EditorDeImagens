import cv2 as cv
from VideoCaptureManager import VideoCaptureManager
from ImageProcessor import ImageProcessor

class AppInterface:
    def __init__(self):
        self.video_manager = VideoCaptureManager()
        self.image_processor = ImageProcessor()

    def run(self):
        """Inicia a interface principal."""
        print("Bem-vindo ao editor de imagens!")
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

    def image_input(self):
        """Permite ao usuário carregar uma imagem e aplicar filtros."""
        path = input("Digite o caminho da imagem: ")
        image = cv.imread(path)
        if image is None:
            print("Erro: não foi possível carregar a imagem. Verifique o caminho.")
            return

        print("Imagem carregada com sucesso!")
        while True:
            print("\nFiltros disponíveis:")
            print("[1] Sobel")
            print("[2] Laplacian")
            print("[3] Grayscale")
            print("[4] Gaussian Blur")
            print("[5] Sepia")
            print("[6] Canny")
            print("[7] Brightness")
            print("[8] Negative")
            print("[9] Motion Blur")
            print("[10] Color Inversion")
            print("[11] Salvar imagem")
            print("[12] Voltar ao menu principal")
            
            filter_choice = input("Escolha um filtro para aplicar ou outra opção: ")

            if filter_choice == "11":
                output_path = input("Digite o caminho para salvar a imagem (com extensão): ")
                cv.imwrite(output_path, image)
                print(f"Imagem salva em {output_path}")
            elif filter_choice == "12":
                print("Voltando ao menu principal...")
                break
            else:
                try:
                    filters = {
                        "1": "sobel",
                        "2": "laplacian",
                        "3": "grayscale",
                        "4": "gaussian_blur",
                        "5": "sepia",
                        "6": "canny",
                        "7": "brightness",
                        "8": "negative",
                        "9": "motion_blur",
                        "10": "color_inversion"
                    }
                    if filter_choice in filters:
                        filter_name = filters[filter_choice]
                        print(f"Aplicando filtro: {filter_name}...")
                        processed_image = self.image_processor.apply_filter(image, filter_name)
                        
                        # Redimensiona a imagem para exibição
                        height, width = processed_image.shape[:2]
                        scale_factor = 0.5  # Ajuste o fator de escala para o tamanho desejado
                        new_dimensions = (int(width * scale_factor), int(height * scale_factor))
                        resized_image = cv.resize(processed_image, new_dimensions)

                        # Exibe a imagem redimensionada
                        cv.imshow(f"Imagem com filtro: {filter_name}", resized_image)
                        cv.waitKey(0)
                        cv.destroyAllWindows()

                        # Atualiza a imagem processada
                        image = processed_image
                    else:
                        print("Opção inválida. Tente novamente.")
                except ValueError as e:
                    print(f"Erro ao aplicar o filtro: {e}")

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
