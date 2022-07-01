# import the function that will return an instance of a connection
from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# model the class after the table from our database
class Show:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    # class method to save our class instance to the database
    @classmethod
    def get_show_with_id(cls, id):
        query = "SELECT * FROM shows_schema.shows WHERE id='%s';" % (id)
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('shows_schema').query_db(query)
        # return instance of class
        if not results:
            return None
        return cls(results[0])
    # shows that are liked by User with user_id
    @classmethod
    def get_liked_shows(cls, user_id):
        query = "SELECT * FROM shows_schema.shows JOIN shows_schema.likes ON shows_schema.likes.show_id = shows_schema.shows.id WHERE shows_schema.likes.user_id=%s;" % (user_id)
        
        results = connectToMySQL('shows_schema').query_db(query)
        # Create an empty list to append our instances of rows
        rows = []
        print('results, get_liked_shows', results)
        if not results:
            return rows
        # Iterate over the db results and create class instances with cls.
        for row in results:
            rows.append( cls(row) )
        print('rows, get_liked_shows', rows)
        return rows
    # shows that are not liked by User with user_id
    @classmethod 
    def get_not_liked_shows(cls, user_id):
        query = "SELECT * FROM shows_schema.shows WHERE shows_schema.shows.id NOT IN (SELECT shows_schema.shows.id FROM shows_schema.shows JOIN shows_schema.likes ON shows_schema.likes.show_id = shows_schema.shows.id WHERE shows_schema.likes.user_id=%s);" % (user_id)
        
        results = connectToMySQL('shows_schema').query_db(query)
        # Create an empty list to append our instances of rows
        rows = []
        if not results:
            return rows
        # Iterate over the db results and create class instances with cls.
        for row in results:
            rows.append( cls(row) )
        return rows
    # class method to save our class instance to the database
    @classmethod
    def insert_show(cls, data ):
        query = "INSERT INTO shows_schema.shows ( title, network, release_date, description, user_id, created_at, updated_at ) VALUES ( %(title)s , %(network)s , %(release_date)s , %(description)s , %(user_id)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('shows_schema').query_db( query, data )
    # class method to update our class instance to the database
    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows_schema.shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, user_id = %(user_id)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL('shows_schema').query_db( query, data )
        # data is a dictionary that will be passed into the save method from server.py
    @classmethod
    def delete_show(cls, id ):
        query = "DELETE FROM shows_schema.shows WHERE id = '%s';" % (id)
        connectToMySQL('shows_schema').query_db( query )
    # class method to return a class instance with no values, a dummy instance
    @classmethod
    def get_dummy_show(cls):
        dummy_data = {
            'id': '',
            'title': '',
            'network': '',
            'release_date': '',
            'description': '',
            'user_id': '',
            'created_at': '',
            'updated_at': ''
        }
        return cls(dummy_data)
    @staticmethod
    # validate the data
    def validate_show(data):
        print('data', data)
            
        is_valid = True
        if len(data['title']) < 3:
            flash("Title is less than 3 characters long")
            is_valid = False
        if len(data['network']) < 3:
            flash("Network is less than 3 characters long")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description is less than 3 characters long")
            is_valid = False
        if len(data['release_date']) == 0:
            flash("Release date must be present")
            is_valid = False
        if len(data['user_id']) == 0:
            flash("User id is missing")
            is_valid = False
        return is_valid
