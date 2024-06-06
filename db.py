from dotenv import load_dotenv

import os
import psycopg2

load_dotenv();

dbURL = os.getenv("DATABASE")
connection = psycopg2.connect(dbURL);


def getAllData():
    with connection:
        with connection.cursor() as cursor:
            query = """SELECT users FROM collection"""
            cursor.execute(query)
            results = cursor.fetchall()
            if(results):
                return results
            else: 
                return "error"


def insertTV():
    return 0

def insertMovies():
    return 0

def deleteMovieFromCollection():
    return 0

def deleteTVFromCollection():
    return 0