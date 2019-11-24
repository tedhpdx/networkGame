from random import randint
import pygame
from game_param import GameParam
from network import Network
from player import Player
from button import Button
from get_games import Get_Games

pygame.font.init()

width = 1000
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")



mr_t_image = pygame.image.load('mr_t.jpg')

pygame.mixer.init()
slap_sound = pygame.mixer.Sound('slap.wav')


font_type = "arial black"
btn_color = (105, 105, 105)
font_color = (192, 192, 192)
roll_btn = Button("Roll", 50, 500, (btn_color), 0)
keep_button = Button("Keep Selected", 300, 600, (btn_color), 0)
choice_buttons = [Button("Die #1", 0, 500, (btn_color), 0),
                  Button("Die #2", 200, 500, (btn_color), 1),
                  Button("Die #3", 400, 500, (btn_color), 2),
                  Button("Die #4", 600, 500, (btn_color), 3),
                  Button("Die #5", 800, 500, (btn_color), 4)]
finish_btn = Button("Finish Round", 50, 500, (btn_color), 0)



def redrawWindow(win, game, dice_player):
    win.fill((0, 0, 0))
    if not (game.connected()):
        font = pygame.font.SysFont(font_type, 48)
        text = font.render("Waiting for Player...", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont(font_type, 36)
        text = font.render("Your roll", 1, (font_color))
        win.blit(text, (80, 200))

        text = font.render("Opponent", 1, (font_color))
        win.blit(text, (380, 200))
        opponent = game.get_opponent(dice_player)
        text = font.render(opponent.name, 1, (0, 255, 255))
        win.blit(text, (380, 400))

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
    pygame.display.update()


def render_rolls(dice_player):
    font = pygame.font.SysFont(font_type, 36)
    text1 = font.render("Die #1: " + str(dice_player.roll[0]), 1, (font_color))
    win.blit(text1, (80, 250))
    if dice_player.remaining_rolls > 1:
        text2 = font.render("Die #2: " + str(dice_player.roll[1]), 1, (font_color))
        win.blit(text2, (80, 300))
    if dice_player.remaining_rolls > 2:
        text3 = font.render("Die #3: " + str(dice_player.roll[2]), 1, (font_color))
        win.blit(text3, (80, 350))
    if dice_player.remaining_rolls > 3:
        text4 = font.render("Die #4: " + str(dice_player.roll[3]), 1, (font_color))
        win.blit(text4, (80, 400))
    if dice_player.remaining_rolls > 4:
        text5 = font.render("Die #5: " + str(dice_player.roll[4]), 1, (font_color))
        win.blit(text5, (80, 450))
    render_total(dice_player)


def render_total(dice_player):
    font = pygame.font.SysFont(font_type, 36)
    text6 = font.render("Total :" + str(dice_player.roll_total), 1, (font_color))
    win.blit(text6, (80, 600))


def draw_game_over_window(win, game, dice_player):
    win.fill((0, 0, 0))
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
        #dice_player.reset()
        pygame.time.wait(1000)
        #win.fill((0, 0, 0))
        pygame.display.flip()
        #create_a_game(dice_player)
    else:
        text = font.render("Waiting on them fools!", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))

    pygame.event.get()
    pygame.display.flip()


def draw_wait_your_turn_window(win, game, dice_player):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont(font_type, 48)
    text = font.render("Wait, it's not your turn yet fool!", 1, (font_color))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    opponent = game.get_opponent(dice_player)
    text = font.render(str(opponent.roll_total), 1, (font_color))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))
    if opponent.roll:
        render_rolls(opponent)
    pygame.event.get()
    pygame.display.flip()





def welcome_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("Welcome to the dice game!", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        win.blit(mr_t_image, (250,500))
        text1 = font.render("Press Any Key", 1, (font_color))
        win.blit(text1, (width / 2 - text1.get_width() / 2, (height / 2 - text1.get_height() / 2) - 100))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                #slap_sound.play()
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
        text = font.render("Hi there!", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text1 = font.render("Please choose your character", 1, (font_color))
        win.blit(text1, (width / 2 - text1.get_width() / 2, (height / 2 - text1.get_height() / 2) - 100))
        btns1 = [Button("Tex", 200, 600, (btn_color)),
                 Button("Sally", 400, 600, (btn_color)),
                 Button("Floyd", 600, 600, (btn_color)),
                 Button("Amber", 200, 750, (btn_color)),
                 Button("Arnold", 400, 750, (btn_color)),
                 Button("Generate $$$", 600, 750, (btn_color))]
        for btn in btns1:
            btn.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for btn in btns1:
                    if btn.click(pos):
                        if btn.text == "Generate $$$":
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
    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("Game Setup", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text = font.render("Hello " + dice_player.name, 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 400))
        text = font.render("You Have $" + str(dice_player.cash), 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 300))


        btns1 = [Button("Join Game", 300, 600, (btn_color)),
                 Button("Create A Game", 500, 600, (btn_color))]
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
                        if btn.text == "Join Game":
                            join_game_screen(dice_player)
                        if btn.text == "Create A Game":
                            create_game_screen(dice_player)
                        run = False
        pygame.display.update()


def join_game_screen(dice_player):
    n = Network()
    g = Get_Games("join")
    n.connect(g)
    dict_choice = draw_join_game_screen(n.games, dice_player)
    g = Get_Games("join", dict_choice)
    n.send(g)
    dice_player.ready = True
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
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 484))
        games = [Button("1", 25, 100, (btn_color)),
                 Button("2", 225, 100, (btn_color)),
                 Button("3", 425, 100, (btn_color)),
                 Button("4", 625, 100, (btn_color)),
                 Button("5", 825, 100, (btn_color))]
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
                            return 1
                        if game.text == "2":
                            return 2
        pygame.display.flip()


def create_game_screen(dice_player):
    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(font_type, 24)
        text = font.render("Create Game", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 484))
        text = font.render("Number of Players", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 450))
        number_of_players = [Button("1", 25, 100, (btn_color)),
                             Button("2", 225, 100, (btn_color)),
                             Button("3", 425, 100, (btn_color)),
                             Button("4", 625, 100, (btn_color)),
                             Button("5", 825, 100, (btn_color))]
        for num in number_of_players:
            num.draw(win)

        text = font.render("Rounds", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 250))
        rounds = [Button("5", 25, 300, (btn_color)),
                  Button("10", 225, 300, (btn_color)),
                  Button("15", 425, 300, (btn_color)),
                  Button("20", 625, 300, (btn_color)),
                  Button("All or Nothing", 825, 300, (btn_color))]
        for round in rounds:
            round.draw(win)

        text = font.render("Ante", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 50))
        rounds = [Button("2", 25, 500, (btn_color)),
                  Button("5", 225, 500, (btn_color)),
                  Button("10", 425, 500, (btn_color)),
                  Button("20", 625, 500, (btn_color)),
                  Button("100", 825, 500, (btn_color))]
        for round in rounds:
            round.draw(win)

        text = font.render("Choose Away", 1, (font_color))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) + 150))
        rounds = [Button("1's", 200, 700, (btn_color)),
                  Button("2's", 400, 700, (btn_color)),
                  Button("3's", 600, 700, (btn_color)),
                  Button("4's", 200, 850, (btn_color)),
                  Button("5's", 400, 850, (btn_color)),
                  Button("6's", 600, 850, (btn_color))]
        for round in rounds:
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
    n.connect(g)
    dice_player.p = int(n.getP())
    n.send(dice_player)
    game = n.send(game_params)
    create_a_game(n, game, dice_player)


def create_a_game(n, game, dice_player):
    run = True
    clock = pygame.time.Clock()

    dice_player.p = game.active_players

    if dice_player.p == 0:
        dice_player.my_turn = True
        game = n.send(dice_player)

    while run:
        game = n.send(dice_player)
        clock.tick(60)
        font = pygame.font.SysFont(font_type, 48)
        if dice_player.my_turn is True and dice_player.finished is False:
            if dice_player.rolled is False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
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
                                dice_player.rolled = False
                                game = n.send(dice_player)
                    redrawWindow(win, game, dice_player)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
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
                                dice_player.remaining_rolls = 0
                                dice_player.finished = True
                            game = n.send(dice_player)
                            dice_player.rolled = False
                    redrawWindow(win, game, dice_player)
        elif dice_player.my_turn is False and dice_player.finished is False:
            game = n.send(dice_player)
            draw_wait_your_turn_window(win, game, dice_player)
            if game.my_turn_yet(dice_player):
                dice_player.my_turn = True
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
