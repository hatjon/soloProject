from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#Creation of the class of Post
class Post:
    db_name='usersTest' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['id'],
        self.content = data['content'],
        self.image = data['image'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #Method to  query the database and 
    #get all the posts, together with the creator's id and email,
    # and the number of likes

    @classmethod
    def getAllPosts(cls):
        query= 'SELECT posts.id, content,image, COUNT(likes.id) as likesNr, users.id as creator_id, email FROM posts LEFT JOIN users on posts.user_id = users.id LEFT JOIN likes on likes.post_id = posts.id GROUP BY posts.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        posts= []
        if results:
            for row in results:
                posts.append(row)
            return posts
        return posts
        
    @classmethod
    def create_post(cls,data):
        query = 'INSERT INTO posts (content, user_id, image) VALUES ( %(content)s, %(user_id)s, %(image)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_post_by_id(cls, data):
        query= 'SELECT * FROM posts WHERE posts.id = %(post_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]


    @classmethod
    def get_user_posts(cls, data):
        query= 'SELECT * FROM users LEFT JOIN posts on posts.user_id = users.id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        if results:
            for row in results:
                posts.append(row)
            return posts
        return posts

    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (post_id, user_id) VALUES ( %(post_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE post_id = %(post_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroyPost(cls, data):
        query= 'DELETE FROM posts WHERE posts.id = %(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def deleteAllLikes(cls, data):
        query= 'DELETE FROM likes WHERE likes.post_id = %(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 2:
            flash("Post content must be at least 2 characters.", 'content')
            is_valid = False
        return is_valid