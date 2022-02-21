from cmath import polar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from kneed import KneeLocator

from SongFeatures import getTracksAudioFeatures
from TrackGeneration import songList

featureLabels = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "valence", "tempo"]
df = getTracksAudioFeatures(songList)
print(df)
df_X = df[featureLabels]

# standardize all the features so they have equal weighting
scaler = StandardScaler()
X_std = scaler.fit_transform(df_X)

# determine how many feature components we need to have to achieve at least 80% variance
featureCountPca = PCA()
featureCountPca.fit(X_std)
evr = featureCountPca.explained_variance_ratio_

# visualization of the variance of each feature
plt.figure(figsize=(10,8))
plt.plot(range(1,9), evr.cumsum(), marker='o', linestyle='--')
plt.title('Explained Variance by Components')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.show()

# using the number of features determined above create a new PCA object initailized with that value
pca = PCA(n_components=5)
pca.fit(X_std)
scoresPca = pca.transform(X_std)

# determine the optimal number of clusters (k) for kMeans
wcss = []
for i in range(1,21):
    kmeansPca = KMeans(n_clusters=i, random_state=42)
    kmeansPca.fit(scoresPca)
    wcss.append(kmeansPca.inertia_)

# grapically show the Within Cluster Sum of Squares (WCSS) to find the optimal number of clusters
plt.figure(figsize=(10,8))
plt.plot(range(1,21), wcss, marker='o', linestyle='--')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('K-Means with PCA Clustering')
plt.show()

# locate the elbow to determine number of clusters
numClusters = KneeLocator([i for i in range(1, 21)], wcss, curve='convex', direction='decreasing').knee
print(numClusters)

# complete KMeans with the optimal number of clusters
kmeanPCA = KMeans(n_clusters=numClusters, random_state=42)
kmeanPCA.fit(scoresPca)
df['Cluster'] = kmeanPCA.labels_

# normalize all of the audio features in the data frame
for feature in featureLabels:
    df[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())

# create a radar chart to visualize clustering based on all the features
radarLabels = [*featureLabels, featureLabels[0]]
label_loc = np.linspace(start=0, stop=2*np.pi, num=len(radarLabels))
plt.figure(figsize=(10,10))
plt.subplot(polar=True)

for cluster in range(numClusters):
    print(df.loc[df['Cluster'] == cluster],'\n')
    clusterAverages = df.loc[df['Cluster'] == cluster, featureLabels].mean(numeric_only=True).array
    plt.plot(label_loc, [*clusterAverages, clusterAverages[0]], label='Cluster: ' + str(cluster))

plt.title('Song clusters', size=20)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=radarLabels)
plt.legend()
plt.show()