import logging
from datetime import datetime

def setup_logger():
    log_filename=f"../data/logs/etl_{datetime.now().strftime('%Y%m%d')}.log" #Format de nom du fichier log
    log_format="%(asctime)s | %(levelname)s | %(filename)s| %(message)s" #Format d’affichage des messages

    logging.basicConfig(
        filename=log_filename, #Où ecrire la mpg
        level=logging.INFO, #Niveau de criticité: INFO, WARNING, ERROR, CRITICAL
        format=log_format,  # Format du message
    )

    # 4Ajout d’un “handler” pour aussi afficher dans la console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(console)
   # logging.info("✅ Logger initialisé avec succès")
    return logging

logging=setup_logger()