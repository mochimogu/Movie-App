from dotenv import load_dotenv

import os
import psycopg2
import json

load_dotenv();

dbURL = os.getenv("DATABASE")
connection = psycopg2.connect(dbURL);

def deleteTable():
    with connection:
        with connection.cursor() as cursor:
            deleteQuery = """DROP TABLE collection"""
            cursor.execute(deleteQuery)
    return 0


def createTable():
    with connection:
        with connection.cursor() as cursor:
            createQuery = """CREATE TABLE collection (
                id SERIAL PRIMARY KEY,
                users jsonb
            );"""
            
            cursor.execute(createQuery)
            return 0

def insertForTable():
    with connection:
        with connection.cursor() as cursor:
            insertQuery = """INSERT INTO collection (users) VALUES (
                '[
                    {
                        "username": "bob",
                        "movies": [
                            {
                                "title": "Kingdom of the Planet of the Apes",
                                "movieId": 653346,
                                "poster": "/gKkl37BQuKTanygYQG1pyYgLVgf.jpg",
                                "releaseDate": "2024-05-08"
                            }
                        ],
                        "shows": [
                            {
                                "title": "Top Chef VIP",
                                "tvId": 209374,
                                "poster": "/cw6M4c2MpLSzqzmrrqpSJlEbwCF.jpg",
                                "airDate": "2022-08-09"
                            }
                        ]
                    }
                ]'::jsonb
            );"""
            
            cursor.execute(insertQuery)
    return 0

# deleteTable()
# createTable()
# insertForTable()

def getAllData():
    with connection:
        with connection.cursor() as cursor:
            query = """SELECT users FROM collection"""
            cursor.execute(query)
            results = cursor.fetchall()
            # print(results[0][0][0])
            sendingBack = results[0][0][0]
            if(results):
                return sendingBack
            else: 
                return "error"


def insertTV(data):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT users FROM collection')
            results = cursor.fetchall()
            if results is not None:
                results[0][0][0]['shows'].append(data)
                # print(results[0][0][0]['shows'])
                updatedResults = json.dumps(results[0][0]);
                cursor.execute('UPDATE collection SET users = %s', [updatedResults])
                return 0
            else: 
                return 1

def insertMovies(data):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT users FROM collection')
            results = cursor.fetchall()
            if results is not None:
                results[0][0][0]['movies'].append(data)
                # print(results[0][0][0]['shows'])
                updatedResults = json.dumps(results[0][0]);
                cursor.execute('UPDATE collection SET users = %s', [updatedResults])
                return 0
            else: 
                return 1

def deleteMovieFromCollection(cinemaID):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT users FROM collection')
            results = cursor.fetchall()    
            # print(results[0][0][0]['movies'])
            count = 0
            for items in results[0][0][0]['movies']:
                # print(items['movieId'])
                if items['movieId'] == cinemaID:
                    # print('found', count)
                    results[0][0][0]['movies'].pop(count)
                    updatedResults = json.dumps(results[0][0]);
                    cursor.execute('UPDATE collection SET users = %s', [updatedResults])
                
                count+=1
    
    return 0

def deleteTVFromCollection(cinemaID):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT users FROM collection')
            results = cursor.fetchall()    
            # print(results[0][0][0]['shows'])
            count = 0
            for items in results[0][0][0]['shows']:
                # print(items['movieId'])
                if items['tvId'] == cinemaID:
                    # print('found', count)
                    results[0][0][0]['shows'].pop(count)
                    updatedResults = json.dumps(results[0][0]);
                    cursor.execute('UPDATE collection SET users = %s', [updatedResults])
                
                count+=1
    
    return 0