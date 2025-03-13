# Projet de visualisation des données
Autheur : Baptiste Grignon & Thomas Fassin

Stockage public du code de traitement des données pour le cours de Visualisation Interactive des Données donnée par Dr. Romain Vuillemot à l'Ecole Centrale de Lyon. Le projet est disponible ici : https://observablehq.com/d/ccc1fb0bd9d2c6c3

Les données sont téléchargés depuis l'API de [Copernicus](https://data.marine.copernicus.eu/product/MULTIOBS_GLO_PHY_TSUV_3D_MYNRT_015_012/description) automatiquement dans les scripts python et stocké dans le dossier datasets (il faut vous inscrire sur la plateforme et remplacer le nom et le mot de passe par le votre).

graph_ex.py permet de réaliser des graphiques exploratoires dynamiques de la base de donnée utilisée [Copernicus](https://data.marine.copernicus.eu/product/MULTIOBS_GLO_PHY_TSUV_3D_MYNRT_015_012/description).

absolute_speed.py permet de calculer la valeur absolue des courants marins (vitesse de l'eau) à travers le monde (et en profondeur) au 1er janvier 2022 et de la stocker au format csv.

DL_datasets.py permet de télécharger les datasets nécessaires pour MOC_compute.py, c'est à dire les données de courants marins sur le monde et en profondeur de 1993 à 2022 (au 1er janvier), en aggrégant les points de données pour diminuer la taille des fichiers.

MOC_compute.py calcule la circulation méridienne de retournement (Meridionnal Overturning Circulation ou MOC) pour chaque point temporel, pour chaque latitude et pour chaque profondeur (l'intégration est réalisé sur toute les valeurs de longitude et sous la profondeur spécifiée).
