from flask import Blueprint, render_template, request
import requests
from wishlistScraper import WishlistScraper

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit', methods=['POST'])
def submit():
    steamid = request.form['steamid_input']

    try:
        steamid = int(steamid)
    except TypeError as e:
        print(f"Can't parse ID into int: {e}")

    scraper = WishlistScraper()
    wishlists = scraper.scrap_wishlist(steamid)
    game_datas = []
    for wishlist in wishlists:
        game_datas.append(scraper.get_gamedata(wishlist))
        
    for data in game_datas:
        if data: print(data.img_url)

    return render_template('index.html', game_datas=[x for x in game_datas if x is not None])