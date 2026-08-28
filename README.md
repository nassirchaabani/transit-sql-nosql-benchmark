# Data SQL / NoSQL Benchmark

[![Tests](https://github.com/nassirchaabani/transit-sql-nosql-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/nassirchaabani/transit-sql-nosql-benchmark/actions/workflows/ci.yml)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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

Les chiffres ne sont pas préremplis : ils dépendent du matériel, des caches et des versions des bases. Une comparaison sérieuse doit conserver les versions, le volume et le nombre de répétitions avec les résultats.

Le script affiche désormais automatiquement la version de Python, les versions de PostgreSQL et MongoDB, le nombre de processeurs logiques, le volume de données et le nombre de répétitions avant les résultats. Pour une publication, compléter avec le modèle exact du processeur et la mémoire vive de la machine.

## Résultats mesurés le 25 août 2026

Configuration : Lenovo 81Y4, Intel Core i5-10300H (4 cœurs / 8 threads, 2,50 GHz), 8 Go de RAM, Windows 10 Professionnel, Python 3.10.11, PostgreSQL 17.11 et MongoDB 8.2.12. Jeu de données : 50 000 événements. Chaque requête comprend un échauffement puis 7 mesures ; la médiane est retenue.

| Scénario | PostgreSQL | MongoDB | Rapport MongoDB / PostgreSQL |
| --- | ---: | ---: | ---: |
| Agrégation par ligne | 18,764 ms | 31,562 ms | 1,68x |
| Fenêtre station/date | 1,181 ms | 2,959 ms | 2,51x |

Sur cette machine et ces deux requêtes, PostgreSQL est donc **1,68 à 2,51 fois plus rapide**. Ces résultats décrivent ce protocole précis et ne constituent pas une conclusion générale sur les deux bases.