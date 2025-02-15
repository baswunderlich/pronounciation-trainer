import numpy as np

def text_to_sequence(text):
    """Convert text into a sequence of characters (case-insensitive)."""
    return list(text.lower())  # Represent text as a list of characters

def dtw(s1, s2, dist=lambda x, y: 0 if x == y else 1):
    """Compute DTW distance between two sequences with a simple mismatch cost."""
    n, m = len(s1), len(s2)
    # Initialize the DTW matrix with infinity
    dtw_matrix = np.full((n + 1, m + 1), np.inf)
    dtw_matrix[0, 0] = 0  # Starting point

    # Populate the DTW matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Calculate cost between characters
            cost = dist(s1[i - 1], s2[j - 1])  
            # Compute the minimum cost of insertion, deletion, or substitution
            dtw_matrix[i, j] = cost + min(
                dtw_matrix[i - 1, j],    # Insertion (extra letter in transcription)
                dtw_matrix[i, j - 1],    # Deletion (missing letter in transcription)
                dtw_matrix[i - 1, j - 1] # Substitution (typo)
            )

    return dtw_matrix[n, m]

def main():
    # Example usage:
    original_text = "The quick brown fox jumps over the lazy dog."
    transcribed_text = "The quick brown box jumps over the lazy dog."

    # Convert texts to sequences of characters
    seq1 = text_to_sequence(original_text)
    seq2 = text_to_sequence(transcribed_text)

    # Compute DTW distance between the two sequences
    distance = dtw(seq1, seq2)

    print(f"DTW Distance: {distance}")

if __name__ == "__main__":
    main()
