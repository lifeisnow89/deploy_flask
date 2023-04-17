from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask_app.models import wine_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Wine:
    db = 'users'
    def __init__(self, data):
        self.id = data["wines_id"]
        self.wine_name = data["wine_name"]
        self.region = data["region"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.posted_by = None

    
    @classmethod
    def get_wine_w_user(cls, wines_id):
        data = {'wines_id' : wines_id}
        print('data_id' ,data)
        query = "SELECT * FROM wines LEFT JOIN users ON wines.user_id = users.user_id WHERE wines.wines_id = %(wines_id)s;"
        results = connectToMySQL('project_one').query_db(query, data)
        new_wine = cls(results[0])
        new_wine.posted_by = (results[0]['first_name'])
        return new_wine

    @classmethod
    def get_all_wines_with_user(cls):
        query = "SELECT * FROM wines LEFT JOIN users ON wines.user_id = users.user_id;"
        result = connectToMySQL('project_one').query_db(query, data)
        wines = []
        for row_in_db in result:
            wine = cls(row_in_db)
            user_data = {
                "id": row_in_db["users.id"],
                "first_name": row_in_db["first_name"],
                "wine_name": row_in_db["wine_name"]
            }
            wine.user = user.User(user_data)
            wine.append(wine)
        return wines

    @classmethod
    def get_one_w_user(cls, wines_id):
        query = "SELECT * FROM wines LEFT JOIN users ON wines.user_id = users.user_id WHERE wines.wines_id = %(id)s;"
        results = connectToMySQL('project_one').query_db(query,{'id':wines_id})
        print(results[0])
        wine = cls(results[0])
        wine.posted_by = results[0]['first_name']
        print(wine.posted_by)
        return wine

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM wines LEFT JOIN users ON wines.user_id = users.user_id;"
        results = connectToMySQL('project_one').query_db(query)
        print(results)
        wines = []
        for wine in results:
            new_wine = cls(wine)
            new_wine.posted_by = wine['first_name']
            wines.append(new_wine)
        return wines

    @classmethod
    def save(cls, form_data):
        query = "INSERT INTO wines (wine_name, region, description, user_id) VALUES (%(wine_name)s, %(region)s, %(description)s, %(user_id)s)"
        results = connectToMySQL('project_one').query_db(query, form_data)
        return results

    @classmethod
    def update(cls, form_data):
        query = "UPDATE wines SET wine_name = %(wine_name)s, region = %(region)s, description = %(description)s WHERE wines_id = %(wines_id)s;"
        results = connectToMySQL('project_one').query_db(query, form_data)
        return results

    @classmethod
    def delete(cls, wines_id):
        query = "DELETE FROM wines WHERE wines_id = %(wines_id)s"
        results = connectToMySQL('project_one').query_db(query, wines_id)
        return results

    @staticmethod
    def validate_wine(wine):
        is_valid = True
        if len(wine['wine_name']) < 3:
            flash("Wine Name must be at least 3 characters, all fields required.")
            is_valid = False
        if len(wine['region']) <3:
            flash("Wine region must be at least 3 characters, all fields required.")
            is_valid = False
        if len(wine['description']) < 3:
            flash("Description must be at least 3 characters, all fields required.")
            is_valid = False
        return is_valid