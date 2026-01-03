# Notice de rendu - TP2

## Objectif
Ce TP met en place une base MongoDB contenant des jeux de données hétérogènes (documents imbriqués), puis exécute des requêtes d’agrégation pour produire des indicateurs.

## Environnement utilisé
- **MongoDB** : exécuté dans un **conteneur Docker** (port exposé, ex. `27017:27017`).
- **Exécution des requêtes** : via **VS Code** avec l’extension **MongoDB for VS Code** et des **MongoDB Playgrounds**.
- **Génération des données** : via **Python**.

## Pré-requis
- Python 3
- Docker
- VS Code + extension **MongoDB for VS Code**
- Dépendance Python : `faker`

Installation de la dépendance (si nécessaire) :
```bash
pip install faker
```

## Étapes d’exécution

### 1) Démarrer MongoDB (Docker)
MongoDB doit être accessible depuis la machine (ou l’environnement) où tourne VS Code.

Exemples d’URI de connexion :
- Sans authentification : `mongodb://localhost:27017`
- Avec authentification : `mongodb://<user>:<password>@localhost:27017`

### 2) Se connecter à MongoDB dans VS Code
1. Ouvrir l’onglet **MongoDB** (barre latérale).
2. Cliquer **Add Connection**.
3. Coller l’URI de connexion.
4. Vérifier que la connexion apparaît et qu’elle est sélectionnée pour l’exécution.

### 3) Générer les données (Python)
Le script `TP2/Partie3/Partie3.py` génère le script d’insertion `TP2/Partie3/mongo_insert.js`.

Commande (à lancer depuis `TP2/Partie3`) :
```bash
python Partie3.py
```

### 4) Insérer les données via un MongoDB Playground
1. `Ctrl+Shift+P` → **MongoDB: Create Playground**.
2. Copier/coller le contenu de `TP2/Partie3/mongo_insert.js` dans le Playground.
3. Exécuter avec **Run** (bouton ▶).

### 5) Exécuter les agrégations via un MongoDB Playground
1. Créer un nouveau Playground (ou remplacer le contenu du précédent).
2. Copier/coller le contenu de `TP2/Partie4/Partie4.js`.
3. Exécuter avec **Run**.

## Résultat attendu
- Base : `tp2_mongodb`
- Collection : `jeux_de_donnees`
- Les résultats des agrégations s’affichent dans l’interface VS Code (sortie de l’extension).

## Fichiers concernés
- Génération : `TP2/Partie3/Partie3.py`
- Insertion : `TP2/Partie3/mongo_insert.js`
- Agrégations : `TP2/Partie4/Partie4.js`
