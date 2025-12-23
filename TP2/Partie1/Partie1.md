# Partie 1 - Identification des données effectives

Cette section détaille les types de fichiers et les métadonnées techniques spécifiques qui seront stockés dans la base de données MongoDB. Ces informations sont associées à chaque fichier individuel au sein d'un jeu de données.

Chaque fichier sera représenté par un document contenant des informations communes et des métadonnées techniques spécifiques à son type.

### Structure commune à tous les fichiers

- **`nom_fichier`**: Nom du fichier (ex: `mesures_temp_2023-10-26.csv`).
- **`chemin_fichier`**: Chemin de stockage du fichier (ex: `/data/datasets/DS-2025-001/mesures.csv`).
- **`taille_fichier_octets`**: Taille du fichier en octets.
- **`type_mime`**: Type MIME du fichier (ex: `text/csv`).
- **`date_acquisition`**: Date et heure de création ou d'acquisition de la donnée.
- **`version`**: Version du fichier (ex: 1.0).
- **`annotations`**: Tableau d'objets pour les annotations ajoutées par les chercheurs (ex: `{ "auteur": "John Doe", "date": "2023-11-15", "commentaire": "Valeur aberrante à vérifier" }`).

---

### Métadonnées techniques par type de fichier

#### 1. Fichiers CSV (Chimie/Environnement)

- **`type_mime`**: `text/csv`
- **`metadonnees_techniques`**:
    - **`delimiteur`**: Caractère délimiteur (ex: `,`, `;`).
    - **`encodage`**: Encodage du fichier (ex: `UTF-8`).
    - **`colonnes`**: Tableau de chaînes de caractères listant les noms des colonnes.
    - **`unites`**: Objet associant une unité à chaque colonne de mesure (ex: `{ "temperature": "°C", "concentration_hcl": "mol/L" }`).
    - **`lieu_prelevement`**: Objet GeoJSON pour le lieu de prélèvement (ex: `{ "type": "Point", "coordonnees": [4.85, 45.75] }`).
    - **`methode_analyse`**: Description de la méthode d'analyse utilisée.

#### 2. Fichiers PNG (Sciences Médicales)

- **`type_mime`**: `image/png`
- **`metadonnees_techniques`**:
    - **`largeur`**: Largeur de l'image en pixels.
    - **`hauteur`**: Hauteur de l'image en pixels.
    - **`resolution`**: Résolution de l'image comme `300dpi`).
    - **`id_patient_pseudo`**: Identifiant pseudonymisé du patient.
    - **`type_examen`**: Type d'examen (ex: `Radiographie Thoracique`, `IRM Cérébrale`).

#### 3. Fichiers WAV (Sciences Humaines et Sociales)

- **`type_mime`**: `audio/wav`
- **`metadonnees_techniques`**:
    - **`duree_sec`**: Durée de l'enregistrement en secondes.
    - **`frequence_echantillonnage_hz`**: Fréquence d'échantillonnage en Hertz.
    - **`canaux`**: Nombre de canaux audio (ex: 1 pour mono, 2 pour stéréo).
    - **`langue`**: Langue parlée dans l'enregistrement (code ISO 639-1, ex: `fr`).
    - **`statut_anonymisation`**: Statut d'anonymisation (ex: `full`, `partial`, `none`).

#### 4. Fichiers GeoTIFF (Géosciences)

- **`type_mime`**: `image/tiff`
- **`metadonnees_techniques`**:
    - **`largeur`**: Largeur de l'image en pixels.
    - **`hauteur`**: Hauteur de l'image en pixels.
    - **`systeme_coordonnees`**: Système de coordonnées de référence (ex: `EPSG:4326 - WGS 84`).
    - **`boite_englobante`**: Emprise spatiale de l'image, sous forme d'un tableau de coordonnées `[min_lon, min_lat, max_lon, max_lat]`.
    - **`resolution`**: Résolution spatiale (ex: `10m/pixel`).
    - **`bandes`**: Nombre de bandes spectrales dans l'image.

#### 5. Fichiers PDF (Plan de Gestion de Données)

- **`type_mime`**: `application/pdf`
- **`metadonnees_techniques`**:
    - **`type_document`**: `Plan de Gestion de Données`.
    - **`version_pgd`**: Version du document (`1.0`, `2.1`..).
    - **`modele_utilise`**: Modèle utilisé pour créer le PGD comme `Science Europe` notamment utilisé par l'UMR CNRS 6240 LISA.