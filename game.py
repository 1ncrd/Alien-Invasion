import pygame

from menu_interface import MenuInterface
from settings import *
from interface import Interface


class Game:

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)

        current_interface: Interface = MenuInterface()

        while True:
            current_interface.display()
            pygame.display.update()
            current_interface = current_interface.handle_input()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
