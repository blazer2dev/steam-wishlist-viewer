import os

from flask import Blueprint, render_template, request, flash, redirect, url_for
from fetch_service import FetchService
from dotenv import load_dotenv

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit', methods=['GET'])
def submit():

    load_dotenv()
    STEAM_API = os.getenv("STEAM_API")

    # grab profile_id from GET
    profile_id = request.args.get("id")

    fetch_service = FetchService()
    if profile_id.isdigit():
        profile_id = int(profile_id)
    else:
        profile_id = fetch_service.resolve_vanity_profile_id(profile_id, STEAM_API)

    profile = fetch_service.fetch_steam_profile(profile_id, STEAM_API)
    app_ids = fetch_service.get_wishlist_app_ids(profile_id)

    game_datas = fetch_service.fetch_all_game_data(app_ids)

    return render_template('index.html', game_datas=[x for x in game_datas if x is not None], profile=profile)