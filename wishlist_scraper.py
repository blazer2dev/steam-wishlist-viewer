from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
from game_data import GameData
import requests
import re

class WishlistScraper:

    def __init__(self):
        # warnings like - game is still coming soon or if we can't parse the html etc
        self.show_warnings=True

        # init colorama
        init(autoreset=True)

    def get_wishlist_app_ids(self, profile_id: int):
        url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={profile_id}"
        url_data = requests.get(url)

        url_data.raise_for_status()

        json = url_data.json()

        app_ids = [item["appid"] for item in json["response"]["items"]]

        return app_ids

    def fetch_game_data(self, app_id) -> GameData:
        url = f'https://gg.deals/steam/app/{app_id}/'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            print(url)
            
            # Keyshop Price
            # soup = BeautifulSoup(response.text, 'html.parser')
            # lowest_span = soup.find('span', class_ = "game-lowest-current-details")
            # soup = BeautifulSoup(str(lowest_span.contents), 'html.parser') # another soup that gets only the lowest spans

            # keyshop_price = soup.find('span', class_ = 'price-inner numeric').get_text(strip=True)
            # keyshop_price = re.sub(r'[^\d,]', '', keyshop_price) # using regex to parse the number
            # keyshop_price = keyshop_price.replace(',', '.')
            # keyshop_price = float(keyshop_price)
            #

            # Official Price
            # soup = BeautifulSoup(response.text, 'html.parser')
            # official_span = soup.find('span', class_ = "price")
            # soup = BeautifulSoup(str(official_span.contents), 'html.parser') # another soup that gets only the official price span

            # official_price = soup.find('span', class_ = 'price-inner numeric').get_text(strip=True)
            # official_price = re.sub(r'[^\d,]', '', official_price) # using regex to parse the number
            # official_price = official_price.replace(',', '.')
            # official_price = float(official_price)
            #

            # Image URL
            # soup = BeautifulSoup(response.text, 'html.parser')
            # img_div = soup.find('div', class_ = "d-flex flex-align-center game-info-image platform-ribbon-container")
            # soup = BeautifulSoup(str(img_div.contents), 'html.parser') # another soup that gets only the official price span

            # img_url = soup.find('img').get('src')
            #
            

        except (requests.exceptions.RequestException, AttributeError, ValueError, KeyboardInterrupt) as e:
            if self.show_warnings: print(f'{Fore.YELLOW}Coming soon... - {app_id}')
            return 

        #return GameData(app_id, keyshop_price, official_price, url, img_url)
        return GameData(app_id, 12, 134, url, url)

    #def process_wishlist(self, wishlist_item):
        data = self.fetch_game_data(wishlist_item)
        if data: 
            print(data, end="")
            self.print_link(data.game_name, data.url)

    #def enable_threads(self, wishlists):
        with ThreadPoolExecutor(max_workers=4) as exec:
            futures = [exec.submit(self.process_wishlist, wishlist) for wishlist in wishlists]
            
        for future in futures:
            future.result()