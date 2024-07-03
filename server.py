from flask import Flask, jsonify, render_template, request
from db import *
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
read_access_key = os.getenv('READ_ACCESS_KEY')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies")
def movies():
    
    playingNow = "https://api.themoviedb.org/3/movie/now_playing"
    popular = "https://api.themoviedb.org/3/movie/popular"
    topRated = "https://api.themoviedb.org/3/movie/top_rated"
    upcoming = "https://api.themoviedb.org/3/movie/upcoming"
    
    header = {
        'Authorization': f'Bearer {read_access_key}'
    }

    response1 = requests.get(playingNow, headers=header).json()
    response2 = requests.get(popular, headers=header).json()
    response3 = requests.get(upcoming, headers=header).json()
    response4 = requests.get(topRated, headers=header).json()
    
    return render_template(
        "./components/movie.html",
        playingNow=(response1),
        popular=(response2),
        topRated=(response3),
        upcoming=(response4)
    )

@app.route('/movies/<id>')
def movieInfo(id):
    print(id)
    
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    header = {
        'Authorization': f'Bearer {read_access_key}'
    }

    response = requests.get(url, headers=header)
    
    # print(response.json())
    
    return render_template('./components/information.html', information=response.json(), type="movie", movieId=id)
    

@app.route('/shows/<id>')
def showInfo(id):
    print(id)
    
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"
    
    header = {
        'Authorization': f'Bearer {read_access_key}'
    }

    response = requests.get(url, headers=header)
    
    # print(response.json())
    
    return render_template('./components/information.html', information=response.json(), type="show", showId=id)

@app.route("/shows")
def shows():
    
    header = {
        'Authorization': f'Bearer {read_access_key}'
    }
    
    airToday = "https://api.themoviedb.org/3/tv/airing_today"
    onAir = "https://api.themoviedb.org/3/tv/on_the_air"
    popular = "https://api.themoviedb.org/3/tv/popular"
    topRated = "https://api.themoviedb.org/3/tv/top_rated"
    
    response1 = requests.get(airToday, headers=header).json()
    response2 = requests.get(onAir, headers=header).json()
    response3 = requests.get(popular, headers=header).json()
    response4 = requests.get(topRated, headers=header).json()
    # print(response1)
    
    return render_template(
        "./components/shows.html", 
        airToday=(response1),
        onAir=(response2),
        popular=(response3),
        topRated=(response4)
    )

@app.route("/collection")
def collection():
    # print(getAllData())
    # print(mockDatabase)
    movies = getAllData()['movies']
    shows = getAllData()['shows']
    
    return render_template("./components/collection.html", moviesCollection=movies, showsCollection=shows)

@app.route('/search', methods=['POST'])
def redirectSearch():
    if request.method == 'POST':
        if(request.content_type == 'application/json'):
            # print(request.get_json()['option'])
            searchURL = ""
            header = {
                'Authorization': f'Bearer {read_access_key}'
            }
            
            if(request.get_json()['option'] == 'movie'):
                searchURL = f'https://api.themoviedb.org/3/search/movie?query={request.get_json()['search']}&include_adult=false&language=en-US&page=1'
            else:
                searchURL = f'https://api.themoviedb.org/3/search/tv?query={request.get_json()['search']}&include_adult=false&language=en-US&page=1'
            
            response = requests.get(searchURL, headers=header)
            url = f'/search/{request.get_json()['option']}={request.get_json()['search']}'
            
            if response.json() != None:
                return jsonify({'url' : url}) , 200
            else: 
                return 400

@app.route("/search/<type>=<searchWord>")
def search(searchWord, type):
    print(type)
    searchURL = ""
    header = {
        'Authorization': f'Bearer {read_access_key}'
    }
    
    if(type == 'movie'):
        searchURL = f'https://api.themoviedb.org/3/search/movie?query={searchWord}&include_adult=false&language=en-US&page=1'
    else:
        searchURL = f'https://api.themoviedb.org/3/search/tv?query={searchWord}&include_adult=false&language=en-US&page=1'

    response = requests.get(searchURL, headers=header)
    
    print(response.json())
    
    return render_template('./components/search.html', data=(response.json()))

mockDatabase = []
@app.route('/api/saveCinema', methods=['POST'])
def saveCinema():
    
    if(request.method == 'POST'):
        if(request.content_type == 'application/json'):
            # print(request.get_json())
            existed = any(request.get_json()['title'] in item.values() for item in mockDatabase)
            # print(existed)
            if existed:
                # print(mockDatabase)
                print('already existed - not adding to collection')
            else:
                #sending to the backend
                if request.get_json()['type'] == 'movie':
                    sending = {
                        'title' : request.get_json()['title'],
                        'movieId' : request.get_json()['id'],
                        'poster' : request.get_json()['imageURL'],
                        'releaseDate' : request.get_json()['release'],
                    }
                    insertMovies(sending)
                else:
                    sending = {
                        'title' : request.get_json()['title'],
                        'tvId' : request.get_json()['id'],
                        'poster' : request.get_json()['imageURL'],
                        'airDate' : request.get_json()['release'],
                    }
                    insertTV(sending)
                
    return jsonify({'results' : 'success'}), 200

@app.route('/api/deleteCinema', methods=['UPDATE'])
def removeMovieFromColl():
    
    if request.method == 'UPDATE':
        if request.content_type == 'application/json':
            # print(request.get_json())
            cinemaID = request.get_json()['cinemaID']
            # print(cinemaID)
            movies = getAllData()['movies']
            shows = getAllData()['shows']
            for items in movies:
                if items['movieId'] == str(cinemaID):
                    print('success in movie list')
                    deleteMovieFromCollection(cinemaID)
                else:
                    print('not in movies list')
                    
            for items in shows:
                if items['tvId'] == str(cinemaID):
                    print('success in show list')
                    deleteTVFromCollection(cinemaID)
                else:
                    print('not in shows list')
                    
            
            
    return jsonify({'results' : 'success'}), 200

if __name__ == "__main__":
    app.run()
