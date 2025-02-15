import numpy as np

def levenshtein(s1, s2):
    """Compute Levenshtein distance between two strings."""
    n, m = len(s1), len(s2)
    dp = np.zeros((n + 1, m + 1), dtype=int)

    # Initialize first row and column
    for i in range(n + 1):
        dp[i][0] = i  # Cost of deleting all characters from s1
    for j in range(m + 1):
        dp[0][j] = j  # Cost of inserting all characters into s1

    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1  # Substitution cost
            dp[i, j] = min(
                dp[i - 1, j] + 1,    # Deletion
                dp[i, j - 1] + 1,    # Insertion
                dp[i - 1, j - 1] + cost  # Substitution
            )

    return dp[n, m]
