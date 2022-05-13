from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", required=True, type=float, help="This field can not be empty")
    parser.add_argument("store_id", required=True, type=int, help="every item should belong to a store")

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()
        return {"item": "item not found"}, 404

    def post(self, name):

        if ItemModel.get_item_by_name(name):
            return {'message': "item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "an error has occurred"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "item has been deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.get_item_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price= data["price"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [list(map(lambda x: x.json(), ItemModel.query.all()))]}
