import pandas as pd
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Carico il dataset come DataFrame
df = pd.read_csv('spotify_songs.csv', encoding='utf-8')

# Seleziona solo le canzoni in lingua inglese
df = df[df['language'] == 'en']

# Precarica le stopwords e il lemmatizzatore
with open('stopwords-en.txt', 'r', encoding='utf-8') as stopwords_file:
    data = stopwords_file.read()
    stop_words = data.replace('\n', ' ').split()
    stop_words = stop_words + ['gon', 'yeah', 'ya', 'wan', 'ooh']
lemmatizer = WordNetLemmatizer()
translator = str.maketrans('', '', string.punctuation)


def normalize_complete(text):
    # Rimuovi la punteggiatura e converti in minuscolo
    text = str(text).lower().translate(translator)
    # Tokenizza il testo
    tokens = word_tokenize(text)
    # Rimuovi le stopwords e lemmatizza
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return ' '.join(tokens)


def normalize_partial(text):
    # Rimozione delle maiuscole e della punteggiatura, divisione in token
    text = str(text).lower().translate(translator)
    tokens = word_tokenize(text)
    return ' '.join(tokens)


# Applicare la normalizzazione completa sui contenuti della colonna lyrics
df['lyrics'] = df['lyrics'].apply(normalize_complete)

# Applicare la normalizzazione parziale sui contenuti delle colonne track_name e track_artist
columns_to_normalize = ['track_name', 'track_artist']
df[columns_to_normalize] = df[columns_to_normalize].apply(lambda col: col.apply(normalize_partial))


# Creo un nuovo DataFrame con le colonne normalizzate e quella contenente le date di pubblicazione
new_df = df[['track_name', 'lyrics','track_album_release_date']].copy()

file_name = 'normalized_selected_data.csv'
new_df.to_csv(file_name, index=False)