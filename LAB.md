Laboratorio: Applicazioni Web con Flask
=======================================

In questo laboratorio vediamo un esempio di applicazione Web realizzata in Flask di cui sono da completare alcune parti.

Setup
-----

1. Scaricare il progetto sul proprio PC
  - eseguire in un terminale `git clone https://github.com/datascienceunibo/dimdb`
  - _oppure_ [scaricare l'archivio ZIP del repository](#) ed estrarne i file in una directory vuota

2. Aprire un terminale e impostare come directory corrente (`cd`) quella del progetto, eseguire in esso i comandi dei punti seguenti

3. Creare un nuovo ambiente virtuale
  - `python -m venv venv` (sostituire `python` con `python3` su Mac OS o Linux)

4. Attivare l'ambiente virtuale
  - `venv\bin\activate.bat` (su Windows)
  - `source venv/bin/activate` (su Mac OS e Linux)

5. Installare le librerie necessarie, elencate nel file `requirements.txt`
  - `pip install -r requirements.txt`

6. Impostare le variabili d'ambiente necessarie
  - su Windows usare `set` come indicato sotto, su Mac OS o Linux sostituire `set` con `export`
  - `set FLASK_APP=dimdb`
  - `set FLASK_DEBUG=true`

7. Creare una directory `instance` dove sono salvati i dati dell'applicazione
  - `mkdir instance`

8. Avviare il webserver di Flask
  - `python -m flask run`

9. Aprire l'URL http://127.0.0.1:5000/ nel browser

10. Cliccare sul pulsante "Download" per scaricare il database usato dall'applicazione e metterla in funzione

Introduzione
------------

**DIMDb** (_Data Intensive Movie Database_) è un semplice database di film che include delle recensioni scritte dagli utenti. Nell'applicazione fornita è possibile solamente consultare il database, per semplicità non è prevista l'autenticazione degli utenti e la pubblicazione o modifica di contenuti.

Struttura del progetto
----------------------

Nel package `dimdb` si trovano:
- il file `__init__.py` dove viene inizializzata e configurata l'applicazione Flask
- il modulo `db.py` con le funzioni per la lettura dei dati dal database SQLite
- il modulo `pages.py` con le funzioni che generano le pagine Web
- la directory `templates` con i template HTML delle pagine
  - `master.html` è il template master con la struttura generale (che comprende header e footer) usata da tutte le pagine
  - `macros.html` contiene alcune macro d'utilità
  - gli altri file corrispondono alle diverse pagine dell'applicazione
- la directory `static` con i file statici dell'applicazione
  - in questo caso solo il foglio di stile `style.css` usato nel template master

Esercizio 1: visualizzazione dati in template
---------------------------------------------

Aprendo la pagina di un film (vedere ad esempio uno dei 5 mostrati casualmente in home page) si vedono già la locandina e la descrizione, mentre è solamente abbozzata la visualizzazione delle recensioni scritte dagli utenti.

**Completare la visualizzazione delle recensioni nel template `movie.html`**, inserendo gli opportuni tag in corrispondenza delle scritte in maiuscolo. Le recensioni sono fornite nella lista `reviews` passata al template: per ciascuna sono disponibili gli attributi `user_id`, `user_name`, `stars`, `summary`, `review`. Aggiungere nella funzione **`movie_details` in `pages.py`** che richiama il template il codice per ottenere la media di stelle delle recensioni.

Utilizzo di modelli all'interno dell'applicazione
-------------------------------------------------

Nelle precedenti esercitazioni abbiamo visto come addestrare modelli di predizione da un set di dati e come valutarli ed utilizzarli all'interno della stessa sessione di lavoro.

In un'applicazione Web, dove ogni richiesta è gestita da un processo separato, non abbiamo modelli già addestrati in memoria. In genere non possiamo ripetere l'addestramento di un modello ad ogni richiesta, in quanto i tempi di risposta sarebbero lunghi.

La soluzione è addestrare il modello una singola volta, salvare tale modello addestrato in un file e caricarlo dallo stesso file ad ogni richiesta.

Il modulo `pickle` della libreria standard di Python fornisce funzionalità per la (de)serializzazione di oggetti Python, inclusi modelli di conoscenza. Una volta addestrato un modello possiamo ottenerne una rappresentazione binaria e salvarla in un file; quando necessario possiamo ricaricare tale rappresentazione dal file e ricostruire da essa il modello addestrato.

Sia dato un modello (ad es. di regressione lineare) addestrato su un set di dati...

```
model = LinearRegression()
model.fit(X_train, y_train)
```

...possiamo serializzarlo su un file `foo.bin` utilizzando la funzione `pickle.dump` in questo modo:

```
with open("foo.bin", "wb") as f:
    pickle.dump(model, f)
```

In seguito, sarà possibile ricaricare il modello tramite la funzione `pickle.load` in questo modo:

```
with open("foo.bin", "rb") as f:
    model = pickle.load(f)
```

Il modello può così essere utilizzato come se fosse appena addestrato.

```
preds = model.predict(X_test)
```

In un'applicazione Web possiamo quindi utilizzare modelli già addestrati caricandoli da file. I tempi per il caricamento sono generalmente trascurabili.

Esercizio 2: ricerca testuale
-----------------------------

Nell'applicazione è predisposta la ricerca di film per titolo. Per supportare la ricerca i titoli dei film sono rappresentati in uno spazio vettoriale; ogni stringa cercata dall'utente viene convertita in vettore in tale spazio e viene calcolata la similarità coseno con quelli dei film, quelli a cui corrisponde similarità più alta sono i risultati della ricerca.

**Completare l'implementazione di `build_index` in `search.py`** in modo che sia creato un vectorizer `vect` ed addestrato sui nomi dei film (colonna `name` del DataFrame `movies`) estraendo la corrispondente matrice documenti-termini `dtm`. Per testare il funzionamento, cliccare su "Build vector space" nella pagina di amministrazione. Testare diverse configurazioni del vectorizer e verificare per quale i risultati delle ricerche appaiano più accurati (ad. es impostare `analyzer="char"` e `ngram_range=(3, 3)` per usare sequenze di tre lettere al posto delle singole parole).

Esercizio 3: classificazione di tweet
-------------------------------------

Nell'applicazione è possibile visualizzare i tweet pubblicati recentemente su Twitter che parlano di un film. Un classificatore addestrato sulle recensioni mostrate dall'applicazione viene utilizzato per etichettare i tweet come positivi o negativi.

**Completare l'implementazione di `train_review_classifier` in `reviews.py`** in modo che venga addestrato un modello di regressione logistica sulle recensioni etichettate come positive (stelle >= 4) o negative (stelle < 4). Per testare il funzionamento cliccare su "Train reviews classifier" nella pagina di amministrazione, usare l'interfaccia predisposta per testare il classificatore su frasi inserite manualmente e vedere le pagine di tweet di alcuni film.
