import requests
import pandas as pd
import time
from datetime import datetime as dt
import logging
import schedule
from outils.logger_config import setup_logger  
from extract.api_call import get_football_info,save_raw_data
from transform.transform import Transformation_Data
from load.database import save_processed_data,load_to_sqlite,connexion







def run_etl():
        
        Data = get_football_info()
        save_raw_data(Data)
        if Data:
             Data_Matchs=Transformation_Data(Data)
             #save_processed_data(Data_Matchs)
             rows_inserted,rows_updated =load_to_sqlite(Data_Matchs)
        return rows_inserted,rows_updated       

JOURS_DE_LA_SEMAINE=[1,2,3,4,5,6]
def scheduler():
     while True:
            now=dt.now()
            hour=now.hour
            weekday=now.weekday()
            if weekday in JOURS_DE_LA_SEMAINE and 13<=hour<=24:
                try:
                    logging.info("Demarrage du job ETL")
                    run_start=dt.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    
                    rows_inserted,rows_updated=run_etl()
                    logging.info("ETL exécuté avec succès")
                    status="SUCCESS"
                    error=None
                except Exception as e:
                    
                    logging.error(f"Erreur pendant l'exécution: {e}")
                    rows_inserted=0
                    rows_updated=0
                    status="FAILED"
                    error=logging.error(f"Erreur pendant l'exécution: {e}")
                finally:
                    run_end=dt.now().strftime("%Y-%m-%d %H:%M:%S")
                    with connexion() as conn:
                        cursor=conn.cursor()
                        run_end = dt.now()
                        cursor.execute("""
                        INSERT INTO etl_logs (run_start, run_end, rows_inserted, rows_updated, status, error)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """, (run_start, run_end, rows_inserted, rows_updated, status, error))
                        conn.commit()
            else:
               logging.info("En dehors des créneaux (pause)")
            time.sleep(180)

def main():
    logging = setup_logger() 
    schedule.every(1).minutes.do(run_etl)
    logging.info('Planification établie: exécution toutes les minutes')
    while True:
        schedule.run_pending()
        time.sleep(60)
   
if __name__ == "__main__":
    scheduler()


