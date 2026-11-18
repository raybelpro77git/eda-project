# Prix de l'immobilier en Seine-et-Marne (DVF 2025)

Analyse exploratoire des ventes de logements en Seine-et-Marne (77) en 2025, à partir des données publiques DVF. Le projet nettoie les données, étudie ce qui fait varier le prix au m² (type de bien, caractéristiques, commune, distance à Paris, mois) et prépare une phase de modélisation.

## Résultats clés

- **Données propres, sans retouche de la cible.** Sur 13 717 ventes de logements, seules 5 sont retirées (surface impossible ou prix au m² aberrant), au lieu de 241 avec une règle statistique appliquée à l'aveugle. Jeu final : 13 712 ventes.
- **Le prix baisse avec la distance à Paris.** Prix médian de 3 518 €/m² à moins de 20 km contre 1 963 €/m² au-delà de 60 km. Corrélation d'environ -0,63 entre distance et prix médian sur les 93 communes de 30 ventes ou plus.
- **La distance n'explique pas tout.** Fontainebleau et Bois-le-Roi (loin mais chères) et les communes de Marne-la-Vallée (Serris, Chessy, Montévrain...) s'écartent nettement du gradient. Les causes possibles (cadre résidentiel, constructions neuves, desserte) ne sont pas dans les données.
- **Effet de composition.** La part de maisons passe de 44 % près de Paris à 80 % au-delà de 60 km : une partie de l'écart de prix entre maisons et appartements vient de la localisation, pas du type de bien.
- **Un modèle bat nettement la baseline.** Un modèle de boosting (surface, terrain, type de bien, distance à Paris, latitude et longitude) atteint une erreur absolue moyenne de 516 €/m² sur le jeu de test, contre 887 €/m² en prédisant la médiane (environ -42 %). L'erreur attendue dans le 77 est d'environ 510 à 575 €/m², selon que la commune est bien connue du modèle ou non. La position géographique et la surface sont les variables les plus utiles ; le réglage des paramètres, une cible en logarithme et l'encodage de la commune n'apportent rien de plus.
- **Pas de saisonnalité des prix démontrée.** Le nombre de ventes varie presque du simple au double selon le mois (804 en avril, 1 587 en juillet), mais le prix médian reste stable (environ 3 000 à 3 160 €/m²), dans l'ordre de grandeur du bruit d'échantillonnage.

## Données

Source : [Demandes de valeurs foncières géolocalisées](https://www.data.gouv.fr/fr/datasets/5cc1b94a634f4165e96436c1/) (DGFiP, enrichies par Etalab, sur data.gouv.fr). Le fichier utilisé est le DVF 2025 France entière.

Les données ne sont pas versionnées dans Git (`data/raw/` et `data/processed/` sont ignorés). Pour reproduire l'analyse :

1. Télécharger le fichier DVF 2025 et le placer dans `data/raw/dvf-2025.csv.gz`.
2. Exécuter les notebooks dans l'ordre, en commençant par `02_extraction`, qui extrait la Seine-et-Marne et produit les fichiers de `data/processed/`.

Chaque notebook lit le fichier produit par le précédent et en écrit un nouveau, sans jamais écraser une étape :
`dvf_77_2025` -> `_propre` -> `_filtre` -> `_analyse` -> `_enrichi`.

## Structure du dépôt

| Notebook | Contenu |
| --- | --- |
| `01_exploration` | Premier contact avec un échantillon de 1 000 lignes |
| `02_extraction` | Extraction de la Seine-et-Marne depuis le fichier France entière (lecture par morceaux) |
| `03_nettoyage` | Ne garder que les ventes d'un seul logement, traiter les anomalies |
| `04_distribution_prix` | Distribution du prix au m², détection et inspection des valeurs aberrantes |
| `05_caracteristiques_bien` | Pièces, dépendances, terrain et prix au m² |
| `06_communes` | Prix par commune, distance à Paris, effet de composition |
| `07_evolution_mensuelle` | Évolution mensuelle des ventes et des prix en 2025 |
| `08_modele_reference` | Baseline, régression linéaire, forêt aléatoire, validation croisée et évaluation finale |
| `09_amelioration_modele` | Boosting, réglage, cible en log, encodage de la commune, évaluation finale |
| `10_feature_engineering` | Nouvelles variables (direction depuis Paris, rapports, prix des ventes voisines) |

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (Linux/Mac : source .venv/bin/activate)
pip install -r requirements.txt
jupyter lab
```

## Limites et suite

- Une seule année de données : impossible de distinguer saisonnalité et tendance.
- Les médianes de petites communes (moins de 30 ventes) sont peu fiables ; toutes les communes sont gardées dans le jeu de données et le seuil n'est appliqué qu'à l'affichage.
- La date de mutation est la date de signature de l'acte, pas celle de la décision d'achat.
- Pas d'information sur l'âge du bâtiment ni sur la desserte en transports.
- Modèle : l'erreur est plus forte pour les maisons et dans la zone de Fontainebleau (50-60 km de Paris) ; la validation par commune laisse les communes voisines dans l'entraînement.
- Le modèle a atteint un plateau : réglages, cible en logarithme, encodage de la commune et nouvelles variables construites (direction, rapports, prix des voisins) n'apportent rien. Pour aller plus loin, il faudrait des données nouvelles (âge et état du bien, transports, zones commerciales) ou plusieurs années. Aucune validation ne mesure le décalage dans le temps (modèle entraîné sur 2025).
