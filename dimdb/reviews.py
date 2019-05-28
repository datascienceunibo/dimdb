import pickle
import numpy as np
import pandas as pd
from flask import current_app, flash
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from . import db

CLASSIFIER_FILENAME = "review_classifier.pkl"

def train_review_classifier():
    reviews = db.get_all_reviews()
    label = np.where(reviews["stars"] >= 4, "pos", "neg")
    model = Pipeline([
        ("vectorizer", TfidfVectorizer(min_df=3)),
        ("classifier", LogisticRegression(C=10))
    ])
    model.fit(reviews["review"], label)
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
