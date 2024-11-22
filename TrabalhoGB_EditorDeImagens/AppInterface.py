import cv2 as cv
from VideoCaptureManager import VideoCaptureManager

class AppInterface:
    def __init__(self):
        self.video_manager = VideoCaptureManager()

    def run(self):
        """Inicia a interface principal."""
        print("Bem-vindo ao editor de imagens!")
        while True:
            print("\nMenu Principal:")
            print("[1] Carregar uma imagem")
            print("[2] Capturar um vídeo")
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
        """Permite ao usuário carregar uma imagem."""
        path = input("Digite o caminho da imagem: ")
        image = cv.imread(path)
        if image is None:
            print("Erro: não foi possível carregar a imagem. Verifique o caminho.")
        else:
            print("Imagem carregada com sucesso!")
            cv.imshow("Imagem Carregada", image)
            cv.waitKey(0)
            cv.destroyAllWindows()

    def video_input(self):
        """Permite ao usuário capturar um vídeo da webcam."""
        print("Iniciando captura de vídeo...")
        try:
            while True:
                frame = self.video_manager.capture_frame()
                cv.imshow("Vídeo ao Vivo (Pressione 'q' para sair)", frame)

                # Salva um frame ao pressionar 's'
                if cv.waitKey(1) & 0xFF == ord('s'):
                    output_path = input("Digite o caminho para salvar o frame (com extensão): ")
                    cv.imwrite(output_path, frame)
                    print(f"Frame salvo em {output_path}")

                # Encerra ao pressionar 'q'
                if cv.waitKey(1) & 0xFF == ord('q'):
                    print("Encerrando captura de vídeo...")
                    break
        finally:
            self.video_manager.release()
            cv.destroyAllWindows()
