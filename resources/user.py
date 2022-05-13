import sqlite3
from flask_restful import Resource, reqparse

# from ..models.user import UserModel
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, help="this field can not be empty")
    parser.add_argument("password", type=str, help="this field can not be empty")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_user_by_username(data["username"]):
            return {"message": "user has already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "user created successfully"}
