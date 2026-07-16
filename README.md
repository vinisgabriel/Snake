# Snake Game com Trapaças

Um clássico jogo da cobrinha (Snake) desenvolvido em Python utilizando a biblioteca padrão `turtle`. O projeto conta com salvamento persistente de recorde (High Score), tela de menu iniciar, créditos e um sistema de trapaças sequenciais ocultas.

## 🚀 Funcionalidades
- **Menu Inicial:** Opções para iniciar o jogo ou visualizar os créditos.
- **High Score Persistente:** O seu recorde é salvo automaticamente em um arquivo de texto.
- **Bloqueio de Redimensionamento:** A janela do jogo possui tamanho fixo para não distorcer os elementos.
- **Área Segura de Comida:** A comidinha nunca nasce por cima do placar de pontuação.

## ⌨️ Comandos do Menu
- `1`: Iniciar Partida
- `2`: Ver Créditos
- `M` (na tela de créditos): Ver lista de trapaças cadastradas
- `B` (nas telas de menu): Voltar para a tela anterior

## 😈 Trapaças Ativas (Digitação Sequencial durante o jogo)
Digite as letras uma por uma rapidamente para ativar/desativar:
1. **`atr`** - Atravessar paredes (a cobra ressurge no lado oposto).
2. **`inv`** - Invencibilidade contra o próprio corpo.
3. **`dez`** - Cada comida passa a valer 10 pontos e muda de cor para laranja.

## 🛠️ Como Executar
Certifique-se de ter o Python instalado. Depois, execute o arquivo principal:
```bash
python jogo.py