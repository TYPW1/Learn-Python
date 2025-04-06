import numpy as np

def compute_A12(metric_MbertP, metric_CosmicRay):
    N1, N2 = len(metric_MbertP), len(metric_CosmicRay)
    count = sum((m1 > m2) + 0.5 * (m1 == m2) for m1 in metric_MbertP for m2 in metric_CosmicRay)
    return count / (N1 * N2)

# Example usage:
mutation_scores_MbertP = [11.11, 9.52,43.86,25.00, 27.71]  # Extracted from mutation_metrics.json
mutation_scores_CosmicRay = [100.00, 100.00, 43.86, 25.00, 25.71]  # Extracted from cosmicraymutation_metrics.json

A12_mutation_score = compute_A12(mutation_scores_MbertP, mutation_scores_CosmicRay)
print("A12 Effect Size for Mutation Score:", A12_mutation_score)
