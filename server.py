from datetime import datetime
import math

from flask import render_template, request
from app import app, db
from db_manager import Flat

MAX_PER_PAGE = 15


@app.route('/', methods=['GET'])
@app.route('/<int:page>', methods=['GET'])
def ads_list(page=1):
    districts = get_districts_from_sql()
    parameters = request.args
    ads = get_data_from_db(parameters)
    pagination = get_pagination(page, len(ads))
    return render_template('ads_list.html', ads=ads[MAX_PER_PAGE * (page - 1):MAX_PER_PAGE * page],
                           districts=districts, pagination=pagination, args=parameters)


def get_pagination(page, quantity):
    last_page = math.ceil(quantity / MAX_PER_PAGE)
    page_neighborhood = [page + x for x  in range(-3, 4) if 0 < page + x <= last_page]
    return {'active_page': page, 'pages_list': page_neighborhood}


def get_districts_from_sql():
    settlements = db.session.query(Flat.settlement).group_by(Flat.settlement).all()
    return [db_item[0] for db_item in settlements]


def get_data_from_db(parameters):
    flats = db.session.query(Flat).filter(Flat.active==1)
    if parameters:
        if parameters['oblast_district'] not in ('all', ''):
            flats = flats.filter(Flat.settlement==parameters['oblast_district'])
        if parameters['min_price']:
            flats = flats.filter(Flat.price>=int(parameters['min_price']))
        if parameters['max_price']:
            flats = flats.filter(Flat.price<=int(parameters['max_price']))
        if 'new_building' in parameters:
            flats = flats.filter(Flat.under_construction==1 or datetime.now().year - Flat.construction_year < 3)
    flats = flats.all()
    return flats


if __name__ == "__main__":
    app.run()
