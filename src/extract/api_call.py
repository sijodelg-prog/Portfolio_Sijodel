import requests
import pandas as pd
import time
from datetime import datetime as dt
from dotenv import load_dotenv
import os
import logging
import json


load_dotenv()  # Charge les variables d’environnement



print(os.getenv("API_KEY"))
print(os.getenv("DB_NAME"))

# Appel d'API
##########################################################
url='https://api.football-data.org/v4/matches'

headers={
    'X-Auth-Token': 'ba2eb4cdd11f417abfb94168f1b95a05' #Clé d'authentification
}
############################################################
def save_raw_data(data):
    filename = f"../data/raw/matches_{dt.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#Fonction d'appel API
############################################################
def get_football_info(): #Fonction d'appel API
    try:
        response=requests.get(url,headers=headers) #On récupere URL+ clé authentification
        response.raise_for_status() #Si code <>200 erreur
        football_data=response.json() # On récupere les données brut
        #save_raw_data(football_data) #On enregistre dans un fichier
        if "matches" not in football_data:
            raise ValueError("Structure inattendue dans la réponse API") #Il n'y a pas le liste des matchs
        logging.info("API call reussi; données récupérées.")
        return football_data
    except requests.exceptions.Timeout:
        logging.error("Timeout: l'API n'a pas répondu à temps")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Erreur HTTP: {e}")#Mauvais site
    except Exception as e:
        logging.error(f"erreur inatendue: {e}")
    return None  # Toujours retourner quelque chose
    
############################################################