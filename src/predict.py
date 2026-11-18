from pathlib import Path

import joblib
import pandas as pd

CHEMIN_MODELE = Path(__file__).resolve().parents[1] / "models" / "modele_prix_m2.joblib"
_modele = None


def charger_modele():
    global _modele
    if _modele is None:
        _modele = joblib.load(CHEMIN_MODELE)
    return _modele


def predire(vente: dict) -> float:
    modele = charger_modele()
    return float(modele.predict(pd.DataFrame([vente]))[0])


if __name__ == "__main__":
    exemple = {
        "type_local": "Appartement",
        "surface_reelle_bati": 65,
        "nombre_pieces_principales": 3,
        "nb_dependances": 0,
        "surface_terrain_total": 0,
        "latitude": 48.5405,
        "longitude": 2.6554,
    }
    print(f"Prix estimé : {predire(exemple):.0f} €/m²")