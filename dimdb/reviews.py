import pickle
import numpy as np
import pandas as pd
from flask import current_app, flash

from . import db

CLASSIFIER_FILENAME = "review_classifier.pkl"

def train_review_classifier():
    reviews = db.get_all_reviews()
    raise Exception("INSERIRE ISTRUZIONI MANCANTI QUI")
    with current_app.open_instance_resource(CLASSIFIER_FILENAME, "wb") as f:
        pickle.dump(model, f)
    flash("Trained review classification model")

def classify_review(review):
    with current_app.open_instance_resource(CLASSIFIER_FILENAME, "rb") as f:
        model = pickle.load(f)
    return pd.Series(model.predict_proba([review]).ravel(),
                     index=model.classes_)

def classify_reviews(reviews):
    with current_app.open_instance_resource(CLASSIFIER_FILENAME, "rb") as f:
        model = pickle.load(f)
    proba = model.predict_proba(reviews)
    return pd.DataFrame(proba, columns=model.classes_)
