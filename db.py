from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Classes below

class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    recipes = db.relationship("Recipe", cascade="delete")
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize User object
        """
        self.username = kwargs.get("username", "User" + str(self.id))

    def serialize(self):
        """
        Serialize a User object
        """
        return {
            "id": self.id,
            "username": self.username,
            "recipes": [r.simple_serialize() for r in self.recipes],
            "user_comments": [c.simple_serialize_for_user() for c in self.comments]
        }
    
    def simple_serialize(self):
        """
        Serialize a User object only with its id and username
        """
        return {
            "id": self.id,
            "username": self.username
        }
    
    def is_valid_user_id(self, user_id):
        """
        Returns True if there is a user corresponding to user_id in the
        users table, else False
        """
        pass


class Recipe(db.Model):
    """
    Recipe model
    """
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    post_date = db.Column(db.String, nullable=False)
    number_of_likes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_url = db.Column(db.String, nullable = False)
    
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize Recipe object/entry
        """
        self.title = kwargs.get("title", "Untitled")
        self.post_date = kwargs.get("post_date", "")
        self.number_of_likes = 0
        self.user_id = kwargs.get("user_id", None)
        self.image_url = kwargs.get("image_url", "")

    def serialize(self):
        """
        Serialize a Recipe object
        """
        return {
            "id": self.id,
            "title": self.title,
            "post_date": self.post_date,
            "number_of_likes": self.number_of_likes,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "recipe_comments": [c.simple_serialize_for_recipe() for c in self.comments]
        }

    def simple_serialize(self):
        """
        Serialize a Recipe object without its comments
        """
        return {
            "id": self.id,
            "title": self.title,
            "post_date": self.post_date,
            "number_of_likes": self.number_of_likes,
            "image_url" : self.image_url
        }
    
    def is_valid_recipe_id(self, recipe_id):
        """
        Returns True if there is a recipe corresponding to recipe_id in
        the recipe table, else False
        """
        pass

class Comment(db.Model):
    """
    Comment model
    """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    post_date = db.Column(db.String, nullable=False)
    number_of_likes = db.Column(db.Integer, nullable=False)
    number_of_dislikes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Comment object/entry
        """
        self.text = kwargs.get("text", "")
        self.post_date = kwargs.get("post_date", "")
        self.number_of_likes = 0
        self.number_of_dislikes = 0
        self.user_id = kwargs.get("user_id")
        self.recipe_id = kwargs.get("recipe_id")

    def serialize(self):
        """
        Serialize a Comment object
        """
        return {
            "id": self.id,
            "text": self.text,
            "post_date": self.post_date,
            "number_of_likes": self.number_of_likes,
            "number_of_dislikes": self.number_of_dislikes,
            "user_id": self.user_id,
            "recipe_id": self.recipe_id
        }

    def simple_serialize_for_user(self):
        """
        Serialize a Comment object without its user id, number of likes,
        and number of dislikes
        """
        return {
            "id": self.id,
            "text": self.text,
            "post_date": self.post_date,
            "recipe_id": self.recipe_id
        }
    
    def simple_serialize_for_recipe(self):
        """
        Serialize a Comment object without its recipe id, number of likes,
        and number of dislikes
        """
        return {
            "id": self.id,
            "text": self.text,
            "post_date": self.post_date,
            "user_id": self.user_id
        }
    
    def is_valid_comment(self, comment_id):
        """
        Returns True if there is a comment corresponding to comment_id in
        the comments table, else False
        """
        pass