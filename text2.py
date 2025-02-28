import cv2
import numpy as np

for i in range(2, 101): 
    # Caminho da imagem original
    caminho_imagem = f"C:\\Users\\cactu\\Downloads\\lint\\imags_test_doentes\\a ({i}).jpg"
    
    imagem_original = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

    if imagem_original is None:
        print(f"Erro ao carregar a imagem: {caminho_imagem}")
        continue  

    caminho_matriz = f"C:\\Users\\cactu\\Downloads\\lint\\imags_test_doentes\\a ({i-1}).txt"
    
    try:
        with open(caminho_matriz, "r") as file:
            linhas = file.readlines()
    except FileNotFoundError:
        print(f"Arquivo de matriz não encontrado: {caminho_matriz}")
        continue  
    # Converter os dados em uma matriz NumPy
    matriz_calor = np.array([list(map(float, linha.split())) for linha in linhas])

    # Normalizar a matriz de calor para o intervalo de 0 a 255
    matriz_calor = (matriz_calor - matriz_calor.min()) / (matriz_calor.max() - matriz_calor.min()) * 255
    matriz_calor = matriz_calor.astype(np.uint8)

    matriz_calor_colorida = cv2.applyColorMap(matriz_calor, cv2.COLORMAP_INFERNO)

    # Garantir que as dimensões sejam compatíveis
    imagem_original = cv2.resize(imagem_original, (matriz_calor.shape[1], matriz_calor.shape[0]))

    # Converter a imagem original para BGR para sobrepor corretamente
    imagem_original_bgr = cv2.cvtColor(imagem_original, cv2.COLOR_GRAY2BGR)

    sobreposicao = cv2.addWeighted(imagem_original_bgr, 0.2, matriz_calor_colorida, 0.9, 0)

    caminho_saida = f"C:\\Users\\cactu\\PROJETOS\\python\\aprimoramento_projeto\\enhancement_Imags\\Inferno\\Inferno_{i-1}.jpg"
    cv2.imwrite(caminho_saida, sobreposicao)

    print(f"Processamento concluido para i = {i}. Imagem salva em: {caminho_saida}")