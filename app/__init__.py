import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
              user=os.getenv("MYSQL_USER"),
              password=os.getenv("MYSQL_PASSWORD"),
              host=os.getenv("MYSQL_HOST"),
              port=3306)

print(mydb)



class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]
    timeline_post = TimelinePost.create(
        name=name,
        email=email,
        content=content)
    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_timeline_posts():
    return{
        'timeline_posts': [model_to_dict(post) for post in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    }

@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_timeline_post(post_id):
    try:
        timeline_post = TimelinePost.get_by_id(post_id)
        timeline_post.delete_instance()
        return {"message": f"Post with ID {post_id} deleted successfully."}, 200
    except TimelinePost.DoesNotExist:
        return {"error": "Post not found."}, 404




@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/about")
def about():
    return render_template(
        "about.html",
        title="About Me",
        work_experiences=[
            {
                "position": "Developer Intern",
                "company": "Direct Agents",
                "years": "February 2025-May 2025",
                "description": "Streamlined workflows",
            },
            {
                "position": "Data Analytics Intern",
                "company": "NYC Department of Investigation",
                "years": "February 2023-May 2023",
                "description": "Analyzed data",
            },
        ],
        education=[ {"school": "New York University", "degree": "MS in Computing", "years": "Expected Graduation December 2025"},{"school": "New York University", "degree": "BA in Computer Science", "years": "Graduated May 2024"}],
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title="Hobbies",
        hobbies=[
            {"name": "Video Games", "image": "videogame.jpg"},
            {"name": "Reading", "image": "reading.jpg"}
        ],
    )



@app.route("/map")
def map():
    places = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "date": "Present"},
        {"name": "Toronto", "lat": 43.651070, "lon": -79.347015, "date": "June 2025"},
        {"name": "Amsterdam", "lat": 52.3676, "lon": 4.9041, "date": "May 2025"},
        {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194, "date": "July 2024"},
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "date": "June 2024"},
        {"name": "Cancun", "lat": 21.1619, "lon": -86.8515, "date": "July 2015"},
        {"name": "Honolulu", "lat": 21.3069, "lon": -157.8583, "date": "June 2014"},
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "date": "2011"},
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "date": "2010"},
        {"name": "Beijing", "lat": 39.9042, "lon": 116.4074, "date": "2006"}

    ]
    return render_template("map.html", places=places)


@app.route("/timeline")
def timeline():
    return render_template('timeline.html', title="Timeline")