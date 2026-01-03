// Connexion à la base de données
db = connect("tp2_mongodb");
use("tp2_mongodb");

// Volume total de données (octets) par type de fichier
db.jeux_de_donnees.aggregate([
  { $unwind: "$fichiers" },
  {
    $group: {
      _id: "$fichiers.metadonnees_techniques.type",
      volume_total_octets: { $sum: "$fichiers.taille_fichier_octets" },
      nb_fichiers: { $sum: 1 }
    }
  }
]);

// Nombre moyen de fichiers par dataset
db.jeux_de_donnees.aggregate([
  {
    $project: {
      nb_fichiers: { $size: "$fichiers" }
    }
  },
  {
    $group: {
      _id: null,
      moyenne_fichiers_par_dataset: { $avg: "$nb_fichiers" },
      min_fichiers: { $min: "$nb_fichiers" },
      max_fichiers: { $max: "$nb_fichiers" }
    }
  }
]);

// Durée moyenne entre la première et la dernière acquisition de fichiers par dataset (en jours)
db.jeux_de_donnees.aggregate([
  { $unwind: "$fichiers" },
  {
    $group: {
      _id: "$id_jeu_de_donnees",
      premiere_acquisition: { $min: { $toDate: "$fichiers.date_acquisition" } },
      derniere_acquisition: { $max: { $toDate: "$fichiers.date_acquisition" } }
    }
  },
  {
    $project: {
      duree_ms: { $subtract: ["$derniere_acquisition", "$premiere_acquisition"] }
    }
  },
  {
    $group: {
      _id: null,
      duree_moyenne_jours: { $avg: { $divide: ["$duree_ms", 1000 * 60 * 60 * 24] } },
      duree_min_jours: { $min: { $divide: ["$duree_ms", 1000 * 60 * 60 * 24] } },
      duree_max_jours: { $max: { $divide: ["$duree_ms", 1000 * 60 * 60 * 24] } }
    }
  }
]);

// Taux de fichiers image avec dimensions manquantes
db.jeux_de_donnees.aggregate([
  { $unwind: "$fichiers" },
  { $match: { "fichiers.metadonnees_techniques.type": "image" } },
  {
    $project: {
      largeur: "$fichiers.metadonnees_techniques.largeur",
      hauteur: "$fichiers.metadonnees_techniques.hauteur"
    }
  },
  {
    $group: {
      _id: null,
      total_images: { $sum: 1 },
      images_dimensions_manquantes: {
        $sum: {
          $cond: [
            {
              $or: [
                { $eq: ["$largeur", null] },
                { $eq: ["$hauteur", null] }
              ]
            },
            1,
            0
          ]
        }
      }
    }
  },
  {
    $project: {
      total_images: 1,
      images_dimensions_manquantes: 1,
      taux_dimensions_manquantes: {
        $multiply: [
          { $divide: ["$images_dimensions_manquantes", "$total_images"] },
          100
        ]
      }
    }
  }
]);