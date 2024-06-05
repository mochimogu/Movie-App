from flask import Flask, jsonify, render_template, request
from db import *
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
read_access_key = os.getenv('READ_ACCESS_KEY')

website = "https://api.themoviedb.org/3/discover/movie"
header = {
    'Authorization': f'Bearer {read_access_key}'
}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies")
def movies():
    
    response = requests.get(website, headers=header)
    print(response.status_code)
    print(response.json())
    
    return render_template("./components/movie.html")

@app.route("/shows")
def shows():
    return render_template("./components/shows.html")

@app.route("/collection")
def collection():
    # print(getAllData())
    return render_template("./components/collection.html")



if __name__ == "__main__":
    app.run()
