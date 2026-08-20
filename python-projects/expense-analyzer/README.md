# Expense Analyzer

Outil en ligne de commande qui lit un fichier CSV de dépenses et produit un résumé texte ainsi que deux graphiques : la répartition par catégorie et la tendance mensuelle.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python analyze.py sample_expenses.csv
```

Les graphiques sont enregistrés dans le dossier `charts/` (`by_category.png` et `by_month.png`).

## Utiliser ses propres données

Le fichier CSV doit avoir trois colonnes : `date` (AAAA-MM-JJ), `category`, `amount`.

```bash
python analyze.py mes_depenses.csv --output-dir mon_dossier
```

Pour n'afficher que le résumé texte, sans générer de graphiques :

```bash
python analyze.py mes_depenses.csv --no-charts
```

## Lancer les tests

```bash
python -m unittest test_analyze.py -v
```
