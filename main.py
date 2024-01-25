from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
from GameData import GameData
import requests
import re
import sys

show_warnings=False

# init colorama
init(autoreset=True)

def print_link(text, link):
    sys.stdout.write("\x1b]8;;" + link + "\x1b\\")
    sys.stdout.write(text)
    sys.stdout.write("\x1b]8;;\x1b\\")
    print() # line break

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
        soup = BeautifulSoup(response.text, 'html.parser')
        lowest_span = soup.find('span', class_ = "game-lowest-current-details")
        soup = BeautifulSoup(str(lowest_span.contents), 'html.parser') # another soup that gets only the lowest spans

        keyshop_price = soup.find('span', class_ = 'price-inner numeric').get_text(strip=True)
        keyshop_price = re.sub(r'[^\d,]', '', keyshop_price) # using regex to parse the number
        keyshop_price = keyshop_price.replace(',', '.')
        keyshop_price = float(keyshop_price)
        #

        # Official Price
        soup = BeautifulSoup(response.text, 'html.parser')
        official_span = soup.find('span', class_ = "price")
        soup = BeautifulSoup(str(official_span.contents), 'html.parser') # another soup that gets only the official price span

        official_price = soup.find('span', class_ = 'price-inner numeric').get_text(strip=True)
        official_price = re.sub(r'[^\d,]', '', official_price) # using regex to parse the number
        official_price = official_price.replace(',', '.')
        official_price = float(official_price)
        #

    except (requests.exceptions.RequestException, AttributeError, ValueError, KeyboardInterrupt) as e:
        if show_warnings: print(f'{Fore.YELLOW}Coming soon... - {game_name}')
        return 

    return GameData(game_name, keyshop_price, official_price, url)

def process_wishlist(wishlist_item):
    data = get_gamedata(wishlist_item)
    if data: 
        print(data, end="")
        print_link(data.game_name, data.url)

wishlists = scrap_wishlist(steamid=76561198164066871)

with ThreadPoolExecutor(max_workers=4) as exec:
    futures = [exec.submit(process_wishlist, wishlist) for wishlist in wishlists]

    for future in futures:
        future.result()