# Snake Game 🐍

Um jogo clássico da cobrinha (Snake) desenvolvido em Python 3 utilizando a biblioteca gráfica **Turtle**. Esta versão foi modificada e aprimorada com persistência de recorde (*High Score*), controle de redimensionamento de tela, telas de menu, créditos e um sistema exclusivo de trapaças sequenciais!

---

## 🎮 Como Jogar

1. Execute o jogo (seja pelo script `nake.py` ou pelo executável `jogo da cobrinha.exe`).
2. No **Menu Principal**:
   * Pressione **[1]** para Iniciar o jogo.
   * Pressione **[2]** para ver os Créditos.
3. Nos **Créditos**:
   * Pressione **[M]** para abrir a lista de trapaças.
   * Pressione **[B]** para voltar ao Menu Principal.

### Controles de Movimento
Você pode controlar a cobra utilizando tanto as setas do teclado quanto as teclas clássicas de movimentação:
* **Cima:** `W` ou `Seta para Cima`
* **Baixo:** `S` ou `Seta para Baixo`
* **Esquerda:** `A` ou `Seta para Esquerda`
* **Direita:** `D` ou `Seta para Direita`

---

## 🤫 Sistema de Trapaças (Cheats)

Durante a partida (enquanto estiver jogando), você pode digitar sequências de letras específicas no teclado para ativar ou desativar trapaças em tempo real. Um aviso amarelo aparecerá na parte inferior da tela confirmando a ação.

| Código | Descrição | Efeito |
| :---: | :--- | :--- |
| **`atr`** | **Atravessar Paredes** | A cobra atravessa as bordas da tela e aparece do lado oposto sem morrer. |
| **`inv`** | **Invencibilidade** | Permite que a cabeça da cobra passe por dentro do próprio corpo sem resetar o jogo. |
| **`dez`** | **Multiplicador 10x** | A comida se torna laranja e cada uma coletada passa a valer **10 pontos** em vez de 1. |
| **`pisc`** | **Efeito Pisca-Pisca** | Inverte as cores da cabeça (verde) e do corpo (verde-claro) a cada 1 segundo. |

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Turtle Graphics** (Interface e renderização do jogo)
* **Tkinter** (Tratamento de eventos e controle de janelas)
* **PyInstaller** (Utilizado para compilar o projeto em um executável `.exe` independente)

---

## 🗂️ Estrutura de Arquivos Importantes

* `nake.py`: Código-fonte principal do jogo.
* `ath.txt`: Arquivo local onde o seu recorde (*High Score*) fica salvo de forma persistente. Ele é criado automaticamente no diretório de dados do jogo.

---
*Desenvolvido por Gabriel Vinicius de Morais (2026).*