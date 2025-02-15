from levenshtein import levenshtein
from dtw_text import dtw, text_to_sequence
import Levenshtein

def benchmarkAlgorithms(original_text, transcribed_text):
    seq1 = text_to_sequence(original_text)
    seq2 = text_to_sequence(transcribed_text)

    dtw_distance = dtw(seq1, seq2)
    levenshtein_distance = levenshtein(original_text, transcribed_text)

    print(f"DTW Distance: {dtw_distance}")
    print(f"Levenshtein Distance: {levenshtein_distance}")
    print(f"Levenshtein correct distance: {Levenshtein.distance(original_text, transcribed_text)}")
    print(f"score: {calculate_score_dtw(original_text, transcribed_text, dtw_distance)}")
    print(f"score real: {Levenshtein.ratio(original_text, transcribed_text)}")  # USES INDEL distance TODO  what is indel

def calculate_score_dtw(s1, s2, dist):
    """Calculate the DTW-based similarity score between two strings."""
    
    # Compute maximum possible DTW distance
    max_distance = max(len(s1), len(s2))
    
    # Calculate similarity score
    score = 100 * (1 - dist / max_distance)
    
    return score

def main():
    # Same text
    original_text = "The quick brown fox jumps over the lazy dog."
    transcribed_text = "The quick brown fox jumps over the lazy dog."
    benchmarkAlgorithms(original_text, transcribed_text)

    # forgot s from jumps
    original_text = "The quick brown fox jumps over the lazy dog."
    transcribed_text = "The quick brown fox jump over the lazy dog."
    benchmarkAlgorithms(original_text, transcribed_text)

    # wrong animal
    original_text = "The quick brown fox jumps over the lazy dog."
    transcribed_text = "Test The quick brown sheep jumps over the lazy dog."
    benchmarkAlgorithms(original_text, transcribed_text)

    print("corrected")
     # wrong animal
    original_text = "The quick brown fox jumps over the lazy dog."
    transcribed_text = "Test The quick brown sheep fox jumps over the lazy dog."
    benchmarkAlgorithms(original_text, transcribed_text)
    
    # wrong animal
    original_text = "The quick brown fox jumps over the lazy dog."
    transcribed_text = "y"
    benchmarkAlgorithms(original_text, transcribed_text)

main()