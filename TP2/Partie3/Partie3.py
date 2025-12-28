from faker import Faker
import random
import json

fake = Faker("fr_FR")

# Paramètres de génération
# On génère 1000 jeux de données, chacun avec entre 5 et 10 fichiers
NB_DATASETS = 1000
MIN_FILES = 5
MAX_FILES = 10

# Types de fichiers possibles
FILE_TYPES = ["csv", "png", "wav", "geotiff", "pdf"]

# Génération d'un plan de gestion de données
def gen_plan_de_gestion(id_jeu_de_donnees):
    v = fake.random_element(elements=["1.0", "2.0", "2.1"])
    
    doc = {
        "nom_fichier": f"PGD_{id_jeu_de_donnees}_v{v}.pdf",
        "chemin_fichier": f"/data/{id_jeu_de_donnees}/PGD_{id_jeu_de_donnees}_v{v}.pdf",
        "taille_fichier_octets": fake.random_int(min=100_000, max=2_000_000),
        "type_mime": "application/pdf",
        "version_pgd": v,
        "modele_utilise": fake.random_element(elements=["DMP OPIDoR v3", "Science Europe"])
    }
    return doc

# Génération des métadonnées communes à tous les fichiers
def gen_common_file(id_jeu_de_donnees, fname, mime, date_debut, date_fin):
    date_acq = fake.date_between(start_date=date_debut, end_date=date_fin)

    doc = {
        "nom_fichier": fname,
        "chemin_fichier": f"/data/{id_jeu_de_donnees}/{fname}",
        "taille_fichier_octets": fake.random_int(min=2_000, max=150_000_000),
        "type_mime": mime,
        "date_acquisition": str(date_acq),
        "version": fake.random_element(elements=["1.0", "1.1", "2.0"]),
        "annotations": [] if random.random() < 0.7 else [
            {
                "auteur": fake.name(),
                "date": str(fake.date_between(start_date=date_acq, end_date=date_fin)),
                "commentaire": fake.random_element(elements=["Valeur aberrante à vérifier", "Donnée validée", "Nécessite un traitement complémentaire", "Anomalie détectée lors de l'acquisition"])
            }
        ]
    }
    return doc


def gen_csv(id_jeu_de_donnees, date_debut, date_fin):
    fname = f"mesures_{fake.date_this_decade()}.csv".replace(" ", "_")
    doc = gen_common_file(id_jeu_de_donnees, fname, "text/csv", date_debut, date_fin)
    doc["taille_fichier_octets"] = fake.random_int(min=2_000, max=600_000)

    colonnes = fake.random_element(elements=[
    ["timestamp", "pH", "temperature"],
    ["date", "nitrates", "phosphates", "temperature"],
    ["timestamp", "concentration_hcl", "conductivite"]
    ])

    unites_possibles = {
        "temperature": "°C",
        "nitrates": "mg/L",
        "phosphates": "mg/L",
        "concentration_hcl": "mol/L",
        "conductivite": "µS/cm"
    }

    unites = {col: unites_possibles[col] for col in colonnes if col in unites_possibles}

    doc["metadonnees_techniques"] = {
        "type": "csv",
        "delimiteur": fake.random_element(elements=[",", ";", "\t"]),
        "encodage": "UTF-8",
        "colonnes": colonnes,
        "unites": unites,
        "lieu_prelevement": {
            "type": "Point",
            "coordinates": [round(float(fake.longitude()), 5), round(float(fake.latitude()), 5)]
        },
        "methode_analyse": fake.random_element(elements=["Chromatographie", "Spectrophotométrie", "ISO", "Mesure électrochimique"])
    }
    return doc


def gen_png(id_jeu_de_donnees, date_debut, date_fin):
    fname = f"radiographie_{fake.random_int(min=1, max=999):03d}.png"
    doc = gen_common_file(id_jeu_de_donnees, fname, "image/png", date_debut, date_fin)
    doc["taille_fichier_octets"] = fake.random_int(min=50_000, max=9_000_000)

    largeur = fake.random_element(elements=[512, 1024, 2048, 4096, None])
    hauteur = largeur if largeur else fake.random_element(elements=[512, 1024, 2048, 4096])

    doc["metadonnees_techniques"] = {
        "type": "image",
        "largeur": largeur,
        "hauteur": hauteur,
        "resolution": fake.random_element(elements=["72dpi", "150dpi", "300dpi"]),
        "id_patient_pseudo": f"P{fake.random_int(min=1, max=999):03d}-{fake.lexify('???').upper()}",
        "type_examen": fake.random_element(elements=["Radiographie Thoracique", "IRM Cérébrale", "Scanner Abdominal"])
    }
    return doc


def gen_wav(id_jeu_de_donnees, date_debut, date_fin):
    fname = f"entretien_{fake.random_int(min=1, max=300):03d}.wav"
    doc = gen_common_file(id_jeu_de_donnees, fname, "audio/wav", date_debut, date_fin)
    doc["taille_fichier_octets"] = fake.random_int(min=500_000, max=120_000_000)

    doc["metadonnees_techniques"] = {
        "type": "audio",
        "duree_sec": fake.random_element(elements=[None, fake.random_int(min=30, max=3600)]),
        "frequence_echantillonnage_hz": fake.random_element(elements=[16000, 22050, 44100, 48000]),
        "canaux": fake.random_element(elements=[1, 2]),
        "langue": fake.random_element(elements=["fr", "en", "it"]),
        "statut_anonymisation": fake.random_element(elements=["full", "partial", "none"])
    }
    return doc


def gen_geotiff(id_jeu_de_donnees, date_debut, date_fin):
    fname = f"carte_{fake.random_int(min=1, max=500):03d}.tiff"
    doc = gen_common_file(id_jeu_de_donnees, fname, "image/tiff", date_debut, date_fin)
    doc["taille_fichier_octets"] = fake.random_int(min=2_000_000, max=400_000_000)

    doc["metadonnees_techniques"] = {
        "type": "geotiff",
        "largeur": fake.random_element(elements=[1024, 2048, 4096, None]),
        "hauteur": fake.random_element(elements=[1024, 2048, 4096, None]),
        "systeme_coordonnees": fake.random_element(elements=["EPSG:4326 - WGS 84", "EPSG:3857"]),
        "boite_englobante": [round(float(fake.longitude()), 4), round(float(fake.latitude()), 4), round(float(fake.longitude()), 4), round(float(fake.latitude()), 4)],
        "resolution": fake.random_element(elements=["1m/pixel", "10m/pixel", "30m/pixel"]),
        "bandes": fake.random_element(elements=[1, 3, 4, 8])
    }
    return doc


def gen_pdf(id_jeu_de_donnees, date_debut, date_fin):
    fname = f"document_{fake.random_int(min=1, max=200):03d}.pdf"
    doc = gen_common_file(id_jeu_de_donnees, fname, "application/pdf", date_debut, date_fin)
    doc["taille_fichier_octets"] = fake.random_int(min=80_000, max=8_000_000)

    doc["metadonnees_techniques"] = {
        "type": "pdf",
        "type_document": "Plan de Gestion de Données",
        "version_pgd": fake.random_element(elements=["1.0", "2.1", "2.0"]),
        "modele_utilise": fake.random_element(elements=["Science Europe", "DMP OPIDoR v3"])
    }
    return doc

# Génération d'un fichier aléatoire parmi les types possibles
def gen_file(id_jeu_de_donnees, date_debut, date_fin):
    ftype = fake.random_element(elements=FILE_TYPES)  # proba équivalente
    if ftype == "csv":
        return gen_csv(id_jeu_de_donnees, date_debut, date_fin)
    if ftype == "png":
        return gen_png(id_jeu_de_donnees, date_debut, date_fin)
    if ftype == "wav":
        return gen_wav(id_jeu_de_donnees, date_debut, date_fin)
    if ftype == "geotiff":
        return gen_geotiff(id_jeu_de_donnees, date_debut, date_fin)
    return gen_pdf(id_jeu_de_donnees, date_debut, date_fin)

# Génération d'un document jeu de données complet
def gen_dataset_doc(i):
    # IDs TP1 : 1..1000
    id_jeu_de_donnees = i

    # Dates de début et fin d'acquisition des fichiers
    date_debut = fake.date_between(start_date="-3y", end_date="-1y")
    date_fin = fake.date_between(start_date=date_debut, end_date="+1y")

    nb_files = fake.random_int(min=MIN_FILES, max=MAX_FILES)

    doc = {
        "id_jeu_de_donnees": id_jeu_de_donnees,
        "plan_de_gestion": gen_plan_de_gestion(id_jeu_de_donnees),
        "fichiers": [
            gen_file(id_jeu_de_donnees, date_debut, date_fin) for i in range(nb_files)
        ]
    }

    return doc


def main():
    # Génération des documents
    docs = [gen_dataset_doc(i) for i in range(1, NB_DATASETS + 1)]
    
    # Écriture du script d'insertion MongoDB
    with open("mongo_insert.js", "w", encoding="utf-8") as f:
        f.write("db=connect(\"tp2_mongodb\");\n")
        f.write("use(\"tp2_mongodb\");\n")
        f.write("db.jeux_de_donnees.deleteMany({});\n")
        f.write("db.jeux_de_donnees.insertMany(\n")
        f.write(json.dumps(docs, ensure_ascii=False, indent=2))
        f.write("\n);\n")

    print("Données générées dans 'mongo_insert.js'")

if __name__ == "__main__":
    main()
