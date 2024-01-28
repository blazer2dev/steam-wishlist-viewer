from flask import Blueprint, render_template, request
from wishlistScraper import WishlistScraper
from GameData import GameData

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit', methods=['POST'])
def submit():
    steamid = request.form['steamid_input']

    fake_data = GameData("bobas", 12312, 123132, 'https://img.gg.deals/52/c2/d98a5c9eac66dfb7eb44f998b5751e2f6390_307xr176.jpg', 'https://img.gg.deals/52/c2/d98a5c9eac66dfb7eb44f998b5751e2f6390_307xr176.jpg')
    fake_datas = []
    for i in range(100):
        fake_datas.append(fake_data)
    return render_template('index.html', game_datas=fake_datas)

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