import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from Home_page import load_data
df_audio_features = load_data('spotify_songs.csv')
df_audio_features = df_audio_features.loc[df_audio_features['language']=='en']

st.markdown('### Esplora i risultati del clustering')

# Controlla se ci valori null nel dataframe
print(df_audio_features.isnull().sum())

# Elimina righe con valori null
df_audio_features = df_audio_features.dropna()

# Seleziona le caratteristiche audio rilevanti per il clustering
features = ['speechiness', 'instrumentalness', 'acousticness']
df_features = df_audio_features[features]

# Calcola lo Z-score per identificare gli outlier (qualsiasi dato con uno Z.score maggiore di 3)
z_scores = np.abs(stats.zscore(df_features))
# Crea una maschera booleana per mantenere solo le righe senza outlier
outlier_mask = (z_scores < 3).all(axis=1)  
# Filtra il dataframe per escludere le righe con outlier
df_features_no_outliers = df_features[outlier_mask]

# Standardizza i dati senza outlier
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_features_no_outliers)

# Applica la PCA (Principal Component Analysis) per ridurre la dimensionalità dei dati a 2 dimensioni
pca = PCA(n_components=2)
df_pca = pca.fit_transform(df_scaled)

# Calcola il numero ottimale di cluster in un range da 2 a 10 usando il Silhouette score
silhouette_scores = []
range_n_clusters = range(2, 11) 

# Itera sul range di cluster per calcolare il Silhouette score
for n_clusters in range_n_clusters:
    # Inizializza e applica l'algoritmo K-means
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, max_iter=300, random_state=42)
    # Predice le etichette dei cluster per i dati standardizzati
    cluster_labels = kmeans.fit_predict(df_scaled)
    # Calcola il Silhouette score per le etichette ottenute
    silhouette_avg = silhouette_score(df_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg)

# Determina il numero ottimale di cluster
# 'np.argmax' trova l'indice del valore massimo nella lista dei Silhouette score
optimal_n_clusters = np.argmax(silhouette_scores) + 2  # Aggiunge +2 perché il range parte da 2
# Ottiene il Silhouette score corrispondente
optimal_silhouette_score = silhouette_scores[optimal_n_clusters - 2]
# Mostra il numero ottimale di cluster con il corrispondente Silhouette score
st.write(f'Numero ottimale di cluster: {optimal_n_clusters}, Silhouette score: {optimal_silhouette_score:.4f}')

# Applica K-means con il numero ottimale di cluster individuato
kmeans = KMeans(n_clusters=optimal_n_clusters, random_state=42)
# Predice le etichette dei cluster per i dati standardizzati
cluster_labels = kmeans.fit_predict(df_scaled)

# Calcola e mostra i valori medi delle colonne 'acousticness', 'speechiness' e 'instrumentalness' per ogni cluster
for i in range(optimal_n_clusters):
    cluster_df = df_audio_features[outlier_mask][cluster_labels == i]  # Usa la maschera per filtrare
    st.write(f"Valori medi di 'acousticness', 'speechiness' e 'instrumentalness' per il cluster {i + 1}:")
    st.write(cluster_df[['speechiness', 'acousticness', 'instrumentalness']].mean())

# Aggiunge una colonna 'cluster' al dataframe originale
df_audio_features['cluster'] = np.nan  # Inizializza la colonna 'cluster' con NaN
df_audio_features.loc[outlier_mask, 'cluster'] = cluster_labels  # Assegna le etichette di cluster solo alle righe senza outlier

# Crea un dataframe che conta il numero di canzoni per ogni genere presenti all'interno di ciascun cluster
genre_counts = df_audio_features.groupby(['cluster', 'playlist_genre']).size().reset_index(name='count')

# Ordina i generi per ogni cluster in ordine decrescente di occorrenze
sorted_genre_counts = genre_counts.sort_values(['cluster', 'count'], ascending=[True, False])

# Mostra la distribuzione dei generi per in ogni cluster
for cluster in range(optimal_n_clusters):
    st.write(f'Distribuzione dei generi nel cluster {cluster + 1}:')
    # Filtra i generi per il cluster corrente
    cluster_genres = sorted_genre_counts[sorted_genre_counts['cluster'] == cluster]
    # Mostra i generi e il loro conteggio
    st.write(cluster_genres[['playlist_genre', 'count']])
    st.write('') # A capo per separare i cluster

# Mostra uno scatterplot dei cluster ottenuti
plt.figure(figsize=(8, 6))
plt.scatter(df_pca[:, 0], df_pca[:, 1], c=cluster_labels, cmap='viridis', alpha=0.5)
plt.title('Clustering delle canzoni ottenuto con K-mean:')
plt.colorbar(label='Cluster Label')
st.pyplot(plt)
