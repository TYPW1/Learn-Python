import re

import nltk
import pandas as pd
from nltk import sent_tokenize
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import KMeans


def read_pdf_text (pdf_file_path):
    reader = PdfReader(pdf_file_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:

            full_text += page_text
    return full_text.strip()

text = read_pdf_text("MySummary.pdf")

#nltk.download("punkt_tab")
clean_text = sent_tokenize(text.lower())

model = SentenceTransformer("all-MiniLM-L6-v2")
text_embeddings = model.encode(clean_text)

def cluster_by_KMeans(embeddings, sentences, number_of_clusters=5, source_label=""):
    kmeans = KMeans(n_clusters=number_of_clusters, random_state=42)

    cluster_labels = kmeans.fit_predict(embeddings)

    print(cluster_labels)

    clustered_data =pd.DataFrame({
        "sentence": sentences,
        "cluster": cluster_labels,
        "source": source_label
    })
    return clustered_data

kmeans_cluster = cluster_by_KMeans(embeddings=text_embeddings,
                                   sentences=clean_text,
                                   number_of_clusters=min(5, len(clean_text)),
                                   source_label="text")
print(kmeans_cluster)