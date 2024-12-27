import streamlit as st
import pandas as pd

from Home_page import load_data
df = load_data('normalized_selected_data.csv')


# TEXT SIMILARITY

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Istruzioni
st.markdown('### Seleziona due canzoni e scopri se i testi sono simili')

# Menu dropdown
selected_song1 = st.selectbox('Seleziona la prima canzone:', df['track_name'].tolist())
selected_song2 = st.selectbox('Seleziona la seconda canzone:', df['track_name'].tolist())

# Mostra le canzoni selezionate
st.write(f'Hai selezionato: *{selected_song1}* e *{selected_song2}*')


# Bottone da cliccare per attivare il calcolo
if st.button('Calcola somiglianza'):
    # Controllo se l'utente ha selezionato due canzoni uguali
    if selected_song1 == selected_song2:
        st.warning('Per favore, seleziona due canzoni diverse')
    else:
        # Estrazione dei testi delle canzoni scelte
        lyrics1 = df.loc[df['track_name'] == selected_song1, 'lyrics'].values[0]
        lyrics2 = df.loc[df['track_name'] == selected_song2, 'lyrics'].values[0]

        # Creo TF-IDF Vectorizer
        vectorizer = TfidfVectorizer()

        vectorizer.fit([lyrics1, lyrics2])

        # Vettorizzare i due testi considerati
        vector1=vectorizer.transform([lyrics1])
        vector2=vectorizer.transform([lyrics2])
            
        # Calcolo della similarità coseno
        similarity=cosine_similarity(vector1,vector2)[0][0]
        similarity_percentage=round(similarity * 100,2)

        st.write('')

        st.metric(label='Somiglianza', value=f'{similarity_percentage}%', delta='')
