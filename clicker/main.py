from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import NumericProperty, DictProperty


Window.size = (1200, 800)


# =========================
# Главное меню
# =========================

class MenuScreen(Screen):

    def start_game(self):
        self.manager.current = "game"


# =========================
# Игровая страница
# =========================

class GameScreen(Screen):

    clicks = NumericProperty(0)
    level = NumericProperty(1)
    level_targets = DictProperty({
        1: 10,
        2: 15,
        3: 30,
        4: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1
    })

    MAX_LEVEL = 10

    def next_level(self):
        target = self.level_targets[self.level]

        if self.clicks >= target:
            # Последний уровень пройден -> экран победы
            if self.level >= self.MAX_LEVEL:
                self.manager.get_screen("win").final_level = self.level
                self.manager.current = "win"
                return

            self.level += 1
            self.clicks = 0
            self.ids.stone.reset(self.level_targets[self.level])

    def back_to_menu(self):
        self.manager.current = "menu"

    def on_hit(self):
        self.clicks += 1
        self.next_level()


# =========================
# Камень
# =========================

class Stone(Button):

    def __init__(self, hp=10, **kwargs):
        self.hp = hp
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        # Ищем экран, в котором лежит камень
        parent = self.parent
        while parent and not isinstance(parent, Screen):
            parent = parent.parent
        self.game_screen = parent

        self.base_size = tuple(self.size)
        self.max_hp = self.hp
        super().on_kv_post(base_widget)

    def click(self):
        self.hp -= 1
        k = max(self.hp / self.max_hp, 0.2)

        self.size = (int(self.base_size[0] * k), int(self.base_size[1] * k))
        self.game_screen.on_hit()

    def reset(self, hp):
        self.size = self.base_size
        self.hp = hp
        self.max_hp = hp


# =========================
# Победная страница
# =========================

class WinScreen(Screen):
    final_level = NumericProperty(10)

    def back_to_menu(self):
        # Сбрасываем игру, чтобы можно было сыграть заново
        game = self.manager.get_screen("game")
        game.level = 1
        game.clicks = 0
        game.ids.stone.reset(game.level_targets[1])

        self.manager.current = "menu"


# =========================
# Запуск приложения
# =========================

class ClickerApp(App):

    def build(self):
        self.title = "Каменный кликер"

        screen_manager = ScreenManager()
        screen_manager.add_widget(MenuScreen(name="menu"))
        screen_manager.add_widget(GameScreen(name="game"))
        screen_manager.add_widget(WinScreen(name="win"))

        return screen_manager


if __name__ == "__main__":
    ClickerApp().run()
    