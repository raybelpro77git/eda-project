import json
from datetime import date
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import make_pipeline

from src.features import COLONNES_ENTREE, PreparationVente

RACINE = Path(__file__).resolve().parents[1]
CHEMIN_DONNEES = RACINE / "data" / "processed" / "dvf_77_2025_enrichi.parquet"
DOSSIER_MODELES = RACINE / "models"


def main():
    df = pd.read_parquet(CHEMIN_DONNEES)
    df = df.dropna(subset=["latitude", "longitude"])
    X = df[COLONNES_ENTREE]
    y = df["prix_m2"]

    modele = make_pipeline(
        PreparationVente(),
        HistGradientBoostingRegressor(
            loss="absolute_error", learning_rate=0.03, max_iter=600,
            max_leaf_nodes=31, early_stopping=False, random_state=42,
        ),
    )
    modele.fit(X, y)

    DOSSIER_MODELES.mkdir(exist_ok=True)
    joblib.dump(modele, DOSSIER_MODELES / "modele_prix_m2.joblib")

    infos = {
        "date_entrainement": date.today().isoformat(),
        "nb_ventes": len(df),
        "version_sklearn": sklearn.__version__,
        "colonnes_entree": COLONNES_ENTREE,
        "mae_attendue_eur_m2": "510 a 575 (validation croisee, notebook 09)",
    }
    with open(DOSSIER_MODELES / "infos_modele.json", "w", encoding="utf-8") as f:
        json.dump(infos, f, ensure_ascii=False, indent=2)

    print(f"Modèle entraîné sur {len(df)} ventes et sauvegardé dans {DOSSIER_MODELES}")


if __name__ == "__main__":
    main()