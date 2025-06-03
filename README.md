# WattsUp Gesture Monitor 
 
 
 # Sobre o Projeto
Este é um sistema de reconhecimento de gestos que utiliza visão computacional para detectar sinais manuais específicos e disparar alertas sonoros correspondentes. O projeto foi desenvolvido para auxiliar em situações de emergência ou assistência, permitindo que usuários comuniquem necessidades através de gestos pré-definidos.

 # Tecnologias Utilizadas
OpenCV: Para captura e processamento de imagens

MediaPipe: Para detecção e rastreamento de mãos

PyGame: Para reprodução dos sons de alerta

Python: Linguagem principal do projeto

 # Gestos Reconhecidos
O sistema reconhece três gestos principais:

EMERGÊNCIA (todos os dedos levantados) - Toca som de emergência

ASSISTÊNCIA (indicador e médio levantados) - Toca som de assistência

RISCO (apenas indicador levantado) - Toca som de risco


# Bibliotecas listadas em requirements.txt

Arquivos de som no mesmo diretório do script:

emergencia.wav

assistencia.wav

risco.wav

 Instalação
Clone o repositório ou baixe o arquivo e Instale as dependências:

pip install -r requirements.txt

Certifique-se de ter os arquivos de som no diretório correto

 # Como Usar
Execute o script

Posicione sua mão diante da câmera

Faça um dos gestos reconhecidos para acionar o alerta correspondente

Pressione 'q' para sair do programa

 # Observações:
O sistema tem um cooldown de 3 segundos entre detecções para evitar repetições acidentais

Funciona melhor com fundos uniformes e boa iluminação

Apenas uma mão é detectada por vez (a primeira reconhecida).


Desenvolvido por Victor e Geovanna
