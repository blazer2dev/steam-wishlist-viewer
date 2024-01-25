from bs4 import BeautifulSoup
import requests
import re
from concurrent.futures import ThreadPoolExecutor

from GameData import GameData


def scrap_wishlist(steamid):
    page_number = 0
    games_list = []
    while True:
        url = f'https://store.steampowered.com/wishlist/profiles/{steamid}/wishlistdata/?p={page_number}'
        page = requests.get(url).json()

        if not page:
            break

        games_list.extend(value['name'] for value in page.values())
        page_number += 1
    return sorted(games_list)


def get_gamedata(game_name) -> GameData:
    url = f'https://gg.deals/game/{game_name.replace(' ', '-').replace(':','')}/'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Keyshop Price
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            lowest_span = soup.find('span', class_ = "game-lowest-current-details")
            soup = BeautifulSoup(str(lowest_span.contents), 'html.parser') # another soup that gets only the lowest spans
        except AttributeError as a:
            print(f"We can't get data for this game {game_name}")
            return

        keyshop_price = soup.find('span', class_ = 'price-inner numeric').get_text(strip=True)
        keyshop_price = re.sub(r'[^\d,]', '', keyshop_price) # using regex to parse the number
        keyshop_price = keyshop_price.replace(',', '.')
        keyshop_price = float(keyshop_price)
        #

        # Official Price
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            official_span = soup.find('span', class_ = "price")
            soup = BeautifulSoup(str(official_span.contents), 'html.parser') # another soup that gets only the official price span
        except AttributeError as a:
            print(f"We can't get data for this game {game_name}")
            return

        official_price = soup.find('span', class_ = 'price-inner numeric').get_text(strip=True)
        official_price = re.sub(r'[^\d,]', '', official_price) # using regex to parse the number
        official_price = official_price.replace(',', '.')
        official_price = float(official_price)
        #

    except requests.exceptions.RequestException as e:
        print(f'Error fetching HTML data - {game_name}')
        return 

    return GameData(game_name, keyshop_price, official_price)

def process_wishlist(wishlist_item):
    data = get_gamedata(wishlist_item)
    if data: print(data)

wishlists = scrap_wishlist(steamid=76561198164066871)

with ThreadPoolExecutor(max_workers=4) as exec:
    futures = [exec.submit(process_wishlist, wishlist) for wishlist in wishlists]

    for future in futures:
        future.result()