-- Script de création du schéma du Data Warehouse (Star Schema)

-- Nettoyage préalable
DROP TABLE IF EXISTS fact_financement CASCADE;
DROP TABLE IF EXISTS dim_temps CASCADE;
DROP TABLE IF EXISTS dim_structure CASCADE;
DROP TABLE IF EXISTS dim_discipline CASCADE;
DROP TABLE IF EXISTS dim_financeur CASCADE;

-- 1. Dimension Temps
CREATE TABLE dim_temps (
    id_temps INT PRIMARY KEY, -- Smart Key: YYYYMMDD (ex: 20230115)
    date_jour DATE NOT NULL,
    annee INT NOT NULL,
    trimestre INT NOT NULL,
    mois INT NOT NULL,
    mois_nom VARCHAR(20),
    semaine INT
);

-- 2. Dimension Structure (Laboratoire et Institution)
CREATE TABLE dim_structure (
    id_structure SERIAL PRIMARY KEY,
    nom_laboratoire VARCHAR(255) NOT NULL,
    nom_institution VARCHAR(255) NOT NULL,
    type_institution VARCHAR(50)
);

-- 3. Dimension Discipline (Issue des Projets/Chercheurs)
CREATE TABLE dim_discipline (
    id_discipline SERIAL PRIMARY KEY,
    libelle_discipline VARCHAR(255) NOT NULL
);

-- 4. Dimension Financeur (Issue des Contrats)
CREATE TABLE dim_financeur (
    id_financeur SERIAL PRIMARY KEY,
    nom_financeur VARCHAR(255) NOT NULL,
    type_contrat VARCHAR(50) -- ex: ANR, Europe, etc.
);

-- 5. Table de Faits : Financement
CREATE TABLE fact_financement (
    id_financement SERIAL PRIMARY KEY,
    fk_temps INT NOT NULL REFERENCES dim_temps(id_temps),
    fk_structure INT NOT NULL REFERENCES dim_structure(id_structure),
    fk_discipline INT NOT NULL REFERENCES dim_discipline(id_discipline),
    fk_financeur INT NOT NULL REFERENCES dim_financeur(id_financeur),
    
    -- Mesures
    montant_contrat NUMERIC(15, 2),
    duree_mois INT,
    nombre_contrats INT DEFAULT 1,
    
    -- Métadonnées (optionnel pour traçabilité)
    source_contrat_id INT
);