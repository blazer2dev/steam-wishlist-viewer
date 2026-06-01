from flask import Blueprint, render_template, request
from fetch_service import FetchService
from game_data import GameData
from profile import Profile

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit', methods=['POST', 'GET'])
def submit():
    profile_id = request.form['profile_id_input']
    template_prof = Profile("Profesorek23", "https://avatars.cloudflare.steamstatic.com/ada818f27a841be80f9159dde619f958016ff0f2_full.jpg", "https://avatars.cloudflare.steamstatic.com/ada818f27a841be80f9159dde619f958016ff0f2_full.jpg")
    
    # for debug layout testing
    layout_test = False

    if layout_test:
        fake_data = GameData("Wally and the FANTASTIC PREDATORS", 53.99, 53.99, 'https://gg.deals/game/Wally-and-the-FANTASTIC-PREDATORS/', img_url='https://img.gg.deals/1d/eb/31621b11b2574a269eda6e3b5fd0d9e081da_307xr176.jpg')
        fake_datas = []
        for i in range(100):
            fake_datas.append(fake_data)
        return render_template('index.html', game_datas=fake_datas, profile=template_prof)

    try:
        profile_id = int(profile_id)
    except TypeError as e:
        print(f"Can't parse ID into int: {e}")

    scraper = FetchService()

    app_ids = scraper.get_wishlist_app_ids(profile_id)

    game_datas = []
    for id in app_ids:
        game_datas.append(scraper.fetch_game_data(id))
        
    for data in game_datas:
        if data: print(data.img_url)

    return render_template('index.html', game_datas=[x for x in game_datas if x is not None], profile=template_prof)
