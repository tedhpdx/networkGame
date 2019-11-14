from random import randint
import pygame
from network import Network

pygame.font.init()

width = 1000
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button1:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.roll = []

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("console", 18)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def get_roll(str):
    if len(str) > 18:
        return str[1:18].split(", ")
    else:
        return str[1:17].split(", ")


def redrawWindow(win, game, p, player_rolled, remaining_rolls):
    win.fill((128, 128, 128))
    if not (game.connected()):
        font = pygame.font.SysFont("console", 48)
        text = font.render("Waiting for Player...", 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("console", 36)
        text = font.render("Your roll", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        roll1 = game.get_player_move(0)
        roll2 = game.get_player_move(1)

        if player_rolled is False and remaining_rolls != 0:
            btns[0].draw(win)
        elif player_rolled is True:
            button_count = 0
            for choice in choice_buttons:
                if button_count < remaining_rolls + 1:
                    choice.draw(win)
                else:
                    break
                button_count += 1
        else:
            draw_game_over_window(win)
        if (roll1 != None and p == 0):
            roll = get_roll(roll1)
            render_rolls(roll, remaining_rolls)
            roll1 = None
        if (roll2 != None and p == 1):
            roll = get_roll(roll2)
            render_rolls(roll, remaining_rolls)
            roll2 = None
    pygame.display.update()


def draw_game_over_window(win):
    win.fill((128, 128, 128))
    font = pygame.font.SysFont("console", 48)
    text = font.render("Game over fool!", 1, (255, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

btns = [Button1("Roll", 50, 500, (0, 0, 0))]
choice_buttons = [Button1("Die #1", 0, 500, (0, 0, 0)),
                  Button1("Die #2", 200, 500, (0, 0, 0)),
                  Button1("Die #3", 400, 500, (0, 0, 0)),
                  Button1("Die #4", 600, 500, (0, 0, 0)),
                  Button1("Die #5", 800, 500, (0, 0, 0))]


def render_rolls(roll, remaining_rolls):
    font = pygame.font.SysFont("console", 36)
    text1 = font.render("Die #1: " + roll[0], 1, (0, 0, 0))
    win.blit(text1, (80, 250))
    if remaining_rolls > 0:
        text2 = font.render("Die #2: " + roll[1], 1, (0, 0, 0))
        win.blit(text2, (80, 300))
    if remaining_rolls > 1:
        text3 = font.render("Die #3: " + roll[2], 1, (0, 0, 0))
        win.blit(text3, (80, 350))
    if remaining_rolls > 2:
        text4 = font.render("Die #4: " + roll[3], 1, (0, 0, 0))
        win.blit(text4, (80, 400))
    if remaining_rolls > 3:
        text5 = font.render("Die #5: " + roll[4], 1, (0, 0, 0))
        win.blit(text5, (80, 450))
    text6 = font.render("Total :" + roll[5], 1, (0, 0, 0))
    win.blit(text6, (80, 600))

def main(away_choice):
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player ", player)
    player_total = 0
    player_rolled: bool = False
    remaining_rolls = 5

    while run:
        clock.tick(60)
        font = pygame.font.SysFont("console", 48)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game ln 107")
            break

        if game.bothWent():
            redrawWindow(win, game, player, player_rolled, remaining_rolls)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game ln 117")
                break
        if player_rolled is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if len(btn.roll) > 4:
                            player_total = btn.roll[5]
                        if btn.click(pos) and game.connected():
                            roll_dice(btn)
                            btn.roll.append(player_total)
                            n.send(btn.roll)
                            player_rolled = True
                            remaining_rolls -= 1
                        if remaining_rolls == -2:
                            run = False
                            break
                redrawWindow(win, game, player, player_rolled, remaining_rolls)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and player_rolled is True:
                    pos = pygame.mouse.get_pos()
                    for choice in choice_buttons:
                        if choice.click(pos) and game.connected():
                            if int(away_choice) != btn.roll[int(choice.text[5]) - 1]:
                                btn.roll[5] += btn.roll[int(choice.text[5]) - 1]
                            player_total = btn.roll[5]
                            n.send(btn.roll)
                            player_rolled = False
                redrawWindow(win, game, player, player_rolled, remaining_rolls)





def roll_dice(btn):
    btn.roll.clear()
    for i in range(5):
        btn.roll.append(randint(1, 6))


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    away_choice = -1

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("console", 24)
        text = font.render("Welcome to the dice game!", 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 200))
        text1 = font.render("Please choose your game", 1, (255, 0, 0))
        win.blit(text1, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2) - 100))
        btns1 = [Button1("1's away", 100, 600, (0, 0, 0)),
                 Button1("2's away", 300, 600, (0, 0, 0)),
                 Button1("3's away", 500, 600, (0, 0, 0)),
                 Button1("4's away", 100, 750, (0, 0, 0)),
                 Button1("5's away", 300, 750, (0, 0, 0)),
                 Button1("6's away", 500, 750, (0, 0, 0))]
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
                        # game start
                        print(btn.text)
                        away_choice = btn.text[0]
                        run = False
        pygame.display.update()
    main(away_choice)


while True:
    menu_screen()
