
import requests
import pymongo
client = pymongo.MongoClient()
db = client["starwars"]
sw = db["starships"]

list_of_ships = []


def create_list():
    page_number = 1 # Here I have created a while loop in order to check for pages in the API.
    still_got_pages = True
    while still_got_pages:
        json_return = requests.get("https://swapi.dev/api/starships/?page={}".format(page_number)).json()
        for starships in json_return["results"]:    # This formats the url so that it goes through the pages
            list_of_ships.append(starships)
        page_number += 1       # This increments the page every time it is used

        if json_return["next"] is None:  # This will break the loop on account of the API running out of pages.
            still_got_pages = False


def change_names():
    for stuff in list_of_ships:   # This creates a for loop for every key value inside the dictionary
        if stuff["pilots"] is not []:  # This looks at the client lists specifically which are embedded
            for index in range(len(stuff["pilots"])):  # This loops through the lists of the Url themselves, where the constraint is the amount of URL's.
                pilot_info = requests.get(stuff["pilots"][index]).json()  # Goes into the URL itself and gets the info from character
                pilot_id = db.characters.find_one({"name": pilot_info["name"]}, {"_id": 1})  # This line references the name from the url and /
                                                                    # looks the _id of the name from the characters list, bringing back the _ID /
                                                                    # of the character
                stuff["pilots"][index] = pilot_id["_id"]            # This line replaces the URl with the _id itself, referring to the index of the URL
    return list_of_ships  # This function returns the amended list of ships


create_list()      # This calls out the first function


sw.delete_many({})  # This refreshes the "starships" page everytime this program gets executed, so that there are no
                    # duplicates


sw.insert_many(change_names())  # This inserts all the amended key value pairs from the change_names() function







