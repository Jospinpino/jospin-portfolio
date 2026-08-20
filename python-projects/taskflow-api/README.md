# TaskFlow API

API REST en Flask pour la gestion de tâches, pensée comme le pendant backend de l'application web TaskFlow. Stocke les tâches dans une base SQLite locale et expose des routes CRUD en JSON.

## Installation

```bash
pip install -r requirements.txt
```

## Lancer le serveur

```bash
python app.py
```

Le serveur démarre sur `http://localhost:5000`.

## Lancer les tests

```bash
python -m unittest test_app.py -v
```

## Routes disponibles

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/health` | Vérifie que l'API répond |
| GET | `/api/tasks` | Liste les tâches (filtre optionnel `?status=todo\|doing\|done`) |
| GET | `/api/tasks/<id>` | Récupère une tâche |
| GET | `/api/tasks/stats` | Compte les tâches par statut |
| POST | `/api/tasks` | Crée une tâche (`title` requis, `priority` et `status` optionnels) |
| PATCH | `/api/tasks/<id>` | Met à jour une tâche |
| DELETE | `/api/tasks/<id>` | Supprime une tâche |

## Exemple

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Préparer la démo", "priority": "high"}'
```
