from random import randint
import pygame
from network import Network
from player import Player
from button import Button

pygame.font.init()

width = 1000
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


roll_btn = Button("Roll", 50, 500, (0, 0, 0), 0)
choice_buttons = [Button("Die #1", 0, 500, (0, 0, 0), 0),
                  Button("Die #2", 200, 500, (0, 0, 0), 1),
                  Button("Die #3", 400, 500, (0, 0, 0), 2),
                  Button("Die #4", 600, 500, (0, 0, 0), 3),
                  Button("Die #5", 800, 500, (0, 0, 0), 4)]
finish_btn = Button("Finish Round", 50, 500, (0, 0, 0), 0)


def redrawWindow(win, game, dice_player):
    win.fill((128, 128, 128))
    if not (game.connected()):
        font = pygame.font.SysFont("console", 48)
        text = font.render("Waiting for Player...", 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("console", 36)
        text = font.render("Your roll", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponent", 1, (0, 255, 255))
        win.blit(text, (380, 200))
        opponent = game.get_opponent_name(dice_player)
        text = font.render(opponent, 1, (0, 255, 255))
        win.blit(text, (380, 400))

        if dice_player.rolled is False and dice_player.remaining_rolls != 0:
            if dice_player.remaining_rolls == 1:
                finish_btn.draw(win)
            else:
                roll_btn.draw(win)
            render_total(dice_player)
        elif dice_player.rolled is True and dice_player.remaining_rolls != 0:
            button_count = 0
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
    font = pygame.font.SysFont("console", 36)
    text1 = font.render("Die #1: " + str(dice_player.roll[0]), 1, (0, 0, 0))
    win.blit(text1, (80, 250))
    if dice_player.remaining_rolls > 1:
        text2 = font.render("Die #2: " + str(dice_player.roll[1]), 1, (0, 0, 0))
        win.blit(text2, (80, 300))
    if dice_player.remaining_rolls > 2:
        text3 = font.render("Die #3: " + str(dice_player.roll[2]), 1, (0, 0, 0))
        win.blit(text3, (80, 350))
    if dice_player.remaining_rolls > 3:
        text4 = font.render("Die #4: " + str(dice_player.roll[3]), 1, (0, 0, 0))
        win.blit(text4, (80, 400))
    if dice_player.remaining_rolls > 4:
        text5 = font.render("Die #5: " + str(dice_player.roll[4]), 1, (0, 0, 0))
        win.blit(text5, (80, 450))
    render_total(dice_player)


def render_total(dice_player):
    font = pygame.font.SysFont("console", 36)
    text6 = font.render("Total :" + str(dice_player.roll_total), 1, (0, 0, 0))
    win.blit(text6, (80, 600))


def draw_game_over_window(win, game, dice_player):
    win.fill((128, 128, 128))
    font = pygame.font.SysFont("console", 48)
    text = font.render("Game over fool!", 1, (255, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    text = font.render("Your Score: " + str(dice_player.roll_total), 1, (255, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))
    if game.finished():
        winner = game.get_winner()
        if winner.result["push"] is True:
            text = font.render("Push!", 1, (255, 0, 0))
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))
        elif winner.p == dice_player.p:
            text = font.render("You Win!", 1, (255, 0, 0))
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 300))
        else:
            text = font.render("You Lose!", 1, (255, 0, 0))
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 400))
        pygame.display.update()
        dice_player.reset()
        pygame.time.wait(1000)
        win.fill((128, 128, 128))
        create_a_game(dice_player)


    else:
        text = font.render("Waiting on them fools!", 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 200))
    pygame.display.update()


def draw_wait_your_turn_window(dice_player):
    font = pygame.font.SysFont("console", 48)
    text = font.render("Waiting!", 1, (255, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    pygame.display.update()


def create_a_game(dice_player):
    run = True
    clock = pygame.time.Clock()
    n = Network()
    dice_player.p = int(n.getP())
    away_choice = '2'
    if dice_player.p == 0:
        dice_player.my_turn = True

    while run:
        clock.tick(60)
        font = pygame.font.SysFont("console", 48)
        try:
            dice_player.pickle_string = "get"
            game = n.send(dice_player)
        except:
            run = False
            print("Couldn't get game")
            break
        if dice_player.my_turn is True and dice_player.finished is False:
            if dice_player.rolled is False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if roll_btn.click(pos) and game.connected():
                            dice_player.roll_dice()
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
                    if event.type == pygame.MOUSEBUTTONDOWN and dice_player.rolled is True:
                        pos = pygame.mouse.get_pos()
                        for choice in choice_buttons:
                            if choice.click(pos) and game.connected():
                                dice_player.get_points(away_choice, choice.value)
                                game = n.send(dice_player)
                                dice_player.rolled = False
                    redrawWindow(win, game, dice_player)
        elif dice_player.my_turn is False and dice_player.finished is False:
            draw_wait_your_turn_window(dice_player)
            if game.my_turn_yet():
                dice_player.my_turn = True
        elif dice_player.finished is True:
            draw_game_over_window(win, game, dice_player)


def welcome_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("console", 24)
        text = font.render("Welcome to the dice game!", 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text1 = font.render("Press Any Key", 1, (255, 0, 0))
        win.blit(text1, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                run = False

        pygame.display.update()
    player_setup()


def player_setup():
    run = True
    clock = pygame.time.Clock()
    player_cash = 500

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("console", 24)
        text = font.render("Hi there!", 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text1 = font.render("Please choose your character", 1, (255, 0, 0))
        win.blit(text1, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 100))
        btns1 = [Button("Tex", 100, 600, (0, 0, 0)),
                 Button("Sally", 300, 600, (0, 0, 0)),
                 Button("Floyd", 500, 600, (0, 0, 0)),
                 Button("Amber", 100, 750, (0, 0, 0)),
                 Button("Arnold", 300, 750, (0, 0, 0)),
                 Button("Generate $$$", 500, 750, (0, 0, 0))]
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
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("console", 24)
        text = font.render("Game Setup", 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text = font.render("Hello " + dice_player.name, 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 400))
        text = font.render("You Have $" + str(dice_player.cash), 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 300))
        btns1 = [Button("Join Game", 100, 600, (0, 0, 0)),
                 Button("Create A Game", 300, 600, (0, 0, 0))]
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
                            pass
                        if btn.text == "Create A Game":
                            pass
                        run = False
        pygame.display.update()
    create_a_game(dice_player)

while True:
    welcome_screen()
