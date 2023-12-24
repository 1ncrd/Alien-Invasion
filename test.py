from enum import Enum, auto


class MenuItem(Enum):
    Start_Game = 0
    Quit = auto()

    @property
    def name_to_render(self):
        return ' '.join(self.name.split('_'))


menu_items = Enum("MenuItems", ["Start Game", "Quit"], start=0)

for i in MenuItem:
    print(i.name_to_render, i.value)

