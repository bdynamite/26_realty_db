import json
import argparse
import os

from app import db


class Flats(db.Model):
    flat_id = db.Column(db.Integer, primary_key=True)
    has_balcony = db.Column(db.Boolean)
    oblast_district = db.Column(db.Text(120))
    construction_year = db.Column(db.Integer)
    description = db.Column(db.Text(1000))
    settlement = db.Column(db.Text(100))
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


def update_db(file_path):
    flats = get_json_data(file_path)
    for flat in flats:
        if not 'active' in flat:
            flat['active'] = True
        table_columns = list(db.Model.metadata.tables['flats'].columns)
        new_record = Flats(**{x.name: flat[x.name] for x in table_columns})
        db.session.add(new_record)
        db.session.commit()


if __name__ == '__main__':
    parser = create_parser()
    if parser.filepath:
        update_db(parser.filepath)
    else:
        create_db()


