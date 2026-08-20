# File Organizer CLI

Outil en ligne de commande qui range automatiquement les fichiers d'un dossier dans des sous-dossiers par catégorie (Images, Documents, Videos, Audio, Archives, Code, Others).

## Utilisation

```bash
python organize.py /chemin/vers/le/dossier
```

## Aperçu sans rien déplacer (dry run)

```bash
python organize.py /chemin/vers/le/dossier --dry-run
```

## Laisser de côté les types de fichiers inconnus

```bash
python organize.py /chemin/vers/le/dossier --skip-others
```

## Lancer les tests

```bash
python -m unittest test_organize.py -v
```

## Sécurité

L'outil ne remplace jamais un fichier existant : en cas de doublon de nom, il ajoute un compteur `(1)`, `(2)`, etc. Le mode `--dry-run` permet de vérifier le résultat avant tout déplacement réel.
