import json
import pickle
import requests

import pandas as pd

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#pkl file imports
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

#functions
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#     recommended = {}
#     index = 0
#     for i in movies_list:
#         recommended[str(index)] = movies.iloc[i[0]].title
#         index += 1
#     return recommended

def recommend2(movie_id):
    recommended = []
    try:
        movie_index = movies[movies['movie_id'] == movie_id].index[0]
    except:
        return None

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    index=0
    for i in movies_list:
        recommended_id = int(movies.iloc[i[0]].movie_id)
        recommended_title = movies.iloc[i[0]].title
        recommended.append( {
            "id": recommended_id,
            "title": recommended_title
        })
        index+=1
        # print(movies.iloc[i[0]].title)
        print(recommended)
    return recommended

def fetchRecommended(recommended_movie_array):
    rec = []

    for i in recommended_movie_array:
        print("i= ",i)
        id = i['id']
        url = "https://api.themoviedb.org/3/movie/"+str(id)+"?api_key=c468f1a4793dde84b380dc978e620225"

        response = requests.get(url)
        data = response.json()
        # print(data)
        rec.append(data)
    return {'results': rec}
#routes
@app.route("/hello")
def hello():
    return 'hello'

@app.route("/")
def hello_world():
    return movies

@app.route("/recommend/<movie>")
def recommend_movie(movie):
    print(movie)
    recommended = recommend2(int(movie))
    # print("rec",recommended)
    if(recommended == None):
        return {'results': []}
    return fetchRecommended(recommended)

# @app.route("/recommend")
# def recommend_movie():
#     return recommend('Avatar')