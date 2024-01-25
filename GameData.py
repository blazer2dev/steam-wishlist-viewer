class GameData:
    def __init__(self, game_name, keyshop_price, official_price):
        self.game_name = game_name
        self.keyshop_price = keyshop_price
        self.official_price = official_price

    def __str__(self) -> str:
        return f'{self.keyshop_price} Keyshop - {self.official_price} Official - {self.game_name}'
