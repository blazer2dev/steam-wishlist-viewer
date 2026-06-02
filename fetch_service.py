from concurrent.futures import ThreadPoolExecutor
from colorama import init
from game_data import GameData
from profile import Profile
from error_handling import throw_span_ex
import requests

class FetchService:

    def __init__(self):
        # init colorama
        init(autoreset=True)

    def resolve_vanity_profile_id(self, profile_id: str, steam_api) -> int:
        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={steam_api}&vanityurl={profile_id}"
    
        json = self.fetch_json(url)

        try:
            new_id = json["response"]["steamid"]
            return new_id
        except Exception as e:
            throw_span_ex(f"resolve_vanity_profile_id {e}")
            return 0

    def get_wishlist_app_ids(self, profile_id: int):
        url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={profile_id}"

        json = self.fetch_json(url)

        try:
            app_ids = [item["appid"] for item in json["response"]["items"]]
            return app_ids
        except Exception as e:
            throw_span_ex(f"get_wishlist_app_ids {e}")
            return []

    def fetch_game_data(self, app_id) -> GameData:
        fetch_details_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"

        json = self.fetch_json(fetch_details_url)

        if json == None:
            throw_span_ex("fetch_game_data json is None")
            return None

        game = json[str(app_id)]["data"]
        name = game["name"]
        
        try:
            price = game["price_overview"]["final"] / 100
        except:
            price = "---" # free2play or unreleased

        url = f'https://gg.deals/steam/app/{app_id}/'
        image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
        gd = GameData(name, 0, price, url, image_url)

        print(gd) # console
        return gd
    
    def fetch_all_game_data(self, app_ids):
        try:
            with ThreadPoolExecutor(max_workers=10) as exec:
                results = list(exec.map(self.fetch_game_data, app_ids))
                return [r for r in results if r is not None]
        except Exception as e:
            throw_span_ex(f"fetch_all_game_data {e}")
            return []

    def fetch_steam_profile(self, profile_id, steam_api) -> Profile:
        fetch_prof_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_api}&steamids={profile_id}"

        json = self.fetch_json(fetch_prof_url)

        new_prof = Profile()
        try:
            json_profile = json["response"]["players"][0]

            new_prof.img_url = json_profile["avatarfull"]
            new_prof.name = json_profile["personaname"]
            new_prof.url = f"https://steamcommunity.com/profiles/{profile_id}/"
        except Exception as e:
            throw_span_ex(f"fetch_steam_profile {e}")
            return None
        
        return new_prof
    
    def fetch_json(self, url):
        try:
            url_data = requests.get(url, timeout=10)
            url_data.raise_for_status()
            return url_data.json()
        except Exception as e:
            throw_span_ex(f"fetch_json {e}")
            return None