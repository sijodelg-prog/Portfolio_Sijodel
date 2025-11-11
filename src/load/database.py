import requests
import pandas as pd
import time
from datetime import datetime as dt
import sqlite3 
import logging



def save_processed_data(df):
    filename = f"../data/processed/matches_{dt.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(filename, index=False)

#Connexion SQL
############################################################
def connexion():
    return sqlite3.connect("../data/Historique_match.db")
############################################################

#Export dans la table SQL
############################################################
def load_to_sqlite(df):
    try:
        with connexion() as conn:
            cursor=conn.cursor()
            existing_ids=pd.read_sql_query("SELECT DISTINCT id_match FROM matchs",conn) #On récupere tous les id de tous les matchs
            existing_ids=set(existing_ids["id_match"].tolist()) #On transforme la colonne "id_match" en liste pour lui appliquer la fonction "set" 
                                                                #qui est une fonction qui sert à detecter les doublons et les enlever automatiquement

            new_matches=df[~df["id_match"].isin(existing_ids)]  # la fonction "isin" retourne un booléen et permet de savoir si l'id du match existe déjà ou pas en base 
                                                                #~ est l'opératuer logique de la négation: en l'ajoutant on demande à savoir les matchs qui ne sont pas dans la base sql
                                                                #On stocke les matchs qui ne sont pas dans la base sql dans "new_matchs"
           
            updated_matches=df[df["id_match"].isin(existing_ids)] #Sans le ~ on veut retourner les matchs qui sont déjà dans la base de données.
            
            #Création de timestamp pour enregistré à quelle h ces matchs ont été intégrés
            now=dt.now().strftime("%Y-%m-%d %H:%M:%S")
            
            new_matches["loaded_at"] = now
            new_matches["updated_at"] = now
            updated_matches["loaded_at"] = now
            updated_matches["updated_at"] = now
            
            new_matches.to_sql(
                 name="matchs", #nom de la table
                 con=conn, #nom de la connexion
                 if_exists="append", #ajouter les données sans les supprimer
                 index=False #pas d'index 
            )
            rows_inserted=len(new_matches)
            logging.info(f"{len(new_matches)} nouveaux matches insérés")
            
            if not updated_matches.empty  : #Si la liste qui récupere les matchs déjà existants n'est pas vide
                updated_matches.to_sql(
                    name="matchs",
                    con=conn,
                    if_exists="replace",
                    index=False
                )
            rows_updated=len(updated_matches)
            logging.info(f"{len(updated_matches)} matches mis à jour")
            conn.commit()       
    except Exception as e:
        logging.error(f"Erreur dans l'insertion: {e}")
    return rows_inserted,rows_updated
############################################################







