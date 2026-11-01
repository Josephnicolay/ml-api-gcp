import os

import pandas as pd
from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from joblib import load
import pandas_gbq 


PROJECT = os.getenv("PROJECT")
DATASET = os.getenv("DATASET")
SOURCE_TABLE = os.getenv("SOURCE_TABLE")
FEATURES_TABLE = os.getenv("FEATURES_TABLE")
PREDICTIONS_TABLE = os.getenv("PREDICTIONS_TABLE")
MODEL_PATH = os.getenv("MODEL_PATH")


source_table_id = "{}.{}.{}".format(PROJECT, DATASET, SOURCE_TABLE)
features_table_id = "{}.{}.{}".format(PROJECT, DATASET, FEATURES_TABLE)
predictions_table_id = "{}.{}.{}".format(PROJECT, DATASET, PREDICTIONS_TABLE)

app = FastAPI()

classifier = load(MODEL_PATH)


@app.get("/")
def index():
    return {"message": "Welcome!", "service": "house-price-predictor-batch"}


@app.post("/predict")
def predict():
    try:
        client = bigquery.Client(project=PROJECT)

        X_train = client.query(
            f"SELECT * FROM `{source_table_id}`"
        ).to_dataframe()

        features = client.query(
            f"SELECT * FROM `{features_table_id}`"
        ).to_dataframe()
        features = features["string_field_0"].tolist()

        X_train = X_train[features]

        predictions = classifier.predict(X_train)

        predictions = pd.DataFrame(predictions, columns=["prediction"])
        predictions["prediction"] = predictions["prediction"]

        pandas_gbq.to_gbq(
            predictions,
            predictions_table_id,
            if_exists="append",
            project_id=PROJECT,
        )

        return {
            "message": "Predicción generada y guardada en BigQuery.",
            "rows": int(len(predictions)),
            "table_id": predictions_table_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))