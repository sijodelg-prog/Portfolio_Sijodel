-- matchs definition

CREATE TABLE "matchs" (
"id_match" INTEGER,
  "competition" TEXT,
  "homeTeam" TEXT,
  "awayTeam" TEXT,
  "Buts_Domicile" INTEGER,
  "Buts_Visiteurs" INTEGER,
  "status" TEXT,
  "Heure" TEXT,
  "score" TEXT,
  "loaded_at" TEXT,
  "updated_at" TEXT
);
-- etl_logs definition

CREATE TABLE etl_logs (
 			id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            run_start VARCHAR,
            run_end VARCHAR,
            rows_inserted INTEGER,
            rows_updated INTEGER,
            status VARCHAR,
            error VARCHAR
           
        );
