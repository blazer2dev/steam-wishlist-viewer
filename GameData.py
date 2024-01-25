from colorama import Back, Fore, Style

class GameData:
    def __init__(self, game_name, keyshop_price, official_price):
        self.game_name = game_name
        self.keyshop_price = keyshop_price
        self.official_price = official_price

    def __str__(self) -> str:
        return f'{Fore.CYAN}{self.keyshop_price}{Style.RESET_ALL} Keyshop - {Fore.GREEN}{self.official_price}{Style.RESET_ALL} Official - {self.game_name}'
