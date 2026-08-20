# Password Strength Checker

Outil en ligne de commande, 100% hors ligne, qui évalue la solidité d'un mot de passe : longueur, variété de caractères, présence dans une liste de mots de passe courants, séquences évidentes ("1234", "qwerty") et répétitions.

Aucune requête réseau n'est effectuée et le mot de passe n'est jamais écrit sur le disque.

## Utilisation (saisie masquée, recommandée)

```bash
python checker.py
```

## Utilisation avec argument

```bash
python checker.py --password "MonMotDePasse123!"
```

Attention : passé en argument, le mot de passe reste visible dans l'historique du terminal. Préférer la saisie masquée en usage réel.

## Lancer les tests

```bash
python -m unittest test_checker.py -v
```

## Ce que ça évalue

- Longueur (8, 12 et 16 caractères sont les paliers)
- Présence de minuscules, majuscules, chiffres et symboles
- Présence dans une liste de mots de passe très courants
- Séquences de clavier ou alphabétiques ("qwerty", "abcd")
- Répétitions du même caractère
