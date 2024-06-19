from dotenv import load_dotenv

import os
import psycopg2
import json

load_dotenv();

dbURL = os.getenv("DATABASE")
connection = psycopg2.connect(dbURL);


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

def deleteMovieFromCollection():
    return 0

def deleteTVFromCollection():
    return 0