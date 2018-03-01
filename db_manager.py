import json
import argparse
import os

from app import db


class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    has_balcony = db.Column(db.Boolean)
    oblast_district = db.Column(db.Text(120), index=True)
    construction_year = db.Column(db.Integer)
    description = db.Column(db.Text(1000))
    settlement = db.Column(db.Text(100), index=True)
    rooms_number = db.Column(db.Integer)
    living_area = db.Column(db.Float)
    address = db.Column(db.Text(100))
    price = db.Column(db.Integer)
    premise_area = db.Column(db.Float)
    under_construction = db.Column(db.Boolean)
    active = db.Column(db.Boolean)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', type=str)
    return parser.parse_args()


def create_db():
    db.create_all()


def get_json_data(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as file_handler:
        return json.load(file_handler)


def add_record_in_db(flat):
    if 'active' not in flat:
        flat['active'] = True
    table_columns = list(db.Model.metadata.tables['flats'].columns)
    new_record = Flat(**{x.name: flat[x.name] for x in table_columns})
    db.session.add(new_record)
    db.session.commit()


def check_inactive_records(flats_id):
    db_id = [db_item[0] for db_item in db.session.query(Flat.id).all()]
    inactive_id = set(db_id).difference(set(flats_id))
    inactive_flats = db.session.query(Flat).filter(Flat.id.in_(inactive_id)).filter_by(active=True).all()
    for flat in inactive_flats:
        flat.active = False
    db.session.commit()


def update_db(file_path):
    flats = get_json_data(file_path)
    [add_record_in_db(flat) for flat in flats]
    check_inactive_records([flat['id'] for flat in flats])


if __name__ == '__main__':
    args = create_parser()
    if args.filepath:
        update_db(args.filepath)
    else:
        create_db()
