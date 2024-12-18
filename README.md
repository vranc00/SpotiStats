# SpotiStats

## Una web app per l`analisi di un dataset di canzoni

### Descrizione

Questo progetto propone un`analisi di dati estratti da un dataset Kaggle che raccoglie testi e caratteristiche audio di oltre 18.000 canzoni.
Sono state selezionate e normalizzate soltanto le canzoni con testi in lingua inglese; su di esse viene effettuata un`analisi delle frequenze delle parole, della somiglianza tra i testi e un`operazione di clustering basata su alcune caratteristiche audio. I risultati sono disponibili su una web app Streamlit con cui l`utente può interagire.

### Istruzioni per l`uso

1. Clonare la repository da GItHub:

```
git clone https://github.com/username/repository.git
```

2. Installare le dipendenze:

```
pip install -r requirements.txt
```

3. Avviare da terminale la web app:

```
streamlit run Home_page.py
```

4. Una volta avviata la web app, è possibile interagire direttamente con le pagine.

### Descrizione dei file e delle librerie

Il progetto è distribuito su cinque file .py contenuti nella repository:

1. normalizzazione.py --- contiene il codice per la normalizzazione dei testi delle canzoni, che utilizza la libreria `nltk` integrata con un elenco di stopwords esterno contenuto nel file `stopwords-en.txt`. Il dataframe viene gestito con la libreria `pandas`.

2. Home_page.py --- contiene il codice per la landing page della web app, dove viene presentato il progetto e fornito il link al dataset. In questo file viene anche definita la funzione `load_data()` per caricare il dataframe, che viene poi importata negli altri script.

3. 1_Word_Frequency_Analysis.py --- contiene il codice per la pagina `Word Frequency Analysis`, dove sono presenti l`analisi delle frequenze delle parole e la visualizzazione dei risultati. Le librerie utilizzate sono `pandas` e `collections` per l`analisi dei dati testuali e `matplotlib.pyplot` per la creazione dei grafici. L`utente può interagire con la pagina mediante dei widget.

4. 2_Text_Similarity.py --- contiene il codice per la pagina `Text Similarity`, dove l’utente può selezionare due canzoni da due diversi dropdown menu e visualizzare la percentuale di similarità tra i due testi. La vettorizzazione dei testi e il calcolo della similarità coseno sono stati progettati con i moduli `feature_extraction.text` e `metrics.pairwise` della libreria `scikitlearn`.

5. 3_Clustering.py --- contiene il codice per la pagina `Clustering`, che presenta i risultati del processo di clusterizzazione delle canzoni sulla base di tre caratteristiche audiometriche (`speechiness`, `instrumentalness` e `acousticness`). Lo script utilizza le librerie `pandas`, `numpy`, e `scipy` per la pulizia dei dati, mentre per la standardizzazione sono stati usati i moduli `preprocessing`, `metrics` e `decomposition` di `scikitlearn`. Il clustering viene effettuato con l`algoritmo K-means, contenuto nella funzione `KMeans()` importata dal modulo `cluster` di `scikitlearn`. I grafici sono stati creati con `matplotlib`.

### Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file `LICENSE` per i dettagli.
