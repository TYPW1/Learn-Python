# Step 1: Import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk import sent_tokenize
nltk.download('punkt_tab')
# Step 2: text data
documents = [
    "Text clustering is a task in NLP.",
    "NLP involves text preprocessing and feature extraction.",
    "K-Means is a popular clustering algorithm.",
    "Evaluation of clustering can be done using various metrics.",
    "Word embeddings capture semantic meaning.",
    "Hierarchical clustering builds a hierarchy of clusters.",
    "DBSCAN identifies clusters based on density.",
    "Clustering is used in document organization.",
    "Preprocessing includes tokenization and stop word removal.",
    "Dimensionality reduction helps in visualization."
]


# Example summaries (replace with your actual content)
my_summary = """
This paper addresses the problem of software testing by proposing a new mutation testing tool.
It also outlines the limitations of current testing methods and suggests how their tool overcomes them.
"""

llm_summary = """
The article introduces a novel approach to mutation testing. It begins by discussing current challenges in software testing and explains how the new tool improves test effectiveness.
"""

my_sentences = sent_tokenize(my_summary)
llm_sentences = sent_tokenize(llm_summary)

all_sentences = my_sentences + llm_sentences
# Step 3: Text Preprocessing and Feature Extraction using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Step 4: Dimensionality Reduction (optional, for visualization)
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X.toarray())

# Step 5: Clustering using K-Means
kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(X)

# Step 6: Visualization
plt.figure(figsize=(10, 7))
scatter = plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=clusters, cmap='viridis')
plt.title("Text Clustering Visualization")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

# Adding cluster centers to the plot
centers = kmeans.cluster_centers_
centers_reduced = pca.transform(centers)
plt.scatter(centers_reduced[:, 0], centers_reduced[:, 1], c='red', s=200, alpha=0.75, marker='X')

# Adding labels to the plot
for i, txt in enumerate(documents):
    plt.annotate(txt, (X_reduced[i, 0], X_reduced[i, 1]), fontsize=9, alpha=0.75)

plt.colorbar(scatter, label='Cluster Label')
plt.show()
