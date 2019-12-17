from random import randint
import pygame
from game_param import GameParam
from network import Network
from player import Player
from button import Button
from get_games import Get_Games

pygame.font.init()

width = 640
height = 480
p = 0
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dice Game!")

mr_t_image = pygame.image.load('mr_t.jpg')

pygame.mixer.init()
slap_sound = pygame.mixer.Sound('slap.wav')


font_type = "arial black"
btn_color = (105, 105, 105)
font_color = (192, 192, 192)
roll_btn = Button("Roll", 50, 350, (btn_color), 0)
keep_button = Button("Keep 'em", 270, 410, (btn_color), 0)
choice_buttons = [Button("Die #1", 50, 350, (btn_color), 0),
                  Button("Die #2", 160, 350, (btn_color), 1),
                  Button("Die #3", 270, 350, (btn_color), 2),
                  Button("Die #4", 380, 350, (btn_color), 3),
                  Button("Die #5", 490, 350, (btn_color), 4)]
finish_btn = Button("Finish Round", 50, 350, (btn_color), 0)


def draw_waiting(win, game, dice_player):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont(font_type, 48)
    text = font.render("Waiting for Players...", 1, font_color)
    draw_scoreboard(win, game, dice_player)
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    pygame.event.get()
    pygame.display.flip()


def draw_roll_window(win, game, dice_player):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont(font_type, 24)
    draw_scoreboard(win, game, dice_player)
    text = font.render("Your roll", 1, font_color)
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))

    if dice_player.rolled is False and dice_player.remaining_rolls != 0:
        if dice_player.remaining_rolls == 1:
            finish_btn.draw(win)
        else:
            roll_btn.draw(win)
        render_total(dice_player)
    elif dice_player.rolled is True and dice_player.remaining_rolls != 0:
        button_count = 0
        keep_button.draw(win)
        for choice in choice_buttons:
            if button_count < dice_player.remaining_rolls:
                choice.draw(win)
            else:
                break
            button_count += 1
    else:
        draw_game_over_window(win, game, dice_player)
    if dice_player.rolled is True:
        render_rolls(dice_player)
    pygame.display.flip()


def render_rolls(dice_player):
    font = pygame.font.SysFont(font_type, 24)
    text = font.render("Die #1: " + str(dice_player.roll[0]), 1, (font_color))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 150))
    if dice_player.remaining_rolls > 1:
        text = font.render("Die #2: " + str(dice_player.roll[1]), 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))
    if dice_player.remaining_rolls > 2:
        text = font.render("Die #3: " + str(dice_player.roll[2]), 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 50))
    if dice_player.remaining_rolls > 3:
        text = font.render("Die #4: " + str(dice_player.roll[3]), 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 0))
    if dice_player.remaining_rolls > 4:
        text = font.render("Die #5: " + str(dice_player.roll[4]), 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 + 50))
    render_total(dice_player)


def render_total(dice_player):
    font = pygame.font.SysFont(font_type, 36)
    text6 = font.render("Total :" + str(dice_player.roll_total), 1, (font_color))
    win.blit(text6, (80, 600))


def draw_game_over_window(win, game, dice_player):
    win.fill((0, 0, 0))
    draw_scoreboard(win, game, dice_player)
    font = pygame.font.SysFont(font_type, 48)
    text = font.render("Game over fool!", 1, (font_color))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    text = font.render("Your Score: " + str(dice_player.roll_total), 1, (font_color))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))
    if game.finished():
        winner = game.get_winner()
        if winner and winner.result["push"] is True:
            text = font.render("Push!", 1, (font_color))
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))
        elif winner and winner.p == dice_player.p:
            text = font.render("You Win!", 1, (font_color))
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 300))
        else:
            text = font.render("You Lose!", 1, (font_color))
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 400))
        # dice_player.reset()
        pygame.time.wait(1000)
        # win.fill((0, 0, 0))
        pygame.display.flip()
        # create_a_game(dice_player)
    else:
        text = font.render("Waiting on them fools!", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))

    pygame.event.get()
    pygame.display.flip()


def draw_wait_your_turn_window(win, game, dice_player):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont(font_type, 24)
    rolling_player = game.whos_rolling()
    if rolling_player:
        text = font.render("Currently Rolling " + rolling_player.name, 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))
    draw_scoreboard(win, game, dice_player)
    pygame.event.get()
    pygame.display.flip()


def draw_scoreboard(win, game, dice_player):
    opponents = {}
    font = pygame.font.SysFont(font_type, 16)
    x_offset = 280
    y_offset = 220
    for opponent in opponents:
        text = font.render(opponents[opponent].name, 1, (0, 255, 255))
        win.blit(text, (width / 2 - text.get_width() / 2 - x_offset, height / 2 - text.get_height() / 2 - y_offset))
        text = font.render(str(opponents[opponent].roll_total), 1, (0, 255, 255))
        win.blit(text, (width / 2 - text.get_width() / 2 - x_offset + 40, height / 2 - text.get_height() / 2 - y_offset))
        y_offset -= 20
        if opponents[opponent].roll and opponents[opponent].rolling:
            render_rolls(opponents[opponent])
    btn = Button("Exit", 100, 10, (btn_color))
    btn.draw(win)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            dice_player.left_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if btn.click(pos):
                dice_player.left_game = True

def welcome_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("Welcome to the dice game!", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        win.blit(mr_t_image, (width/2 - 250, height/2 - 100))
        text1 = font.render("Press Any Key", 1, (font_color))
        win.blit(text1, (width / 2 - text1.get_width() / 2, (height / 2 - text1.get_height() / 2) - 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # slap_sound.play()
                run = False

        pygame.display.update()
    player_setup()


def player_setup():
    run = True
    clock = pygame.time.Clock()
    player_cash = 500

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("What up!?", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text1 = font.render("Please choose your character", 1, (font_color))
        win.blit(text1, (width / 2 - text1.get_width() / 2, (height / 2 - text1.get_height() / 2) - 100))
        btns1 = [Button("Tex", 125, 240, (btn_color)),
                 Button("Sally", 275, 240, (btn_color)),
                 Button("Floyd", 425, 240, (btn_color)),
                 Button("Amber", 125, 340, (btn_color)),
                 Button("Arnold", 275, 340, (btn_color)),
                 Button("$$$", 425, 340, (btn_color))]
        for btn in btns1:
            btn.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns1:
                    if btn.click(pos):
                        if btn.text == "$$$":
                            player_cash = randint(500, 800)
                            btn.text = "$" + str(player_cash)
                            continue
                        player_name = btn.text
                        dice_player = Player(player_name, player_cash)
                        print(dice_player.name + "  $" + str(player_cash))
                        run = False
        pygame.display.update()
    game_setup(dice_player)


def game_setup(dice_player):
    if dice_player.left_game is True:
        dice_player.reset()
    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("Game Setup", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text = font.render("Hello " + dice_player.name, 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 150))
        text = font.render("You Have $" + str(dice_player.cash), 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 100))

        btns1 = [Button("Join", 200, 300, (btn_color)),
                 Button("Create", 350, 300, (btn_color))]
        for btn in btns1:
            btn.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns1:
                    if btn.click(pos):
                        if btn.text == "Join":
                            join_game_screen(dice_player)
                        if btn.text == "Create":
                            create_game_screen(dice_player)
                        run = False
        pygame.display.flip()


def join_game_screen(dice_player):
    if dice_player.left_game is True:
        dice_player.reset()
    n = Network()
    g = Get_Games("join")
    n.connect(g)
    dice_player.p = int(n.getP())
    dice_player.global_id = n.get_global_id()
    dict_choice = draw_join_game_screen(n.games, dice_player)
    if dict_choice == -1:
        return game_setup(dice_player)
    g = Get_Games("join", dict_choice)
    dice_player.p = n.games[dict_choice].active_players
    n.send(g)
    dice_player.ready = True
    game = n.games[dict_choice]
    if game.in_progress:
        high_p = 0
        for d in game.dice_players:
            if game.dice_players[d].p >= high_p:
                high_p = game.dice_players[d].p
                dice_player.p = high_p
        dice_player.p += 1
    game = n.send(dice_player)
    create_a_game(n, game, dice_player)


def draw_join_game_screen(game_dict, dice_player):
    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("Join a Game", 1, (font_color))
        btn = Button("Exit", 100, 10, (btn_color))
        btn.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn.click(pos):
                    return -1
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        games = [Button("1", 10, 100, (btn_color)),
                 Button("2", 120, 100, (btn_color)),
                 Button("3", 230, 100, (btn_color)),
                 Button("4", 340, 100, (btn_color)),
                 Button("5", 560, 100, (btn_color))]
        button_count = 0
        for game in games:
            if (button_count < game_dict.__len__()):
                game.draw(win)
            else:
                break
            button_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for game in games:
                    if game.click(pos):
                        if game.text == "1":
                            count = 0
                            for g in game_dict:
                                count += 1
                                if count == 1:
                                    return g
                        if game.text == "2":
                            count = 0
                            for g in game_dict:
                                count += 1
                                if count == 2:
                                    return g
        pygame.display.flip()


def create_game_screen(dice_player):
    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("Create Game", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text = font.render("Number of Players", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 175))
        number_of_players = [Button("1", 50, 85, (btn_color)),
                             Button("2", 160, 85, (btn_color)),
                             Button("3", 270, 85, (btn_color)),
                             Button("4", 380, 85, (btn_color)),
                             Button("5", 490, 85, (btn_color))]
        for num in number_of_players:
            num.draw(win)

        text = font.render("Rounds", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 75))
        rounds = [Button("5", 50, 185, (btn_color)),
                  Button("10", 160, 185, (btn_color)),
                  Button("15", 270, 185, (btn_color)),
                  Button("20", 380, 185, (btn_color)),
                  Button("WTA", 490, 185, (btn_color))]
        for round in rounds:
            round.draw(win)

        text = font.render("Ante", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) +25))
        rounds = [Button("2", 50, 285, (btn_color)),
                  Button("5", 160, 285, (btn_color)),
                  Button("10", 270, 285, (btn_color)),
                  Button("20", 380, 285, (btn_color)),
                  Button("100", 490, 285, (btn_color))]
        for round in rounds:
            round.draw(win)

        text = font.render("Choose Away", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) + 125))
        rounds = [Button("1's", 10, 385, (btn_color)),
                  Button("2's", 120, 385, (btn_color)),
                  Button("3's", 230, 385, (btn_color)),
                  Button("4's", 340, 385, (btn_color)),
                  Button("5's", 450, 385, (btn_color)),
                  Button("6's", 560, 385, (btn_color))]
        for round in rounds:
            round.width = 75;
            round.draw(win)

        game_params = GameParam(2, 5, 10, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for num in number_of_players:
                    if num.click(pos):
                        if num.text == "1":
                            dice_player.ready = True
                            connect(dice_player, game_params)
                        if num.text == "2":
                            pass
        pygame.display.update()
    connect(dice_player, game_params)


def connect(dice_player, game_params):
    n = Network()
    g = Get_Games("create")
    if n.connect(g) == -1:
        create_game_screen(dice_player)
        return
    dice_player.p = int(n.getP())
    dice_player.global_id = n.get_global_id()
    n.send(dice_player)
    game = n.send(game_params)
    create_a_game(n, game, dice_player)


def create_a_game(n, game, dice_player):
    run = True
    clock = pygame.time.Clock()

    if dice_player.p == 0 or game.in_progress:
        dice_player.my_turn = True
        game = n.send(dice_player)

    while run:
        game = n.send(dice_player)
        if game is None:
            game_setup(dice_player)
        if game == -2:
            run = False
            print ("server quit")
            dice_player.left_game = True
            game_setup(dice_player)
        if game == -1:
            run = False
            pygame.quit()
        if dice_player.left_game is True:
            run = False
            game_setup(dice_player)
            #pygame.quit()
        clock.tick(60)
        font = pygame.font.SysFont(font_type, 48)
        if game.connected() is False:
            draw_waiting(win, game, dice_player)
        elif dice_player.my_turn is False and dice_player.finished is False:
            game = n.send(dice_player)
            draw_wait_your_turn_window(win, game, dice_player)
            if game.my_turn_yet(dice_player):
                dice_player.my_turn = True
        elif dice_player.my_turn is True and dice_player.finished is False:
            in_progress = GameParam(0,0,0,0)
            in_progress.in_progress = True
            n.send(in_progress)
            if dice_player.rolled is False:
                dice_player.rolling = True
                game = n.send(dice_player)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        dice_player.left_game = True
                        game = n.send(dice_player)
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if roll_btn.click(pos) and game.connected():
                            get_ready(dice_player)
                            dice_player.roll_dice()
                            if dice_player.remaining_rolls == 6:
                                dice_player.remaining_rolls -= 1
                            dice_player.rolled = True
                            game = n.send(dice_player)
                            if dice_player.remaining_rolls == 0:
                                dice_player.my_turn = False
                                dice_player.finished = True
                                dice_player.rolling = False
                                dice_player.rolled = False
                                game = n.send(dice_player)
                    draw_roll_window(win, game, dice_player)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        dice_player.quit = True
                        game = n.send(dice_player)
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONUP and dice_player.rolled is True:
                        pos = pygame.mouse.get_pos()
                        for choice in choice_buttons:
                            if choice.click(pos) and choice.selected is True:
                                choice.color = (btn_color)
                                if dice_player.roll[choice.value] != game.away_choice:
                                    dice_player.roll_total -= dice_player.roll[choice.value]
                                dice_player.roll_reduction -= 1
                                choice.selected = False
                                game = n.send(dice_player)
                            elif choice.click(pos) and game.connected():
                                choice.color = (12, 23, 0)
                                choice.selected = True
                                if dice_player.roll[choice.value] != game.away_choice:
                                    dice_player.roll_total += dice_player.roll[choice.value]
                                dice_player.roll_reduction += 1
                                game = n.send(dice_player)
                        if keep_button.click(pos):
                            keep_button.color = (12, 23, 0)
                            dice_player.final_total = dice_player.roll_total
                            if dice_player.roll_total > game.top_total:
                                dice_player.busted = True
                                dice_player.rolling = False
                                dice_player.remaining_rolls = 0
                                dice_player.finished = True
                            game = n.send(dice_player)
                            dice_player.rolled = False
                    if (draw_roll_window(win, game, dice_player) == False):
                        run = False
        elif dice_player.finished is True:
            draw_game_over_window(win, game, dice_player)


def get_ready(dice_player):
    dice_player.remaining_rolls -= dice_player.roll_reduction
    dice_player.roll_reduction = 0
    reset_buttons()


def reset_buttons():
    for choice in choice_buttons:
        choice.color = (btn_color)
        choice.selected = False
    keep_button.color = (btn_color)


while True:
    welcome_screen()
