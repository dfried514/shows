# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# model the class after the table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    # class method to save our class instance to the database
    @classmethod
    def get_user_with_email(cls, email):
        query = "SELECT * FROM shows_schema.users WHERE email='%s';" % email
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('shows_schema').query_db(query)
        # return instance of class
        if not results:
            return None
        print('RESULTS', results[0])
        return cls(results[0])
    # class method to get full user name who posted a show
    @classmethod 
    def get_user_name_with_show_id(cls, show_id):
        query = "SELECT CONCAT(users.first_name, ' ', users.last_name) AS name FROM shows_schema.users JOIN shows_schema.shows ON shows_schema.shows.user_id = users.id WHERE shows_schema.shows.id='%s';" % (show_id)
        
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('shows_schema').query_db(query)
        # return instance of class
        if not results:
            return None
        return results[0]['name']
    # class method to save our class instance to the database
    @classmethod
    def insert_user(cls, data ):
        query = "INSERT INTO shows_schema.users ( first_name, last_name, email, password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s, %(email)s , %(password)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('shows_schema').query_db( query, data )
    @staticmethod
    def validate_user(data):
        print('data', data)
        email_regex = '^\w+@\w+\.[a-zA-Z]{2,}$'
            
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name is less than 3 characters long")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name is less than 3 characters long")
            is_valid = False
        if not re.match(email_regex, data['email']):
            flash("Email is not valid")
            is_valid = False 
        if not data['password'] == data['password2']:
            flash("Passwords don't match")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password is less than 8 characters long")
            is_valid = False 
        return is_valid
    