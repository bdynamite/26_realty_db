from datetime import datetime
from collections import defaultdict
import math

from flask import render_template, request, session, redirect, url_for
from app import app, db
from db_manager import Flats

MAX_PER_PAGE = 15


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:page>', methods=['GET', 'POST'])
def ads_list(page=1):
    districts = get_districts_from_sql()
    ads = get_data_from_db()
    pagination = get_pagination(page, len(ads))
    return render_template('ads_list.html', ads=ads[MAX_PER_PAGE * (page - 1):MAX_PER_PAGE * page],
                           districts=districts, pagination=pagination, result_page='')


@app.route('/query')
def query():
    session['args'] = dict(request.args)
    return redirect(url_for('result'))


@app.route('/result', methods=['GET', 'POST'])
@app.route('/result/<int:page>', methods=['GET', 'POST'])
def result(page=1):
    districts = get_districts_from_sql()
    parametres = session['args']
    ads = get_data_from_db(parametres)
    pagination = get_pagination(page, len(ads))
    return render_template('ads_list.html', ads=ads[MAX_PER_PAGE * (page - 1):MAX_PER_PAGE * page],
                           districts=districts, pagination=pagination, result_page='result/', **parametres)


def get_pagination(page, quantity):
    last_page = math.ceil(quantity / MAX_PER_PAGE)
    page_neighborhood = [page + x for x  in range(-3, 4) if 0 < page + x <= last_page]
    return {'active_page': page, 'pages_list': page_neighborhood}


def get_districts_from_sql():
    main_cities = ('Череповец', 'поселок городского типа Шексна', 'Вологда')
    districts = []
    def_dict = defaultdict(list)
    settlements = db.session.query(Flats.settlement).group_by(Flats.settlement).all()
    for settlement in settlements:
        city = settlement[0]
        if city in main_cities:
            districts.append(city)
        else:
            for word in city.split():
                if word[0].isupper():
                    def_dict[word[0]].append(city)
                    break
    districts.extend(sorted([city for city in def_dict.items()], key=lambda x: x[0]))
    return districts


def get_data_from_db(parametres=None):
    flats = db.session.query(Flats).filter(Flats.active==1)
    if parametres:
        if parametres['oblast_district'][0] not in ('all', ''):
            flats = flats.filter(Flats.settlement==parametres['oblast_district'][0])
        if parametres['min_price'][0]:
            flats = flats.filter(Flats.price>=int(parametres['min_price'][0]))
        if parametres['max_price'][0]:
            flats = flats.filter(Flats.price<=int(parametres['max_price'][0]))
        if 'new_building' in parametres:
            flats = flats.filter(Flats.under_construction==1 or datetime.now().year - Flats.construction_year < 3)
    flats = flats.all()
    return flats


if __name__ == "__main__":
    app.run()
