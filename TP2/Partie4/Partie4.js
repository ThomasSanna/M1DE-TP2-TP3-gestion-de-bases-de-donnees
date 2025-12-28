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