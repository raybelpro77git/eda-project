import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

LAT_PARIS, LON_PARIS = 48.8534, 2.3488

# Colonnes attendues en entrée (ce que fournit l'utilisateur)
COLONNES_ENTREE = ["type_local", "surface_reelle_bati", "nombre_pieces_principales",
                   "nb_dependances", "surface_terrain_total", "latitude", "longitude"]

# Colonnes envoyées au modèle, dans cet ordre exact
VARIABLES_MODELE = ["type_local", "surface_reelle_bati", "nombre_pieces_principales",
                    "nb_dependances", "surface_terrain_total", "distance_paris_km",
                    "latitude", "longitude"]


def distance_km(lat1, lon1, lat2, lon2):
    rayon_terre = 6371
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = phi2 - phi1
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    return 2 * rayon_terre * np.arcsin(np.sqrt(a))


class PreparationVente(BaseEstimator, TransformerMixin):
    """Transforme les données brutes d'une vente en variables pour le modèle."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = pd.DataFrame(X)[COLONNES_ENTREE].copy()
        X["type_local"] = (X["type_local"] == "Maison").astype(int)
        X["distance_paris_km"] = distance_km(X["latitude"], X["longitude"], LAT_PARIS, LON_PARIS)
        return X[VARIABLES_MODELE]