from colorama import Fore, Style

class GameData:
    def __init__(self, game_name, keyshop_price, official_price, url, img_url):
        self.game_name = game_name
        self.keyshop_price = keyshop_price
        self.official_price = official_price
        self.url = url
        self.img_url = img_url

    def __str__(self) -> str:
        return f'{Fore.YELLOW}{self.keyshop_price}{Style.RESET_ALL} Keyshop - {Fore.GREEN}{self.official_price}{Style.RESET_ALL} Official - '
