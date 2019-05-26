import pickle

import pandas as pd
from flask import current_app, flash
# aggiungere quì import necessari in build_index

from . import db

INDEX_FILENAME = "movies_index.pkl"

def build_index():
    # reperisci dati di tutti i film
    movies = db.get_all_movies()
    # costruisci indice (spazio vettoriale e vettori dei film)
    raise Exception("INSERIRE ISTRUZIONI MANCANTI QUI")
    # vect = ...
    # dtm = ...
    # salva indice su file
    with current_app.open_instance_resource(INDEX_FILENAME, "wb") as f:
        pickle.dump((movies.id, vect, dtm), f)
    # mostra messaggio all'utente
    flash("Built matrix of movies names with {} terms".format(len(vect.get_feature_names())))

def search_movie(query_str):
    # carica indice da file
    with current_app.open_instance_resource(INDEX_FILENAME, "rb") as f:
        mids, vectorizer, dtm = pickle.load(f)
    # converti stringa cercata in vettore
    query_bow = vectorizer.transform([query_str])
    # calcola similarità tra stringa cercata e titoli di tutti i film
    similarities = pd.Series(dtm.dot(query_bow.T).toarray().ravel(), index=mids).sort_values(ascending=False)
    # seleziona i 50 film con similarità maggiore
    similarities = similarities[similarities>0].head(50)
    # reperisci informazioni sui film
    movies = db.get_movies([int(x) for x in similarities.index])
    return movies
