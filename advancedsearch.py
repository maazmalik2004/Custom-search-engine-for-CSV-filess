import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz

def load_data(file_path):
    """Load CSV data into a DataFrame."""
    return pd.read_csv(file_path)

def preprocess_documents(data_frame, column_name):
    """Extract and preprocess text data from a specified column."""
    return data_frame[column_name].tolist()

def calculate_similarity(query_terms, documents):
    """Calculate cosine similarity and fuzzy scores for the given query terms."""
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    query_tfidf = tfidf_vectorizer.transform(query_terms)
    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix)
    min_cosine_similarities = cosine_similarities.min(axis=0)
    fuzzy_scores = [fuzz.partial_ratio(" ".join(query_terms).lower(), document.lower()) for document in documents]
    return min_cosine_similarities, fuzzy_scores

def combine_scores(min_cosine_similarities, fuzzy_scores):
    """Combine cosine similarity and fuzzy scores."""
    combined_scores = [0.5 * min_cosine_sim + 0.5 * fuzzy_score / 100 for min_cosine_sim, fuzzy_score in zip(min_cosine_similarities, fuzzy_scores)]
    return combined_scores

def rank_documents(combined_scores, data_frame, documents):
    """Rank documents based on combined scores and print the top 5 ranked documents."""
    sorted_indices = sorted(range(len(combined_scores)), key=lambda i: combined_scores[i], reverse=True)
    print("Top 5 Ranked Documents:")
    for idx in sorted_indices[:5]:
        print(f"cve id: {data_frame.iloc[idx]['cve id']}")
        print(f"pub_date: {data_frame.iloc[idx]['pub_date']}")
        print(f"cvss: {data_frame.iloc[idx]['cvss']}")
        print(f"summary: {documents[idx]}")
        print(f"Combined Score: {combined_scores[idx]}")
        print()

def main():
    # Load data
    file_path = 'C:\\Users\\MI\\Desktop\\dataset\\cve.csv'
    df = load_data(file_path)
    
    # Preprocess documents
    documents = preprocess_documents(df, 'summary')

    # User input for query terms
    query_terms = input("Enter your query terms separated by spaces: ").split()

    # Calculate similarity
    min_cosine_similarities, fuzzy_scores = calculate_similarity(query_terms, documents)

    # Combine scores
    combined_scores = combine_scores(min_cosine_similarities, fuzzy_scores)

    # Rank and print documents
    rank_documents(combined_scores, df, documents)

if __name__ == "__main__":
    main()
