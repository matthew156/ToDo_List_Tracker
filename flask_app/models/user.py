from flask.helpers import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def add(cls, data):
        query = "INSERT INTO user(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('login_registration').query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL('login_registration').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL('login_registration').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])



    @staticmethod
    def validation(register):
        valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL('login_registration').query_db(query, register)
        if len(results)>=1:
            flash('Email already taken, Register')
        if not EMAIL_REGEX.match(register['email']):
            flash("Invalid Email!!!!")
        if len(register['first_name']) < 3:
            valid = False
            flash('Name must be 3 characters!') 
        if len(register['last_name']) < 3:
            valid = False
            flash('Name must be 3 characters!') 
        if len(register['email']) < 3:
            valid = False
            flash('Email must be 3 characters!')
        if len(register['password']) < 3:
            valid = False
            flash('Password must be 3 characters!') 
        if register['password'] != ['confirm_password']:
            flash('Passwords must Match!')
        return valid