import json
import os
import db

from db import db
from flask import Flask, request
from db import User, Recipe, Comment

app = Flask(__name__)
db_filename = "test1.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code = 200):
    return json.dumps(data), code

def failure_response(message, code = 404):
    return json.dumps({"error": message}), code

@app.route("/")
def hello_world():
    """
    Hello world!
    """
    return "Hello world!"

# User Routes ----------------------------------------------------------
@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    return success_response({"users": [u.serialize() for u in User.query.all()]})

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)

    if not "username" in body:
        return json.dumps({"error": "Username not provided"}), 400
    
    new_user = User(
        username = body.get("username")
    )

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_specific_user(user_id):
    """
    Endpoint for getting a specified user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())


@app.route("/api/users/<int:user_id>/", methods = ["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a specified user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

# Recipe Routes --------------------------------------------------------
@app.route("/api/recipes/")
def get_recipes():
    """
    Endpoint for getting all recipes
    """
    return success_response({"recipes": [r.serialize() for r in Recipe.query.all()]})

@app.route("/api/users/<int:user_id>/recipes/", methods = ["POST"])
def create_recipe(user_id):
    """
    Endpoint for creating a recipe
    """
    # Need to check if the user_id exists

    body = json.loads(request.data)

    if not "title" in body:
        return json.dumps({"error": "Title not provided"}), 400
    
    if not "post_date" in body:
        return json.dumps({"error": "Post date not provided"}), 400

    new_recipe = Recipe(
        title = body.get("title"),
        post_date = body.get("post_date"),
        image_url= body.get("image_url", ""),
        user_id = user_id
    )

    db.session.add(new_recipe)
    db.session.commit()
    return success_response(new_recipe.serialize(), 201)

@app.route("/api/recipes/<int:recipe_id>/")
def get_specific_recipe(recipe_id):
    """
    Endpoint for getting a specified recipe
    """
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe is None:
        return failure_response("Recipe not found!")
    return success_response(recipe.serialize())

@app.route("/api/recipes/<int:recipe_id>/", methods = ["DELETE"])
def delete_recipe(recipe_id):
    """
    Endpoint for deleting a specified recipe
    """
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe is None:
        return failure_response("Recipe not found!")
    db.session.delete(recipe)
    db.session.commit()
    return success_response(recipe.serialize())

@app.route("/api/recipes/<int:recipe_id>/", methods = ["POST"])
def like_recipe(recipe_id):
    """
    Update number of likes for recipe given id
    """
    

# Comments Routes ------------------------------------------------------
@app.route("/api/comments/")
def get_comments():
    """
    Endpoint for getting all comments
    """
    return success_response({"comments": [c.serialize() for c in Comment.query.all()]})

@app.route("/api/users/<int:user_id>/recipes/<int:recipe_id>/comments/", methods = ["POST"])
def create_comment(user_id, recipe_id):
    """
    Endpoint for creating a comment
    """
    # Need to check if the given user_id and recipe_id exists
    
    body = json.loads(request.data)
    
    if not "text" in body:
        return json.dumps({"error": "Text not provided"}), 400

    if not "post_date" in body:
        return json.dumps({"error": "Post date not provided"}), 400

    new_comment = Comment(
        text = body.get("text"),
        post_date = body.get("post_date"),
        user_id = user_id,
        recipe_id = recipe_id
    )

    db.session.add(new_comment)
    db.session.commit()
    return success_response(new_comment.serialize(), 201)

@app.route("/api/comments/<int:comment_id>/")
def get_specific_comment(comment_id):
    """
    Endpoint for getting a specified comment
    """
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return failure_response("Comment not found!")
    return success_response(comment.serialize())

@app.route("/api/comments/<int:comment_id>/", methods = ["DELETE"])
def delete_comment(comment_id):
    """
    Endpoint for deleting a specified comment
    """
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return failure_response("Comment not found!")
    db.session.delete(comment)
    db.session.commit()
    return success_response(comment.serialize())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
