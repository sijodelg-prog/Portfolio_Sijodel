# ⚽ FootballAnalytics_Python

> 🚀 **Projet Data Engineering complet** : pipeline **ETL en Python** pour extraire, transformer et charger les données de matchs de football depuis l’API _Football-Data.org_ vers une base **SQLite**, avec gestion des logs et traçabilité.

---

## 🏷️ Badges techniques

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-DataFrame-yellow?logo=pandas)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![ETL](https://img.shields.io/badge/Process-ETL-orange)
![ADF](https://img.shields.io/badge/Azure-Data%20Factory-blue?logo=microsoftazure)
![Snowflake](https://img.shields.io/badge/Warehouse-Snowflake-00BFFF?logo=snowflake)
![Power BI](https://img.shields.io/badge/Dashboard-Power%20BI-F2C811?logo=powerbi)

---

## 🧠 Objectif

Automatiser le suivi et la transformation des données de matchs :
1. **Extraction** depuis l’API `football-data.org`
2. **Transformation** des données brutes en DataFrames propres
3. **Chargement** dans une base **SQLite**
4. **Journalisation complète** via `logger_config.py`

Ce pipeline constitue la **brique Python locale** du projet global *Football Analytics Data Platform* (ADF → Snowflake → Streamlnt).

---

## 🧩 Stack technique

| Outil / Lib | Usage principal |
|--------------|----------------|
| 🐍 **Python** | Développement du pipeline ETL |
| 🌐 **Requests** | Appels API REST |
| 🧮 **Pandas** | Transformation de données |
| 🗄️ **SQLite3** | Stockage local |
| 🧾 **Logging / dotenv** | Logs & variables d’environnement |
| 📊 **OpenPyXL** | Export Excel |

---

## 🗂️ Structure du projet
## 🧠 Architecture du pipeline Python

```mermaid
flowchart LR
    A[⚽ API Football Data] -->|JSON| B[📥 EXTRACT<br>src/extract/extract_api.py]
    B --> C[🧮 TRANSFORM<br>src/transform/transform.py]
    C --> D[💾 LOAD<br>src/load/database.py]
    D --> E[(🗄️ SQLite<br>data/historique_match.db)]
    C --> F[📊 Processed Files<br>data/processed/]
    A --> G[📁 Raw JSON<br>data/raw/]
    B --> H[🧾 Logs<br>data/logs/etl_*.log]
    D --> H

