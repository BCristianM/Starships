import requests
import pymongo
client = pymongo.MongoClient()
db = client["starwars"]
from pprint import pprint
#mongosh
#db.collection.insertOne()

pilot_info_page = []
page_number = 1
still_got_pages = True
list_of_ships = []
while still_got_pages:
    json_return = requests.get("https://swapi.dev/api/starships/?page={}".format(page_number)).json()
    for starships in json_return["results"]:
        list_of_ships.append(starships)
    page_number += 1

    if json_return["next"] is None:
        still_got_pages = False


def change_names():
    for stuff in list_of_ships:
        if stuff["pilots"] is not []:
            for index in range(len(stuff["pilots"])):
                pilot_info = requests.get(stuff["pilots"][index]).json()
                pilot_id = db.characters.find_one({"name": pilot_info["name"]}, {"_id": 1})
                stuff["pilots"][index] = pilot_id
    pprint(list_of_ships)






'''
pilot_info = requests.get("https://swapi.dev/api/people/10/").json()
pilot_ID = db.characters.find_one({"name": pilot_info["name"]}, {"_id": 1})

'''






