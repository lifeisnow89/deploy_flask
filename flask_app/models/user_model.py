from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import wine_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

class User:
    db = 'wines'
    def __init__(self, data):
        self.id = data["user_id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def save(cls, request_data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL('project_one').query_db(query, request_data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('project_one').query_db(query)
        users = []
        for d in results:
            users.append( cls(d) )
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('project_one').query_db(query,data)
        if len(results) < 1:
            return False
        print (results[0])
        return cls(results[0])

    @classmethod
    def get_info(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s, password = %(password)s;"
        results = connectToMySQL('project_one').query_db(query,data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('project_one').query_db(query,data)
        return cls(results[0])

        @classmethod
        def get_by_name(cls, data):
            query = "SELECT * FROM users WHERE first_name = %(first)s;"
            results = connectToMySQL('project_one').query_db(query,data)
            return cls(results[0])

    @staticmethod
    def validate_user(register_form):
        print(register_form)
        is_valid = True
        if len(register_form['first_name']) < 2:
            flash("First Name must be at least 2 characters.", "register")
            is_valid = False
        if len(register_form['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", "register")
            is_valid = False
        if len(register_form['email']) >= 1:
            flash("Email already taken", "register")
        if not EMAIL_REGEX.match(register_form['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(register_form['password']) < 8:
            flash("Password must be 8 characters or greater.", "register")
            is_valid = False
        if register_form['password'] != register_form['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(login_form):
        print(login_form)
        is_valid = True
        data = { 
            "email" : login_form["email"], 
            "password" : pw_hash
            }
        user_in_db = User.get_info(data)
        if not user_in_db:
            is_valid = False
            flash("Invalid Email/Password", "login")
        if not bcrypt.check_password_hash(user_in_db.password, login_form['password']):
            is_valid = False
            flash("Invalid Email/Password", "login")
        return is_valid

    @classmethod
    def save(cls, request_data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL('project_one').query_db(query, request_data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('project_one').query_db(query)
        users = []
        for d in results:
            users.append( cls(d) )
        return users

    @classmethod
    def get_one(cls, user_id):
        query = "SELECT * FROM users WHERE users_id = %(user_id)s;"
        results = connectToMySQL('project_one').query_db(query,user_id)
        user = User(results[0])
        return user


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('project_one').query_db(query,data)
        if len(results) < 1:
            return False
        print (results[0])
        return cls(results[0])

