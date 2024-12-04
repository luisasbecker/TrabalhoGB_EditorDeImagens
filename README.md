# TrabalhoGB_EditorDeImagens

**Nomes:** Ana Beatriz Stahl
           Emanuele Schlemmer Thomazzoni
           Luisa Becker dos Santos

Este projeto é um editor de imagens 2D, desenvolvido como trabalho acadêmico para a disciplina de **Processamento Gráfico**. Ele utiliza a API Gráfica OpenGL moderna para manipulação de imagens, aplicando transformações, filtros e outras operações gráficas.

## Funcionalidades:
- Carregamento de imagens.
- Aplicação de transformações geométricas (translação, rotação, escalonamento).
- Efeitos básicos de filtro (tons de cinza, negativo, entre outros).
- Interface gráfica interativa para manipulação das operações.

## Requisitos:
Para compilar e executar a aplicação, você precisará de:

- Um compilador C/C++ (GCC, Clang ou MSVC).
- Biblioteca OpenGL (versão moderna, 4.0 ou superior).
- [GLFW](https://www.glfw.org/) - para gerenciar janelas e eventos.
- [GLEW](http://glew.sourceforge.net/) - para carregar extensões OpenGL.
- Uma IDE ou editor de texto de sua preferência (como Visual Studio Code, CLion, etc.).
- CMake (opcional, para sistemas que preferem build scripts).

## Como Compilar:

1. Clone o repositório para o seu ambiente local:

   ```bash
   git clone https://github.com/luisasbecker/TrabalhoGB_EditorDeImagens.git
   cd TrabalhoGB_EditorDeImagens

2. Certifique-se de que as dependências necessárias (GLFW, GLEW) estão instaladas no seu sistema.

3. Compile o projeto:

  - **Com GCC:**
       ```bash
       g++ main.cpp -o EditorDeImagens -lGL -lGLU -lglfw -lGLEW

  - **Com CMake:**
       ```bash
       mkdir build
       cd build
       cmake ..
       make
        
    
4. O executável será gerado no diretório atual.

## Estrutura do Repositório:

- **main.cpp:** Arquivo principal do programa.
- **src/:** Diretório contendo os arquivos fonte adicionais.
- **include/:** Diretório com os cabeçalhos do projeto.
- **resources/:** Diretório com imagens de exemplo e outros recursos visuais.
- **shaders/:** Diretório com os shaders usados no programa.
- **CMakeLists.txt:** Arquivo de configuração para o CMake.
