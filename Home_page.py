import streamlit as st

# Definisco la funzione per caricare il dataframe e memorizzo i dati
import pandas as pd
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path,encoding="utf-8")
    return df

# Titolo e sottotitolo dell'app
st.title(":rainbow[SpotiStats]")
st.subheader("Una web app per l'analisi di un dataset di canzoni")

st.divider()

# Informazioni sul dataset
st.markdown("""
Il **Dataset** su cui l'analisi è stata svolta è consultabile [qui](https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs/data)

In questa app troverai le seguenti pagine:
- :chart_with_upwards_trend:**Word Frequency Analysis**: analisi delle parole usate più di frequente nei testi
- :handshake:**Text Similarity**: permette di selezionare due canzoni e calcolare la somiglianza tra i due testi
- :globe_with_meridians:**Clustering**: raggruppamento delle canzoni in cluster in base alle loro caratteristiche audio
            """)
st.divider()

st.markdown('**Sviluppato da**: Virginia Ranciaro e Irene Vivani')



















