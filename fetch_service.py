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
    
        json = self.fetch_json(url)

        return json["response"]["steamid"]

    def get_wishlist_app_ids(self, profile_id: int):
        url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={profile_id}"

        json = self.fetch_json(url)

        app_ids = [item["appid"] for item in json["response"]["items"]]

        return app_ids

    def fetch_game_data(self, app_id) -> GameData:
        fetch_details_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"

        json = self.fetch_json(fetch_details_url)

        game = json[str(app_id)]["data"]
        name = game["name"]
        
        try:
            price = game["price_overview"]["final"] / 100
        except:
            price = "---" # free2play or unreleased
            pass

        url = f'https://gg.deals/steam/app/{app_id}/'
        image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
        gd = GameData(name, 0, price, url, image_url)

        print(gd.__str__()) # console
        return gd
    
    def fetch_all_game_data(self, app_ids):
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.fetch_game_data, app_ids))
        return results

    def fetch_steam_profile(self, profile_id, steam_api) -> Profile:
        fetch_prof_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_api}&steamids={profile_id}"

        json = self.fetch_json(fetch_prof_url)

        prof = json["response"]["players"][0]
        img_url = prof["avatarfull"]

        name = prof["personaname"]
        url = f"https://steamcommunity.com/profiles/{profile_id}/"
        return Profile(name, img_url, url)
    
    def fetch_json(self, url):
        url_data = requests.get(url, timeout=10)
        url_data.raise_for_status()

        return url_data.json()