from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Show:
    db_name = 'blank_db'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.network = db_data['network']
        self.release_date = db_data['release_date']
        self.description = db_data['description']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO shows (title, network, release_date, description, user_id) VALUES (%(title)s,%(network)s,%(release_date)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_shows = []
        for row in results:
            all_shows.append( cls(row) )
        return all_shows

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters.","show")
        if len(show['network']) < 3:
            is_valid = False
            flash("Network name must be at least 3 characters.","show")
        if show['release_date'] == "":
            is_valid = False
            flash("Please enter a release date.","show")
        if len(show['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters.","show")
        return is_valid