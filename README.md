<a id="readme-top"></a>
# :camera::raised_hand_with_fingers_splayed: Jokenpô (w/ MediaPipe)

- ### [:dart: Objetivo](#dart-objetivo-1)
- ### [:rock: Dependências](#rock-dependências-1)
- ### [:page_with_curl: Documentação](#page_with_curl-documentação-1)
- ### [:scissors: Como rodar](#scissors-como-rodar-1)
- ### [:arrow_down: Baixar o projeto](https://github.com/hvslucas/jokenpo-mediapipe/archive/refs/heads/main.zip)

## Task from [CortechX](https://www.linkedin.com/company/cortechx.ufpb)

Esse foi um projeto desenvolvido por um discente do curso de *Engenharia da Computação da Universidade Federal da Paraíba*, curso este que pertence ao *[Centro de Informática](http://ci.ufpb.br/)*, localizado na *[Rua dos Escoteiros S/N - Mangabeira - João Pessoa - Paraíba - Brasil](https://g.co/kgs/xobLzCE)*. O projeto, no entanto, não é vinculado a uma disciplina do curso. Este pequeno projeto faz parte de uma task associada à Liga Acadêmica de Interação Humano-Computador, [CortechX](https://www.linkedin.com/company/cortechx.ufpb).

### :video_game: Autor:

-  :eye:  *[Lucas Henrique Vieira da Silva](https://github.com/hvslucas)*

###  :brain: Siga a CortechX:

-  [LinkedIn](https://www.linkedin.com/company/cortechx.ufpb)
-  [Instagram](https://www.instagram.com/cortechx.ufpb)
-  [GitHub](https://github.com/cortechx-team)

<p align="center">
  <a href="#readme-top">
    <img width="637" height="694" alt="5cba" src="https://github.com/user-attachments/assets/a1b9eff7-94d1-4df3-8c4d-73980f9edc7a" />
  </a>
</p>

## :dart: Objetivo

O objetivo deste projeto é desenvolver um jogo interativo de Jokenpô (Pedra, Papel e Tesoura) contra a máquina, jogando diretamente pela webcam. O foco principal da aplicação é a utilização prática de visão computacional: capturamos os frames de vídeo utilizando **OpenCV**[^1] e os processamos através do **MediaPipe**[^2] para mapear e desenhar, em tempo real, os 21 pontos de referência (landmarks) da mão do jogador.

[^1]: OpenCV. Open Source Computer Vision Library. https://opencv.org/
[^2]: MediaPipe. Framework para construção de pipelines de percepção multimodal. https://mediapipe.dev/

## :rock: Dependências

Para a execução adequada, recomenda-se a criação de um ambiente virtual Python configurado com as seguintes bibliotecas:

* **OpenCV** (`opencv-python`): Responsável por abrir a webcam, capturar os frames e renderizar a interface gráfica e os resultados na tela.
* **MediaPipe** (`mediapipe`): Framework encarregado do rastreamento da mão e extração das coordenadas espaciais.
* **Modelo do MediaPipe**: O arquivo pré-treinado `hand_landmarker.task`, necessário para a inferência local da detecção.

## :page_with_curl: Documentação

O núcleo do sistema funciona interpretando a lógica baseada nas coordenadas (X, Y) dos pontos da mão desenhados pelo MediaPipe. O algoritmo avalia a posição vertical (eixo Y) e horizontal (eixo X, para o polegar) das pontas dos dedos em relação às suas respectivas articulações inferiores. Dessa forma, é possível determinar quantos dedos estão levantados e mapear para a jogada correspondente:

* **✊ Pedra (Rock)**: 0 dedos levantados.
* **✌️ Tesoura (Scissors)**: 2 dedos levantados.
* **🖐️ Papel (Paper)**: 5 dedos levantados.

**Sistema de Jogo:**
O sistema confronta a jogada detectada com uma escolha aleatória gerada para a máquina. A cada rodada, o script processa a lógica de vitória, derrota ou empate e "printa" o resultado (quem ganhou a rodada e o placar geral) diretamente na tela da webcam. Como incremento, foi colocada a lógica de melhor de 3 rodadas para ganhar a partida.

**:open_file_folder: Estruturação:**

```text
jokenpo-mediapipe/
.
├── jokenpo_game.py         # Script principal. Gerencia a captura da webcam com OpenCV, a integração com o modelo do MediaPipe, o desenho dos 21 pontos na tela e o loop da partida (Melhor de 3).
├── gesture_utils.py        # Módulo auxiliar com a lógica do jogo. Contém as funções que calculam as coordenadas (X, Y) para contar os dedos, mapear o gesto (Pedra, Papel, Tesoura), gerar a jogada da máquina e definir o vencedor.
├── requirements.txt        # Arquivo contendo as dependências do Python necessárias para rodar o projeto (opencv-python e mediapipe).
├── hand_landmarker.task    # Modelo pré-treinado de Machine Learning do Google MediaPipe. Obrigatório para realizar a detecção das mãos (deve ser baixado manualmente).
└── README.md               # Documentação principal do projeto.
```

## :scissors: Como rodar

[**Atenção:** Lembre de baixar o projeto e extraí-lo devidamente do `.zip`.](#zap-simulação-de-circuitos-rlc-paralelo)

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Baixar o modelo antes da execução:

### Windows (PowerShell):

```sh
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -OutFile "hand_landmarker.task"
```

Linux (curl):

```sh
curl -o hand_landmarker.task [https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)
```

### 3. Executar o projeto

```sh
python jokenpo_game.py
```

**OBS.:** Versões dos frameworks podem ser um problema na execução
