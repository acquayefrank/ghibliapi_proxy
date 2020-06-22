import json
import os

import requests
import pymongo
import simplejson as sjson
from pymongo import MongoClient
from klein import Klein

MONGODB_HOSTNAME = os.getenv('MONGODB_HOSTNAME')
MONGODB_PORT = int(os.getenv('MONGODB_PORT'))
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
client = MongoClient(host=MONGODB_HOSTNAME,
                     port=MONGODB_PORT, 
                     username=MONGODB_USERNAME, 
                     password=MONGODB_PASSWORD,
                    authSource="admin")
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
app = Klein()


def get_ghibli_films():
    r = requests.get('https://ghibliapi.herokuapp.com/films')
    if r.status_code == 200:
        return r.json()
    else:
        return {"messgae": "something went wrong"}  


def get_ghibli_film(film_id):
    r = requests.get(f'https://ghibliapi.herokuapp.com/films/{film_id}')
    if r.status_code == 200:
        return r.json()
    else:
        return {"messgae": "something went wrong"}     
    

@app.route('/')
def pg_root(request):
    return 'Welcome to Ghibli'


@app.route('/api/v1/films/')
def pg_films(request):
    content = get_ghibli_films()
    response = json.dumps(content)
    return response

@app.route('/api/v1/films/<film_id>/')
def pg_film(request, film_id):
    db = client[MONGODB_DATABASE]
    collection = db.films
    data = collection.find_one({'film_id': film_id})
    film = get_ghibli_film(film_id)
    film['r_name'] = data['r_name'] #.encode(encoding = 'UTF-8',errors = 'strict')
    response = sjson.dumps(film) #, ensure_ascii=False).encode('utf8')
    return response
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run("0.0.0.0", port)

