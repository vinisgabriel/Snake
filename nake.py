# Simple Snake Game in Python 3 with Persistent High Score and Cheat Modes
# By @TokyoEdTech (Modificado para salvar o High Score, cheats sequenciais, travar redimensionamento, isolar o placar, Menu/Ajuda e Pisca)

import turtle
import time
import random
import os
import _tkinter  # Importado para capturar erros de interface ao fechar a janela

delay = 0.1

# Pontuação
score = 0
high_score = 0

# Estados do Jogo ("menu", "creditos", "ajuda", "jogando")
estado_jogo = "menu"

# Estados das Trapaças
cheat_atravessar = False  # Ativado com "atr"
cheat_invencivel = False  # Ativado com "inv"
cheat_dez_vezes = False  # Ativado com "dez"
cheat_pisca = False  # Ativado com "pisc"

# Variáveis para o controle do efeito pisca-pisca
ultimo_pisca = 0.0
cor_invertida = False

# Variáveis para controlar a exibição temporária das mensagens das trapaças
mostrar_mensagem_trapaca = False
tempo_mensagem_trapaca = 0.0

# Caminho completo para salvar o seu recorde
hs_file_path = r"D:\jogos\pasta com dados dos jogos\snake\ath.txt"

# Carregar o recorde do arquivo txt ao iniciar o jogo
try:
    # Garante que a estrutura de pastas existe
    dir_name = os.path.dirname(hs_file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Se o arquivo já existir, lê o valor do recorde anterior
    if os.path.exists(hs_file_path):
        with open(hs_file_path, "r") as file:
            content = file.read().strip()
            if content.isdigit():
                high_score = int(content)
except Exception as e:
    print(f"Erro ao carregar o high score: {e}")

# Configurações da tela do jogo
wn = turtle.Screen()
wn.title("Snake Game by @TokyoEdTech")
wn.bgcolor("black")  # Fundo PRETO
wn.setup(width=600, height=600)
wn.tracer(0)  # Desliga as atualizações de tela automáticas

# --- DESABILITAR BOTÃO DE TELA CHEIA (REDIMENSIONAMENTO) ---
root = wn.getcanvas().winfo_toplevel()
root.resizable(False, False)

# Cabeça da cobra (oculta no menu)
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")  # Cabeça VERDE
head.penup()
head.goto(0, 0)
head.direction = "stop"
head.hideturtle()

# Comida (oculta no menu)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)
food.hideturtle()

segments = []

# Objeto que desenha o placar tradicional e telas de menu/créditos
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

# Novo objeto para mostrar mensagens da trapaça na parte de baixo
pen_cheat = turtle.Turtle()
pen_cheat.speed(0)
pen_cheat.shape("square")
pen_cheat.color("yellow")  # Cor amarela para destacar o aviso
pen_cheat.penup()
pen_cheat.hideturtle()
pen_cheat.goto(0, -260)


# --- FUNÇÕES DE INTERFACE (MENU, CRÉDITOS, AJUDA E PLACAR) ---

def mostrar_menu():
    global estado_jogo
    estado_jogo = "menu"

    head.hideturtle()
    food.hideturtle()
    pen_cheat.clear()

    pen.clear()
    pen.color("white")
    pen.goto(0, 80)
    pen.write("SNAKE GAME", align="center", font=("Courier", 36, "bold"))

    pen.goto(0, -20)
    pen.write("Pressione [1] para Iniciar", align="center", font=("Courier", 20, "normal"))

    pen.goto(0, -70)
    pen.write("Pressione [2] para Créditos", align="center", font=("Courier", 20, "normal"))

    pen.goto(0, -200)
    pen.write(f"High Score: {high_score}", align="center", font=("Courier", 16, "normal"))


def mostrar_creditos():
    global estado_jogo
    estado_jogo = "creditos"

    pen.clear()
    pen.color("white")
    pen.goto(0, 110)
    pen.write("CRÉDITOS", align="center", font=("Courier", 32, "bold"))

    pen.goto(0, 30)
    pen.write("Criador: Gabriel Vinicius de Morais", align="center", font=("Courier", 18, "bold"))

    pen.goto(0, -20)
    pen.write("Ano: 2026", align="center", font=("Courier", 18, "normal"))

    pen.color("yellow")
    pen.goto(0, -100)
    pen.write("Pressione [M] para Mais Opções (Cheat List)", align="center", font=("Courier", 14, "bold"))

    pen.color("white")
    pen.goto(0, -180)
    pen.write("Pressione [B] para Voltar ao Menu", align="center", font=("Courier", 16, "italic"))


def mostrar_ajuda_trapacas():
    global estado_jogo
    estado_jogo = "ajuda"

    pen.clear()
    pen.color("yellow")
    pen.goto(0, 130)
    pen.write("MENU DE TRAPAÇAS", align="center", font=("Courier", 28, "bold"))

    pen.color("white")
    pen.goto(0, 50)
    pen.write("Digite as letras em sequência durante o jogo:", align="center", font=("Courier", 12, "italic"))

    pen.goto(0, 10)
    pen.write("atr  - Atravessar paredes", align="center", font=("Courier", 16, "normal"))

    pen.goto(0, -30)
    pen.write("inv  - Invencibilidade (corpo)", align="center", font=("Courier", 16, "normal"))

    pen.goto(0, -70)
    pen.write("dez  - Comida Laranja / Vale 10 Pontos", align="center", font=("Courier", 16, "normal"))

    pen.goto(0, -110)
    pen.write("pisc - Cobrinha Pisca-Pisca (1s)", align="center", font=("Courier", 16, "normal"))

    pen.color("white")
    pen.goto(0, -180)
    pen.write("Pressione [B] para Voltar aos Créditos", align="center", font=("Courier", 16, "italic"))


def iniciar_jogo():
    global estado_jogo, score, cheat_pisca, cor_invertida
    estado_jogo = "jogando"
    score = 0
    cheat_pisca = False
    cor_invertida = False

    # Reseta posições e exibe cobra e comida com as cores originais
    head.goto(0, 0)
    head.direction = "stop"
    head.color("green")
    head.showturtle()

    food.goto(0, 100)
    food.showturtle()

    atualizar_placar()


def atualizar_placar():
    if estado_jogo == "jogando":
        pen.clear()
        pen.color("white")
        pen.goto(0, 260)
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))


# Funções de movimento da cobra
def go_up():
    if estado_jogo == "jogando" and head.direction != "down":
        head.direction = "up"


def go_down():
    if estado_jogo == "jogando" and head.direction != "up":
        head.direction = "down"


def go_left():
    if estado_jogo == "jogando" and head.direction != "right":
        head.direction = "left"


def go_right():
    if estado_jogo == "jogando" and head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


# Função para atualizar o arquivo de texto com o novo recorde
def save_high_score(new_high_score):
    try:
        with open(hs_file_path, "w") as file:
            file.write(str(new_high_score))
    except Exception as e:
        print(f"Erro ao salvar o high score: {e}")


# --- SISTEMA DE DETECÇÃO SEQUENCIAL DOS CHEATS ---
teclas_pressionadas = ""


def registrar_tecla(char):
    global teclas_pressionadas, cheat_atravessar, cheat_invencivel, cheat_dez_vezes, cheat_pisca, mostrar_mensagem_trapaca, tempo_mensagem_trapaca

    if estado_jogo != "jogando":
        return  # Cheats só funcionam enquanto estiver jogando

    teclas_pressionadas += char

    # Permite analisar até as últimas 4 letras digitadas para incluir "pisc"
    if len(teclas_pressionadas) > 4:
        teclas_pressionadas = teclas_pressionadas[-4:]

    # Cheat 1: "atr" (Atravessar paredes)
    if teclas_pressionadas.endswith("atr"):
        cheat_atravessar = not cheat_atravessar
        teclas_pressionadas = ""

        mostrar_mensagem_trapaca = True
        tempo_mensagem_trapaca = time.time()

        pen_cheat.clear()
        if cheat_atravessar:
            pen_cheat.write("Trapaça Ativada!", align="center", font=("Courier", 20, "bold"))
        else:
            pen_cheat.write("Trapaça Desativada!", align="center", font=("Courier", 20, "bold"))

    # Cheat 2: "inv" (Invencibilidade contra o corpo)
    elif teclas_pressionadas.endswith("inv"):
        cheat_invencivel = not cheat_invencivel
        teclas_pressionadas = ""

        mostrar_mensagem_trapaca = True
        tempo_mensagem_trapaca = time.time()

        pen_cheat.clear()
        if cheat_invencivel:
            pen_cheat.write("Invencibilidade Ativada!", align="center", font=("Courier", 20, "bold"))
        else:
            pen_cheat.write("Invencibilidade Desativada!", align="center", font=("Courier", 20, "bold"))

    # Cheat 3: "dez" (Pontos valem 10 e comida laranja)
    elif teclas_pressionadas.endswith("dez"):
        cheat_dez_vezes = not cheat_dez_vezes
        teclas_pressionadas = ""

        mostrar_mensagem_trapaca = True
        tempo_mensagem_trapaca = time.time()

        pen_cheat.clear()
        if cheat_dez_vezes:
            food.color("orange")
            pen_cheat.write("Multiplicador 10x Ativado!", align="center", font=("Courier", 20, "bold"))
        else:
            food.color("red")
            pen_cheat.write("Multiplicador 10x Desativado!", align="center", font=("Courier", 20, "bold"))

    # Cheat 4: "pisc" (Inverter cores de 1 em 1 segundo)
    elif teclas_pressionadas.endswith("pisc"):
        cheat_pisca = not cheat_pisca
        teclas_pressionadas = ""

        mostrar_mensagem_trapaca = True
        tempo_mensagem_trapaca = time.time()

        pen_cheat.clear()
        if cheat_pisca:
            pen_cheat.write("Pisca-Pisca Ativado!", align="center", font=("Courier", 20, "bold"))
        else:
            pen_cheat.write("Pisca-Pisca Desativado!", align="center", font=("Courier", 20, "bold"))
            # Restaura as cores originais da cobra imediatamente ao desligar
            head.color("green")
            for segment in segments:
                segment.color("lightgreen")


# --- FUNÇÕES DE CONTROLE DE MENU/TELAS ---
def pressionou_1():
    if estado_jogo == "menu":
        iniciar_jogo()


def pressionou_2():
    if estado_jogo == "menu":
        mostrar_creditos()


def pressionou_m():
    if estado_jogo == "creditos":
        mostrar_ajuda_trapacas()


def pressionou_b():
    if estado_jogo == "creditos":
        mostrar_menu()
    elif estado_jogo == "ajuda":
        mostrar_creditos()


# Atalhos do teclado
wn.listen()

# Movimentos (WASD / Setas)
wn.onkeypress(go_up, "w")
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "d")
wn.onkeypress(go_right, "Right")

# Atalhos exclusivos do Menu, Créditos e Ajuda
wn.onkeypress(pressionou_1, "1")
wn.onkeypress(pressionou_2, "2")
wn.onkeypress(pressionou_m, "m")
wn.onkeypress(pressionou_m, "M")
wn.onkeypress(pressionou_b, "b")
wn.onkeypress(pressionou_b, "B")

# Registra as teclas individuais para as senhas "atr", "inv", "dez" e "pisc"
wn.onkeypress(lambda: registrar_tecla("a"), "a")
wn.onkeypress(lambda: registrar_tecla("t"), "t")
wn.onkeypress(lambda: registrar_tecla("r"), "r")
wn.onkeypress(lambda: registrar_tecla("i"), "i")
wn.onkeypress(lambda: registrar_tecla("n"), "n")
wn.onkeypress(lambda: registrar_tecla("v"), "v")
wn.onkeypress(lambda: registrar_tecla("d"), "d")
wn.onkeypress(lambda: registrar_tecla("e"), "e")
wn.onkeypress(lambda: registrar_tecla("z"), "z")
wn.onkeypress(lambda: registrar_tecla("p"), "p")
wn.onkeypress(lambda: registrar_tecla("s"), "s")
wn.onkeypress(lambda: registrar_tecla("c"), "c")

# Exibe o menu inicialmente ao abrir o script
mostrar_menu()

# Loop principal do jogo com tratamento contra erro ao fechar a janela
try:
    while True:
        wn.update()

        if estado_jogo == "jogando":
            # Lógica do timer de 5 segundos para a mensagem sumir
            if mostrar_mensagem_trapaca:
                if time.time() - tempo_mensagem_trapaca > 5.0:
                    pen_cheat.clear()
                    mostrar_mensagem_trapaca = False

            # Lógica do efeito Pisca-Pisca (Inverte cores a cada 1.0 segundo)
            if cheat_pisca:
                if time.time() - ultimo_pisca >= 1.0:
                    cor_invertida = not cor_invertida
                    ultimo_pisca = time.time()

                    if cor_invertida:
                        head.color("lightgreen")
                        for segment in segments:
                            segment.color("green")
                    else:
                        head.color("green")
                        for segment in segments:
                            segment.color("lightgreen")

            # Verificar colisão com as bordas
            if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
                if cheat_atravessar:
                    if head.xcor() > 290:
                        head.setx(-290)
                    elif head.xcor() < -290:
                        head.setx(290)
                    elif head.ycor() > 290:
                        head.sety(-290)
                    elif head.ycor() < -290:
                        head.sety(290)
                else:
                    time.sleep(1)

                    # Esconde o corpo da cobra
                    for segment in segments:
                        segment.goto(1000, 1000)
                    segments.clear()

                    delay = 0.1

                    # Garante comida em local seguro no reset
                    x = random.randint(-290, 290)
                    y = random.randint(-290, 220)
                    food.goto(x, y)

                    mostrar_menu()

            # Verificar colisão com a comida
            if head.distance(food) < 20:
                x = random.randint(-290, 290)
                y = random.randint(-290, 220)
                food.goto(x, y)

                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")

                # Se o cheat de piscar estiver ativo, cria o novo segmento na cor certa do momento
                if cheat_pisca and cor_invertida:
                    new_segment.color("green")
                else:
                    new_segment.color("lightgreen")

                new_segment.penup()
                segments.append(new_segment)

                delay -= 0.001

                if cheat_dez_vezes:
                    score += 10
                else:
                    score += 1

                if score > high_score:
                    high_score = score
                    save_high_score(high_score)

                atualizar_placar()

            # Move os segmentos do corpo
            for index in range(len(segments) - 1, 0, -1):
                x = segments[index - 1].xcor()
                y = segments[index - 1].ycor()
                segments[index].goto(x, y)

            if len(segments) > 0:
                x = head.xcor()
                y = head.ycor()
                segments[0].goto(x, y)

            move()

            # Verificar colisão da cabeça com o corpo
            for segment in segments:
                if segment.distance(head) < 20:
                    if cheat_invencivel:
                        pass
                    else:
                        time.sleep(1)

                        for segment in segments:
                            segment.goto(1000, 1000)
                        segments.clear()

                        delay = 0.1

                        # Garante comida em local seguro
                        x = random.randint(-290, 290)
                        y = random.randint(-290, 220)
                        food.goto(x, y)

                        mostrar_menu()

            time.sleep(delay)
        else:
            # Se estiver no menu, créditos ou ajuda, o jogo simplesmente espera o input das teclas
            time.sleep(0.05)

except (turtle.Terminator, _tkinter.TclError):
    # Trata de forma amigável e encerra o script sem estourar Tracebacks
    pass