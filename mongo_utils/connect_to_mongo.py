import os
import json
from decouple import config
from pathlib import Path
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = config("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["La-Justa"]  
collection = db["news"]

project_root = Path(__file__).resolve().parent.parent  # Up 2 levels
results_folder = project_root / 'results'  # Acceder a 'results'

for filename in os.listdir(results_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(results_folder, filename)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            data = json.load(file)
            
            # Asegúrate de que `data` esté en el formato esperado (una lista o un diccionario)
            if isinstance(data, list):  # Si el archivo contiene una lista de noticias
                collection.insert_many(data)  # Inserta varias noticias a la vez
            elif isinstance(data, dict):  # Si el archivo contiene solo una noticia
                collection.insert_one(data)  # Inserta una noticia

print("Datos insertados correctamente en MongoDB")

