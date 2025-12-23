# Partie 2 - Conception des collections

Cette section présente deux schémas possibles pour organiser les données dans MongoDB, suivie d'une justification du choix retenu.

## Schéma 1 : Collection unique avec documents embarqués

Dans cette approche, une seule collection `jeux_de_donnees` est utilisée. Chaque document de cette collection représente un jeu de données complet (identifié par son `id_jeu_de_donnees` provenant de PostgreSQL) et contient un tableau `fichiers` qui embarque les informations sur tous les fichiers qui le composent.

```json
{
  "id_jeu_de_donnees": "DS-2025-001", // Clé de jointure avec PostgreSQL
  "plan_de_gestion": {
    "nom_fichier": "PGD_Projet_ChimieVerte_v2.pdf",
    "chemin_fichier": "/data/DS-2025-001/PGD_Projet_ChimieVerte_v2.pdf",
    "taille_fichier_octets": 345678,
    "type_mime": "application/pdf",
    "version_pgd": "2.0",
    "modele_utilise": "DMP OPIDoR v3"
  },
  "fichiers": [
    {
      "nom_fichier": "radiographie_thorax_patient01.png",
      "chemin_fichier": "/data/DS-2025-001/img_01.png",
      "taille_fichier_octets": 120450,
      "type_mime": "image/png",
      "date_acquisition": "2023-01-15T09:30:00Z",
      "metadonnees_techniques": {
        "type": "image",
        "largeur": 1024,
        "hauteur": 1024,
        "id_patient_pseudo": "P001-A7B"
      }
    },
    {
      "nom_fichier": "mesures_ph_riviere.csv",
      "chemin_fichier": "/data/DS-2025-001/mesures_01.csv",
      "taille_fichier_octets": 5120,
      "type_mime": "text/csv",
      "date_acquisition": "2023-02-20T14:00:00Z",
      "metadonnees_techniques": {
        "type": "csv",
        "delimiteur": ",",
        "colonnes": ["timestamp", "pH", "temperature"]
      }
    }
    // ... autres fichiers
  ]
}
```

## Schéma 2 : Plusieurs collections spécialisées

Cette approche utilise une collection principale `jeux_de_donnees` pour lier le `id_jeu_de_donnees` à une liste de références de fichiers, et des collections séparées pour chaque type de fichier (`fichiers_images`, `fichiers_audio`, etc.).

**Collection `jeux_de_donnees` :**
```json
{
  "id_jeu_de_donnees": "DS-2025-001",
  "fichiers": [
    { "id_fichier": ObjectId("6564d3..."), "collection": "fichiers_images" },
    { "id_fichier": ObjectId("6564d4..."), "collection": "fichiers_csv" }
  ]
}
```

**Collection `files_images` :**
```json
{
  "_id": ObjectId("6564d3..."),
  "file_name": "radiographie_thorax_patient01.png",
  // ... métadonnées communes et techniques pour les images
}
```

## Choix de la solution et justification

**La solution retenue est le Schéma 1 : Collection unique avec documents embarqués.**

### Justification :

1.  **Atomicité et cohérence des données** : Le principal avantage est que toutes les informations relatives à un jeu de données (tous ses fichiers et leurs métadonnées) sont stockées dans un seul document. Cela garantit que les opérations de lecture ou de mise à jour pour un jeu de données complet sont atomiques. Il n'y a pas de risque de désynchronisation entre plusieurs collections.

2.  **Performance des requêtes** : Les requêtes qui analysent les fichiers au sein d'un même jeu de données (par exemple, "calculer le volume total d'un dataset" ou "lister tous les fichiers d'un dataset") sont extrêmement performantes. Toutes les données nécessaires sont récupérées en une seule opération de lecture, évitant ainsi des jointures applicatives (`$lookup`) qui seraient nécessaires avec le Schéma 2 et qui peuvent être coûteuses.

3.  **Simplicité du modèle** : Le modèle est plus simple à comprendre et à gérer. Il y a moins de collections à maintenir, et la relation entre un jeu de données et ses fichiers est explicite et naturelle.

4.  **Flexibilité** : Le schemaless de MongoDB permet de stocker des `technical_metadata` de structures très différentes au sein du même tableau `files`, ce qui correspond parfaitement à la nature hétérogène des fichiers d'un jeu de données. Un champ `type` dans les métadonnées techniques permet de distinguer facilement les différents formats.

### Limites à considérer :

Le Schéma 1 est idéal tant que le nombre de fichiers par jeu de données n'est pas excessivement grand. La limite de taille d'un document MongoDB (16 Mo) pourrait être atteinte si un jeu de données contenait des centaines de milliers de fichiers avec des métadonnées volumineuses. Cependant, pour la plupart des cas d'usage de la recherche, où un jeu de données regroupe quelques dizaines à quelques milliers de fichiers, cette approche reste la plus pertinente et performante.