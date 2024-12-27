import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


from Home_page import load_data
df = load_data('normalized_selected_data.csv')

# Converte la data di uscita in datetime ed estrae l'anno
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], format='mixed')
df['track_album_release_year'] = df['track_album_release_date'].dt.year.astype(int)

# Raggruppa le canzoni per decennio
decades = {
    #'Anni 50': df[df['track_album_release_year'] < 1960],
    'Anni 60': df[(df['track_album_release_year'] >= 1960) & (df['track_album_release_year'] < 1970)],
    'Anni 70': df[(df['track_album_release_year'] >= 1970) & (df['track_album_release_year'] < 1980)],
    'Anni 80': df[(df['track_album_release_year'] >= 1980) & (df['track_album_release_year'] < 1990)],
    'Anni 90': df[(df['track_album_release_year'] >= 1990) & (df['track_album_release_year'] < 2000)],
    'Anni 2000': df[(df['track_album_release_year'] >= 2000) & (df['track_album_release_year'] < 2010)],
    'Anni 10': df[(df['track_album_release_year'] >= 2010) & (df['track_album_release_year'] < 2020)],
    #'Anni 20': df[(df['track_album_release_year'] >= 2020) & (df['track_album_release_year'] < 2030)]
}

# Funzione per calcolare le 5 parole più frequenti per ogni sottoinsieme
def five_most_freq_words(decade):
    lyrics = ' '.join(lyric for lyric in decade['lyrics'] if isinstance(lyric, str))
    # Conta le parole direttamente usando Counter
    most_freq_words = Counter(lyrics.split()).most_common(5)
    return most_freq_words

# Titolo e istruzioni
st.markdown('### Scegli un’epoca musicale e scopri le cinque parole più ricorrenti')

# Dropdown menu per selezionare il decennio
selected_decade = st.selectbox('Seleziona un decennio', list(decades.keys()))

st.write('')

if st.button('Calcola'):
    # Calcolo le parole più frequenti e memorizzo in un dizionario
    most_freq_words = five_most_freq_words(decades[selected_decade])
    st.write('Le 5 parole più frequenti sono:')
    for n, (word, count) in enumerate(most_freq_words, start=1):
        st.write(f'{n}) {word}')

    def plot_word_occurrences(decade, most_freq_words):
        
        # Itera attraverso ogni parola nella lista delle parole più frequenti
        for word, _ in most_freq_words:
            # Conta le occorrenze della parola per ogni anno nel decennio
            word_counts = decade.groupby('track_album_release_year')['lyrics'].apply(lambda lyrics: ' '.join(lyric for lyric in lyrics if isinstance(lyric, str)).split().count(word))
            
            # Crea un grafico per la parola corrente
            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(word_counts.index, word_counts, marker='o', label=word)
            
            ax.set_title(f'Occorrenze della parola {word.upper()} attraverso il decennio')
            ax.set_xlabel('Anno')
            ax.set_ylabel('Numero di Occorrenze')
            ax.set_xticks(word_counts.index)
            ax.legend(title='Parola')
            ax.grid()
            st.pyplot(fig)



    # Traccia le occorrenze
    plot_word_occurrences(decades[selected_decade], most_freq_words)