from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from datetime import datetime
import sqlite3


app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://yaznfhnrifizmu:99ccd882cae2922fdce4f9d8db9992f3179fb1c970a983e1527f9ef7f7f0c024@ec2-54-221-217-204.compute-1.amazonaws.com:5432/deij3tq74i7arp'


CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)





class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(140))
    post_type = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)
       
    def __init__(self, title, description, post_type):
        self.title = title
        self.description = description
        self.post_type = post_type


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "post_type")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)






@app.route("/posts", methods=["GET"])
def get_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)


@app.route("/post", methods=["POST"])
def add_post(): 
    title = request.json["title"]
    description = request.json["description"]
    post_type = request.json["post_type"]

    new_post = Post(title, description, post_type)
    db.session.add(new_post)
    db.session.commit()

    created_post = Post.query.get(new_post.id)
    return post_schema.jsonify(created_post)

@app.route("/post/<id>", methods=["PUT"])
def update_post(id):
    post = Post.query.get(id)

    post.title = request.json["title"]
    post.description = request.json["description"]
    post.post_type = request.post_type["description"]

    db.session.commit()
    return todo_schema.jsonify(post)

@app.route ("/post/<id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return "RECORD SUCCESSFULLY MERKED"

if __name__ == "__main__":
    app.debug = True
    app.run()