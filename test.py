from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def concat_phrases_in_sentences(sentences, phrases, threshold=0.5):
    concatenated_string = ""

    # Combine sentences and phrases for vectorization
    combined_text = sentences + phrases
    
    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer().fit(combined_text)
    sentence_vectors = vectorizer.transform(sentences)
    phrase_vectors = vectorizer.transform(phrases)
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(phrase_vectors, sentence_vectors)

    # Find and concatenate phrases with similarity above the threshold
    for i, phrase in enumerate(phrases):
        if np.any(similarity_matrix[i] > threshold):
            concatenated_string += phrase + " "

    # Remove trailing space
    concatenated_string = concatenated_string.strip()

    return concatenated_string

# Example usage
sentences = [
    "The head of a black fox was seen in the forest.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question."
]
phrases = ["head of black", "single step", "not to be"]

result = concat_phrases_in_sentences(sentences, phrases)
print(result)
