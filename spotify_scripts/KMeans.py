import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from kneed import KneeLocator

# creates a graph that shows the cumulative feature variance
def plotFeatureVariance(evr):
    # visualization of the variance of each feature
    plt.figure(figsize=(10,8))
    plt.plot(range(1,9), evr.cumsum(), marker='o', linestyle='--')
    plt.title('Explained Variance by Components')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.show()

# creates a graph showing the WCSS for K-Means using different numbers of clusters
def plotWCSS(wcss):
    plt.figure(figsize=(10,8))
    plt.plot(range(1,21), wcss, marker='o', linestyle='--')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.title('K-Means with PCA Clustering')
    plt.show()

# creates a graph to visualize the clusters
def clusterRadarChart(df, featureLabels, numClusters):
    radarLabels = [*featureLabels, featureLabels[0]]
    label_loc = np.linspace(start=0, stop=2*np.pi, num=len(radarLabels))
    plt.figure(figsize=(10,10))
    plt.subplot(polar=True)

    for cluster in range(numClusters):
        print(df.loc[df['cluster'] == cluster],'\n')
        clusterAverages = featureAverages(df, featureLabels, cluster)
        plt.plot(label_loc, [*clusterAverages, clusterAverages[0]], label='Cluster: ' + str(cluster))

    plt.title('Song clusters', size=20)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=radarLabels)
    plt.legend()
    plt.show()

# finds the average for each feature in the cluster
def featureAverages(df, featureLabels, cluster):
    return df.loc[df['cluster'] == cluster, featureLabels].mean(numeric_only=True).array

# determines the number of features needed to reach 80% variance
def optimalNumFeatures(xStd):
    featureCountPca = PCA()
    featureCountPca.fit(xStd)
    evr = featureCountPca.explained_variance_ratio_
    evrCum = np.array(evr.cumsum())
    return evr, np.where(evrCum > 0.8)[0][0] + 1

# determines the optimal number of clusters using within cluster sum of squares (WCSS)
def optimalNumClusters(scoresPca):
    wcss = []
    for i in range(1,21):
        kmeansPca = KMeans(n_clusters=i, random_state=42)
        kmeansPca.fit(scoresPca)
        wcss.append(kmeansPca.inertia_)
    # locates the elbow to determine number of clusters
    return wcss, KneeLocator([i for i in range(1, 21)], wcss, curve='convex', direction='decreasing').knee

# given a list of songs use PCA and K-Means to seperate into different clusters
def kMeans(df, featureLabels):
    # seperate only the numeric data from the dataframe
    dfX = df[featureLabels]
    # standardize all the features so they have equal weighting
    scaler = StandardScaler()
    xStd = scaler.fit_transform(dfX)

    # compute the number of components needed for 80% variance
    evr, numComponents = optimalNumFeatures(xStd)

    # show graph of feature variance
    # plotFeatureVariance(evr)

    # using the number of features determined above create a new PCA object initailized with that value
    pca = PCA(n_components=numComponents)
    pca.fit(xStd)
    scoresPca = pca.transform(xStd)
    
    # compute the optimal number of clusters (k) to minimize the WCSS
    wcss, numClusters = optimalNumClusters(scoresPca)

    # show graph of wcss for each number of clusters using K-Means
    # plotWCSS(wcss)

    # complete KMeans with the optimal number of clusters
    kmeanPCA = KMeans(n_clusters=numClusters, random_state=42)
    kmeanPCA.fit(scoresPca)

    # adds column to dataframe that represents the associated cluster
    df = df.assign(cluster = kmeanPCA.labels_)

    # normalize all of the audio features in the data frame
    for feature in featureLabels:
        df.loc[:, feature] = (dfX[feature] - dfX[feature].min()) / (dfX[feature].max() - dfX[feature].min())

    # create a radar chart to visualize clustering based on all the features
    clusterRadarChart(df, featureLabels, numClusters)

    return df, numClusters

# TODO: alter this when we determine activity properties
# select a cluster based on the activity selection by the user in the website and return the song ids
def selectCluster(df, numClusters, activity):
    return df.loc[df['cluster'] == 1]['uri'].array