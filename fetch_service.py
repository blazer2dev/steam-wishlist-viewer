from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
from game_data import GameData
from profile import Profile
import requests

class FetchService:

    def __init__(self):
        # init colorama
        init(autoreset=True)

    def resolve_vanity_profile_id(self, profile_id: str, steam_api) -> int:
        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={steam_api}&vanityurl={profile_id}"
        url_data = requests.get(url)

        url_data.raise_for_status()

        json = url_data.json()

        return json["response"]["steamid"]

    def get_wishlist_app_ids(self, profile_id: int):
        url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={profile_id}"
        url_data = requests.get(url)

        url_data.raise_for_status()

        json = url_data.json()

        app_ids = [item["appid"] for item in json["response"]["items"]]

        return app_ids

    def fetch_game_data(self, app_id) -> GameData:
        url = f'https://gg.deals/steam/app/{app_id}/'

        image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
        return GameData(app_id, 12, 134, url, image_url)
    
    def fetch_steam_profile(self, profile_id) -> Profile:
        name = str(profile_id)
        url = f"https://steamcommunity.com/profiles/{profile_id}/"
        img_url = f"https://avatars.steamstatic.com/{profile_id}_medium.jpg"
        return Profile(name, img_url, url)


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