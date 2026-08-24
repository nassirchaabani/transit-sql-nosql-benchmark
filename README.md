# Transit SQL / NoSQL Benchmark

Ce projet compare PostgreSQL et MongoDB sur un même jeu de données synthétique de transport. Il couvre la génération, le chargement, l'indexation et des requêtes analytiques équivalentes. Chaque mesure est répétée et la médiane est affichée pour limiter l'effet du bruit.

## Prérequis

- Python 3.10
- Docker Desktop pour PostgreSQL et MongoDB

## Installation sous Windows

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Exécution

```powershell
docker compose up -d
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m src.generate_data --rows 50000
.\.venv\Scripts\python.exe -m src.load_postgres
.\.venv\Scripts\python.exe -m src.load_mongo
.\.venv\Scripts\python.exe -m src.benchmark --repetitions 7
```

## Résultats

Mesures obtenues localement sur 50 000 événements. Chaque requête a été exécutée une fois pour réchauffer les caches, puis sept fois ; le tableau présente la médiane.

| Requête | PostgreSQL | MongoDB | Rapport MongoDB/PostgreSQL |
|---|---:|---:|---:|
| Agrégation des retards par ligne | 16,718 ms | 40,631 ms | 2,43× |
| Moyenne des passagers par station et fenêtre temporelle | 1,514 ms | 3,900 ms | 2,58× |

PostgreSQL est donc environ 2,4 à 2,6 fois plus rapide sur ces deux scénarios. Le second cas bénéficie directement de l'index composé `(station_id, recorded_at)`. Ces résultats ne signifient pas que PostgreSQL est toujours plus rapide : ils décrivent seulement ce volume, ces modèles de données, ces index et cette machine.

## Reproduire les mesures

Pour comparer correctement une autre configuration, il faut conserver le volume de données et le nombre de répétitions, puis noter le matériel ainsi que les versions de PostgreSQL et MongoDB. Les caches, les processus actifs et le stockage peuvent modifier les temps obtenus.

Pour arrêter les bases après le benchmark :

```powershell
docker compose down
```

