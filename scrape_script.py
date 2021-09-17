from pymongo import MongoClient
from bs4 import BeautifulSoup
from typing import List,NamedTuple
import requests
import json
import pandas as pd

scraped_count = 0
url = 'https://pokemondb.net/pokedex/all'

page_response = requests.get(url, timeout=5)

page_content = BeautifulSoup(page_response.content, "html.parser")


pokemonRows = page_content.find_all("tr")
pokemonDict = {}

class Pokemon(NamedTuple):
    id: int
    name: str
    Types: List[str] 
    Hp: int
    Attack: int
    Defence: int
    Spattack: int
    Spdefence: int
    Speed: int


# client = MongoClient("mongodb+srv://bdatadmin:bdatadmin@DataMining.axs52.mongodb.net/DataMining?retryWrites=true&w=majority")
client = MongoClient("mongodb://localhost/pokemon")
db = client.pokemon
pokemon_collection = db.pokemon_pokemon


for row in pokemonRows[1:]:
    # Name
    name = row.find("a", attrs={"class": "ent-name"}).text
    ifMegaEvo = row.find("small", attrs={"class": "text-muted"})
    if ifMegaEvo:
        name = ifMegaEvo.text

    # Types
    pokemontype = []
    for ptype in row.find_all("a", attrs={"class": "type-icon"}):
        pokemontype.append(ptype.getText())
    #typesArray = list(map(lambda data: TYPES.index(data.text.upper()), typesHtml))
    typesArray = pokemontype
    
    # Base Stats
    id = row.find_all("td")[0]['data-sort-value']
    statsHtml = row.find_all("td")[4:]
    statsArray = list(map(lambda data: int(data.text), statsHtml))
    typesList = []

    # Format
    if len(typesArray) > 1:
        typesList.append(typesArray[0])
        typesList.append(typesArray[1])        
        pokemonDict[name] = {
        "Type1": typesArray[0],
        "Type2": typesArray[1],
        "Hp": statsArray[0],
        "Attack": statsArray[1],
        "Defense": statsArray[2],
        "Spattack": statsArray[3],
        "Spdefense": statsArray[4],
        "Speed": statsArray[5]
    }
    else:
        typesList.append(typesArray[0])
        pokemonDict[name] = {
        "Type1": typesArray[0],
        "Hp": statsArray[0],
        "Attack": statsArray[1],
        "Defense": statsArray[2],
        "Spattack": statsArray[3],
        "Spdefense": statsArray[4],
        "Speed": statsArray[5]
    }
    
    typed_pokemon = Pokemon(
    id = int(id),
    name = name,
    Types =  typesList,
    Hp = int(statsArray[0]),
    Attack = int(statsArray[1]),
    Defence = int(statsArray[2]),
    Spattack =  int(statsArray[3]),
    Spdefence = int(statsArray[4]),
    Speed = int(statsArray[5])
    )
    #print(typed_pokemon)
    
    types_string = ", ".join(typed_pokemon.Types)
    
    pokemon_collection.insert_one(
    
    {
        "id": scraped_count,
        "name": typed_pokemon.name,
        "Types":  types_string,
        "Hp": typed_pokemon.Hp,
        "Attack": typed_pokemon.Attack,
        "Defence": typed_pokemon.Defence,
        "Spattack": typed_pokemon.Spattack,
        "Spdefence": typed_pokemon.Spdefence,
        "Speed": typed_pokemon.Speed
    })
    scraped_count += 1
    print(scraped_count)

print("----------------------------------------Done---------------------------------------------")

    

    


#df = pd.DataFrame(data=pokemonDict)
#df.to_csv("pokedex.csv", header=True, index=False)
# Saving
#with open('db/pokedex.json', 'w') as outfile:
 #   json.dump(pokemonDict, outfile)

# pokemonDict[name]["Type2"] = typesArray[1]
# print(pokemonDict)
# print(name, typesArray, statsArray)
