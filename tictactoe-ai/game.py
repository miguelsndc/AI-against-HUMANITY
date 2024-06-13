import pygame as pg

pg.init()
screen = pg.display.set_mode((600, 500))
clock = pg.time.Clock()
running = True
font = pg.font.SysFont("Hack", 120)
board = [["", "", ""], ["", "", ""], ["", "", ""]]
IS_X_TURN = True
move_count = 0


def draw_lines():
    w = screen.get_width()
    h = screen.get_height()
    pg.draw.line(screen, "black", (w / 3, 0), (w / 3, h), 2)
    pg.draw.line(screen, "black", (w * 2 / 3, 0), (w * 2 / 3, h), 2)

    pg.draw.line(screen, "black", (0, h / 3), (w, h / 3), 2)
    pg.draw.line(screen, "black", (0, 2 * h / 3), (w, 2 * h / 3), 2)


def draw_players():
    i = 1
    w = screen.get_width()
    h = screen.get_height()
    f = lambda x: (1 / 6 + (x - 1) / 3)  # line that goes through all points i need

    for i in range(0, 3):
        height_mult = f(i + 1)
        for j in range(0, 3):
            width_mult = f(j + 1)
            if board[i][j] != "":
                text_surface = font.render(board[i][j], True, "black")
                fx, fy = font.size(board[i][j])
                screen.blit(
                    text_surface,
                    (w * width_mult - fx / 2, h * height_mult - fy / 2),
                )


def handle_click():
    w = screen.get_width()
    h = screen.get_height()
    mouse_x, mouse_y = pg.mouse.get_pos()

    x, y = 0, 0

    if mouse_x <= w / 3:
        y = 0
    elif 2 * w / 3 >= mouse_x >= w / 3:
        y = 1
    elif w >= mouse_x and mouse_x >= 2 * w / 3:
        y = 2

    if mouse_y <= h / 3:
        x = 0
    elif 2 * h / 3 >= mouse_y >= h / 3:
        x = 1
    elif h >= mouse_y >= 2 * h / 3:
        x = 2

    return x, y


def check_win():
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]

    if move_count == 9:
        return "DRAW"

    return None


def play(x, y):
    global IS_X_TURN, move_count
    symbol = "X" if IS_X_TURN else "O"

    if board[x][y] == "":
        board[x][y] = symbol
        move_count += 1
        IS_X_TURN = not IS_X_TURN


def announce_result(result):
    w = screen.get_width()
    h = screen.get_height()

    overlay = pg.Surface((w, h))
    overlay.set_alpha(128)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))

    text = f"{result} Won!" if result != "DRAW" else "Draw!"
    text_surface = font.render(text, False, "black")
    fx, fy = font.size(text)
    screen.blit(
        text_surface,
        (w / 2 - fx / 2, h / 2 - fy / 2),
    )

    pg.display.flip()
    pg.time.wait(2000)
    restart()
    pg.display.flip()


def restart():
    global board, move_count, IS_X_TURN
    for i in range(3):
        for j in range(3):
            board[i][j] = ""
    move_count = 0
    IS_X_TURN = True


def render():
    screen.fill("white")
    draw_lines()
    draw_players()
    pg.display.flip()


def evaluate():
    result = check_win()
    if result == "X":
        return -1
    elif result == "O":
        return 1
    elif result == "DRAW":
        return 0

    return None


def minimax(depth, maximizing):
    global move_count
    score = evaluate()
    if score is not None:
        return score

    if maximizing:
        best_score = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    move_count += 1
                    score = minimax(depth + 1, False)
                    board[i][j] = ""
                    move_count -= 1
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    move_count += 1
                    score = minimax(depth + 1, True)
                    board[i][j] = ""
                    move_count -= 1
                    best_score = min(score, best_score)
        return best_score


def find_best_move():
    global move_count
    best_score = float("-inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                move_count += 1
                score = minimax(0, False)
                board[i][j] = ""
                move_count -= 1
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def AI():
    move = find_best_move()
    if move is not None:
        play(move[0], move[1])


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = handle_click()
            play(x, y)
            render()
            result = check_win()
            if result is not None:
                announce_result(result)
                break
            AI()
    render()
    clock.tick(30)


pg.quit()
