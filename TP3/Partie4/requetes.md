### Requête 1 : Montant total par année

```mdx
SELECT
    { [Measures].[Montant Total] } ON COLUMNS,
    { [temps].[calendrier].[annee].MEMBERS } ON ROWS
FROM [cubeTP3]
```

### Requête 2 : Évolution des Financements par Laboratoire et par Année

```mdx
SELECT
    NON EMPTY { [temps].[calendrier].[annee].MEMBERS } ON COLUMNS,
    NON EMPTY { [structure].[organisation].[laboratoire].MEMBERS } ON ROWS
FROM [cubeTP3]
WHERE ( [Measures].[Montant Total] )
```

### Requête 3 : Top 3 des Disciplines les plus financées (Toute période)

```mdx
SELECT
    { [Measures].[Montant Total], [Measures].[Nombre Contrats] } ON COLUMNS,
    NON EMPTY TopCount(
        [discipline].[discipline].[discipline].MEMBERS,
        3,
        [Measures].[Montant Total]
    ) ON ROWS
FROM [cubeTP3]
```