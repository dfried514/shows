# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the table from our database
class Like:
    def __init__( self , data ):
        self.user_id = data['user_id']
        self.show_id = data['show_id']
    # class method to save our class instance to the database
    @classmethod
    def insert_like(cls, data):
        query = "INSERT INTO shows_schema.likes ( user_id, show_id ) VALUES ( %(user_id)s , %(show_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('shows_schema').query_db( query, data )
    # class method to delete class instance from database
    @classmethod
    def delete_like(cls, data ):
        query = "DELETE FROM shows_schema.likes WHERE user_id=%(user_id)s AND show_id=%(show_id)s;"
        # data is a dictionary that will be passed into the delete method from server.py
        connectToMySQL('shows_schema').query_db( query, data )
    # class method to delete class instance with Show show_id from database
    @classmethod
    def delete_like_with_show_id(cls, show_id ):
        query = "DELETE FROM shows_schema.likes WHERE show_id='%s';" % (show_id)
        # data is a dictionary that will be passed into the delete method from server.py
        connectToMySQL('shows_schema').query_db( query )
    # class method to retrieve number of likes of Show with show_id
    @classmethod
    def get_num_likes_of_show(cls, show_id):
        query = "SELECT COUNT(*) AS 'count' FROM shows_schema.likes WHERE show_id='%s';" % (show_id)
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('shows_schema').query_db(query)
        # return instance of class
        if not results:
            return None
        return results[0]['count']
    