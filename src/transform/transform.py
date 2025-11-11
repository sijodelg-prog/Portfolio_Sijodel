import requests
import pandas as pd
import time
from datetime import datetime as dt
import logging
import pytz


TIMEZONE = pytz.timezone("Europe/Paris")
def now_local():
    return dt.now(TIMEZONE)
#Récuperation des colonnes necessaires et changement de noms
############################################################
def Info_Match(Data,MatchList):
  matches=Data["matches"]#On récupere tous les matchs
  for match in matches:
      competition = match["competition"]["name"]
      if competition in ["Serie A","Bundesliga","Ligue 1","Premier League","Primera Division","Primeira Liga","UEFA Champions League"]:
          id= match["id"]
          homeTeam=match["homeTeam"]["name"]
          awayTeam=match["awayTeam"]["name"]
          score_home = match["score"]["fullTime"]["home"]
          score_away = match["score"]["fullTime"]["away"]
          status = match["status"]
          Heure_match=match["utcDate"],

          MatchList.append({
              "id_match": id,
              "competition": competition,
              "homeTeam": homeTeam,
              "awayTeam":awayTeam,
              "Buts_Domicile": score_home,
              "Buts_Visiteurs": score_away,
              "status": status,
              "Heure_match":Heure_match,


          })
  return MatchList
############################################################

#Transformation de données
############################################################

def Transformation_Data(DataJson): 
    try:
        MatchList = Info_Match(DataJson, [])
        DataMatch = pd.DataFrame(MatchList)

        DataMatch["Buts_Domicile"] = pd.to_numeric(DataMatch["Buts_Domicile"], errors='coerce').fillna(0).astype(int)
        DataMatch["Buts_Visiteurs"] = pd.to_numeric(DataMatch["Buts_Visiteurs"], errors='coerce').fillna(0).astype(int)

        DataMatch["Heure_match"] = DataMatch["Heure_match"].apply(lambda x: x[0] if isinstance(x, tuple) else x)
        DataMatch["Heure_match"] = pd.to_datetime(DataMatch["Heure_match"], utc=True)
        DataMatch["Heure"] = DataMatch["Heure_match"].dt.tz_convert("Europe/Paris").dt.tz_localize(None)

        DataMatch["Heure"] = DataMatch["Heure"].dt.strftime("%H:%M")

        DataMatch["score"] = (
            DataMatch['homeTeam'] + " " +
            DataMatch["Buts_Domicile"].astype(str) + "-" +
            DataMatch["Buts_Visiteurs"].astype(str) + " " +
            DataMatch['awayTeam']
        )

        DataMatch["competition"] = (
            DataMatch["competition"]
            .str.replace(" ", "_")
            .str.replace("Primera_Division", "Liga")
        )

        DataMatch = DataMatch.drop(columns=["Heure_match"])
        return DataMatch

    except Exception as e:
        logging.error(f"Erreur pendant la transformation : {e}")
        return pd.DataFrame()

############################################################