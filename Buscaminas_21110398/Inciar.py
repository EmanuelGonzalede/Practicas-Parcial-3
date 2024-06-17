import pygame
import sys
import time

from buscaminas import Minesweeper, MinesweeperAI

# Constantes del juego
HEIGHT = 8
WIDTH = 8
MINES = 8

# Colores
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
RED = (255, 0, 0)

# Crear el juego
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fuentes
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Tamaño del tablero
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Cargar imágenes
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))
mine_red = pygame.image.load("assets/images/mine-red.png")
mine_red = pygame.transform.scale(mine_red, (cell_size, cell_size))

# Mina detonada
mine_detonated = None

# Crear el juego y la IA
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Rastrear celdas reveladas, celdas marcadas y si se ha golpeado una mina
revealed = set()
flags = set()
lost = False

# Mostrar instrucciones inicialmente
instructions = True

# Autoplay
autoplay = False
autoplaySpeed = 0.3
makeAiMove = False

# Mostrar celdas seguras y minas
showInference = False

while True:
    # Verificar si se ha cerrado el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Mostrar instrucciones del juego
    if instructions:
        # Título
        title = largeFont.render("Jugar al Buscaminas", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Reglas
        rules = [
"Haz clic en una celda para revelarla.",
            "Haz clic derecho en una celda para marcarla como mía.",
            "¡Marca todas las minas con éxito para ganar!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Botón para jugar
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Jugar", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Verificar si se ha hecho clic en el botón de jugar
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Dibujar el tablero
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            # Dibujar rectángulo para la celda
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Añadir una mina, bandera o número si es necesario
            if game.is_mine((i, j)) and lost:
                if (i, j) == mine_detonated:
                    screen.blit(mine_red, rect)
                else:
                    screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)
            elif (i, j) in ai.safes and showInference:
                pygame.draw.rect(screen, PINK, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)
            elif (i, j) in ai.mines and showInference:
                pygame.draw.rect(screen, RED, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)
            row.append(rect)
        cells.append(row)

    # Botón de Autoplay
    autoplayBtn = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Autoplay" if not autoplay else "Parar"
    buttonText = mediumFont.render(bText, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = autoplayBtn.center
    pygame.draw.rect(screen, WHITE, autoplayBtn)
    screen.blit(buttonText, buttonRect)

    # Botón de movimiento de IA
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 70,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Mover IA", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    if not autoplay:
        pygame.draw.rect(screen, WHITE, aiButton)
        screen.blit(buttonText, buttonRect)

    # Botón de reinicio
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 140,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Resetear", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    if not autoplay:
        pygame.draw.rect(screen, WHITE, resetButton)
        screen.blit(buttonText, buttonRect)

    # Texto de estado del juego
    text = "Perdiste" if lost else "Ganaste" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, BOARD_PADDING + 232)
    screen.blit(text, textRect)

    # Botón para mostrar celdas seguras y minas
    safesMinesButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 280,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Mostrar inferencia" if not showInference else "Ocultar inferencia"
    buttonText = smallFont.render(bText, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = safesMinesButton.center
    if not autoplay:
        pygame.draw.rect(screen, WHITE, safesMinesButton)
        screen.blit(buttonText, buttonRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Verificar clic derecho para alternar bandera
    if right == 1 and not lost and not autoplay:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # Si se hace clic en el botón de Autoplay, alternar autoplay
        if autoplayBtn.collidepoint(mouse):
            if not lost:
                autoplay = not autoplay
            else:
                autoplay = False
            time.sleep(0.2)
            continue

        # Si se hace clic en el botón de IA, hacer un movimiento de IA
        elif aiButton.collidepoint(mouse) and not lost:
            makeAiMove = True
            time.sleep(0.2)

        # Reiniciar estado del juego
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            mine_detonated = None
            continue

        # Si se hace clic en el botón de inferencia, alternar showInference
        elif safesMinesButton.collidepoint(mouse):
            showInference = not showInference
            time.sleep(0.2)

        # Movimiento hecho por el usuario
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Si autoplay está activado, hacer movimiento con IA
    if autoplay or makeAiMove:
        if makeAiMove:
            makeAiMove = False
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                flags = ai.mines.copy()
                print("No quedan movimientos por hacer.")
                autoplay = False
            else:
                print("No se conocen movimientos seguros, la IA realiza movimientos aleatorios.")
        else:
            print("IA haciendo movimientos seguros.")

        # Añadir demora para autoplay
        if autoplay:
            time.sleep(autoplaySpeed)

    # Hacer movimiento y actualizar conocimiento de la IA
    if move:
        if game.is_mine(move):
            lost = True
            mine_detonated = move
            autoplay = False
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()