from os import path

from flask import render_template, request, abort, redirect, url_for

from . import app, db, search, reviews, twitter

# home page
@app.route("/")
def home():
    # verifica la presenza della cartella "instance" e del database in essa
    if not path.isdir(app.instance_path):
        return render_template("error_datadir.html", datadir=app.instance_path)
    elif not path.isfile(path.join(app.instance_path, "dimdb.db")):
        return render_template("error_nodb.html", datadir=app.instance_path,
                               dbfile=db.DB_FILENAME, dburl=db.DB_URL)
    # seleziona 5 film casuali da mostrare
    highlights = db.get_random_movies(5)
    return render_template("home.html", highlights=highlights.to_records())

# scheda di un film (mid = ID del film nel database)
@app.route("/movie/<int:mid>")
def movie_details(mid):
    # reperisci le informazioni base sul film
    movie = db.get_movie(mid)
    # se il film con l'ID dato non esiste, da errore 404 Not Found
    if not movie:
        abort(404)
    # reperisci le recensioni in forma di DataFrame pandas
    # (il numero di stelle è nella colonna "stars")
    reviews = db.get_movie_reviews(mid)
    # (to_records converte il DataFrame in una lista di oggetti
    # compatibili con Jinja2)
    return render_template("movie.html", movie=movie,
            reviews=reviews.to_records())

# scheda utente (simile a scheda film)
@app.route("/user/<int:uid>")
def user_details(uid):
    user = db.get_user(uid)
    if not user:
        abort(404)
    reviews = db.get_user_reviews(uid)
    return render_template("user.html", user=user, reviews=reviews.to_records())

# risultati ricerca
@app.route("/search")
def movie_search():
    # ottieni stringa da cercare da form
    query = request.args["q"]
    # esegui ricerca
    results = search.search_movie(query)
    return render_template("search.html", query=query, results=results.to_records())

# test classificatore recensioni
@app.route("/classifier")
def review_classifier_test():
    # ottieni testo da classificare (vuoto di default)
    text = request.args.get("text", "")
    # classifica il testo se non vuoto (ottieni probabilità positivo/negativo)
    probabilities = reviews.classify_review(text) if text else None
    return render_template("classifier_test.html", text=text,
                           probabilities=probabilities)

# pagina con tweet su un film
@app.route("/movie/<int:mid>/tweets")
def movie_tweets(mid):
    # reperisci informazioni sul film e da errore 404 se non esiste
    movie = db.get_movie(mid)
    if not movie:
        abort(404)
    # reperisci tweet recenti sul film
    tweets = twitter.search_tweets(movie["name"])
    # crea risultati da mostrare con tweet e loro classificazione
    results = [
        {"tweet": tweet, "probs": reviews.classify_review(tweet.text)}
        for tweet in tweets
    ]
    return render_template("tweets.html", movie=movie, tweets=results)

# esegui download del database e redireziona ad home page quando finito
@app.route("/getdb", methods=["POST"])
def download_db():
    db.download_db_file()
    return redirect(url_for("home"))

# pagina amministrazione
@app.route("/admin")
def admin_page():
    return render_template("admin.html")

# esegui costruzione indice di ricerca
@app.route("/reindex", methods=["POST"])
def reindex_movies():
    search.build_index()
    return redirect(url_for("admin_page"))

# esegui addestramento classificatore di recensioni
@app.route("/retrain", methods=["POST"])
def retrain_review_classifier():
    reviews.train_review_classifier()
    return redirect(url_for("review_classifier_test"))
