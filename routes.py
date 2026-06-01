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

    # grab profile_id from form
    profile_id = request.form['profile_id_input']

    try:
        profile_id = int(profile_id)
    except TypeError as e:
        print(f"Can't parse ID into int: {e}")


    fetch_service = FetchService()
    profile = fetch_service.fetch_steam_profile(profile_id)
    app_ids = fetch_service.get_wishlist_app_ids(profile_id)

    game_datas = []
    for id in app_ids:
        game_datas.append(fetch_service.fetch_game_data(id))
        
    # for data in game_datas:
        # if data: print(data.img_url)

    return render_template('index.html', game_datas=[x for x in game_datas if x is not None], profile=profile)
