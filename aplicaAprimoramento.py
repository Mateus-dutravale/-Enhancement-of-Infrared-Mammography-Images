import cv2
import numpy as np
import matplotlib.pyplot as plt

def carregar_paleta(caminho_paleta):
    with open(caminho_paleta, 'r') as file:
        linhas = file.readlines()
    
    paleta = []
    for linha in linhas:
        if linha.strip(): 
            r, g, b = map(int, linha.strip().split())
            paleta.append((b, g, r))  
    
    return np.array(paleta, dtype=np.uint8)

for i in range(2, 101):  # Começa em 1 e vai até 100 (inclusive)
    # Carregar a imagem original 
    caminho_imagem = f"C:\\Users\\cactu\\Downloads\\lint\\imags_test_doentes\\a ({i}).jpg"
    imagem_original = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

    if imagem_original is None:
        print(f"Erro ao carregar a imagem: {caminho_imagem}")
        continue  # Pula para a próxima iteração se a imagem não for carregada

    # Carregar a matriz de calor do arquivo
    caminho_matriz = f"C:\\Users\\cactu\\Downloads\\lint\\imags_test_doentes\\a ({i-1}).txt"
    try:
        with open(caminho_matriz, "r") as file:
            linhas = file.readlines()
    except FileNotFoundError:
        print(f"Arquivo de matriz não encontrado: {caminho_matriz}")
        continue 

    matriz_calor = np.array([list(map(float, linha.split())) for linha in linhas])

    # Normalizar a matriz de calor para o intervalo de 0 a 255
    matriz_calor = (matriz_calor - matriz_calor.min()) / (matriz_calor.max() - matriz_calor.min()) * 255
    matriz_calor = matriz_calor.astype(np.uint8)

    paleta = carregar_paleta("C:\\Users\\cactu\\Downloads\\lint\\normalizações\\Rain.pal")

    matriz_calor_normalizada = (matriz_calor / 255.0) * (len(paleta) - 1)
    matriz_calor_normalizada = matriz_calor_normalizada.astype(np.uint8)

    # Aplicar a paleta de cores
    matriz_calor_colorida = np.zeros((matriz_calor.shape[0], matriz_calor.shape[1], 3), dtype=np.uint8)
    for row in range(matriz_calor.shape[0]):
        for col in range(matriz_calor.shape[1]):
            matriz_calor_colorida[row, col] = paleta[matriz_calor_normalizada[row, col]]

    # Redimensionar a imagem original para o tamanho da matriz de calor
    imagem_original = cv2.resize(imagem_original, (matriz_calor.shape[1], matriz_calor.shape[0]))

    imagem_original_bgr = cv2.cvtColor(imagem_original, cv2.COLOR_GRAY2BGR)

    # Misturar a matriz de calor com a imagem original 
    sobreposicao = cv2.addWeighted(imagem_original_bgr, 0.2, matriz_calor_colorida, 0.8, 0)

    caminho_saida = f"C:\\Users\\cactu\\PROJETOS\\python\\aprimoramento_projeto\\enhancement_Imags\\Rain\\Rain_{i-1}.jpg"
    cv2.imwrite(caminho_saida, sobreposicao)
