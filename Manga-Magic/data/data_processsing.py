import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval

# Load Data
meta_data = pd.read_csv('Manga-Magic\data\data.csv',low_memory=False)

print("Original Data:",meta_data.shape) # Check size to ensure it is complete 

# Filter out incomplete data
qualified_data = meta_data.copy().loc[meta_data['description'] != "This entry currently doesn't have a synopsis. Check back soon!"]

print("Qualified Data:",qualified_data.shape) # Get Size of qualified data to comparision purposes

#Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

qualified_data['description'] = qualified_data['description'].fillna('')

#Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(qualified_data['description'])

print("(<amount of data>,<amount of keywords>) : ",tfidf_matrix.shape) # Check size of matrix (<amount of data>,<amount of keywords>)

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) # Compute the cosine similarity matrix for each movie in the dataset to each other

#Construct a reverse map of indices and movie titles
indices = pd.Series(qualified_data.index, index=qualified_data['title']).drop_duplicates()

def get_reccomendations(title , cosine_sim=cosine_sim):
    # Get the index of the manga/manhwa/manhua that matches the title
    idx = indices[title]
   
    # Get the pairwsie similarity scores of all manga/manhwa/manhua with that manga/manhwa/manhua
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar manga/manhwa/manhua
    sim_scores = sim_scores[1:11]

    # Get the manga/manhwa/manhua indices
    manga_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar manga/manhwa/manhua
    return qualified_data['title'].iloc[manga_indices]

print(get_reccomendations('Kingdom')) # Test the function