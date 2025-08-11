import random
import math

# Set random seed for reproducibility
random.seed(42)

# Create sample dataset of 20 students
n_students = 20

# Generate student IDs
student_ids = [f"S{i:03d}" for i in range(1, n_students + 1)]

# Generate scores manually
# Before AI scores - around 72 with some variation
before_scores = []
for i in range(n_students):
    score = 72 + random.gauss(0, 8)  # mean 72, SD 8
    score = max(50, min(95, score))  # Keep in range
    before_scores.append(round(score, 1))

# After AI scores - generally improved by about 5 points
after_scores = []
improvements = []
for i in range(n_students):
    improvement = random.gauss(5, 3)  # mean improvement 5, SD 3
    after_score = before_scores[i] + improvement
    after_score = max(50, min(100, after_score))  # Keep in range
    after_scores.append(round(after_score, 1))
    improvements.append(round(after_score - before_scores[i], 1))

# Display the dataset
print("Sample Dataset: Writing Scores Before and After Using AI Tools")
print("=" * 60)
print(f"{'Student_ID':<12} {'Before_AI':<10} {'After_AI':<10} {'Improvement':<12}")
print("-" * 44)
for i in range(n_students):
    print(f"{student_ids[i]:<12} {before_scores[i]:<10} {after_scores[i]:<10} {improvements[i]:<12}")

# Calculate basic statistics
def mean(data):
    return sum(data) / len(data)

def std_dev(data):
    m = mean(data)
    variance = sum((x - m) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)

# Descriptive statistics
print("\n\nDescriptive Statistics")
print("=" * 60)
print(f"Before AI - Mean: {mean(before_scores):.2f}, SD: {std_dev(before_scores):.2f}")
print(f"After AI  - Mean: {mean(after_scores):.2f}, SD: {std_dev(after_scores):.2f}")
print(f"Mean Improvement: {mean(improvements):.2f}, SD: {std_dev(improvements):.2f}")

# Paired t-test calculation
differences = [after_scores[i] - before_scores[i] for i in range(n_students)]
mean_diff = mean(differences)
std_diff = std_dev(differences)
se_diff = std_diff / math.sqrt(n_students)
t_stat = mean_diff / se_diff
df = n_students - 1

# Critical value for two-tailed test at alpha = 0.05
# For df = 19, critical value ≈ 2.093
critical_value = 2.093

# Calculate 95% CI
ci_lower = mean_diff - critical_value * se_diff
ci_upper = mean_diff + critical_value * se_diff

print("\n\nPaired t-test Results")
print("=" * 60)
print(f"Mean difference: {mean_diff:.2f}")
print(f"Standard error: {se_diff:.2f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"Degrees of freedom: {df}")
print(f"Critical value (α = 0.05, two-tailed): ±{critical_value}")
print(f"95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]")

if abs(t_stat) > critical_value:
    print("Result: Statistically significant difference (|t| > critical value)")
else:
    print("Result: No statistically significant difference (|t| ≤ critical value)")

# Calculate Cohen's d
cohens_d = mean_diff / std_diff

print("\n\nEffect Size")
print("=" * 60)
print(f"Cohen's d: {cohens_d:.3f}")
if abs(cohens_d) < 0.2:
    effect_interpretation = "negligible"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "small"
elif abs(cohens_d) < 0.8:
    effect_interpretation = "medium"
else:
    effect_interpretation = "large"
print(f"Interpretation: {effect_interpretation} effect size")

# Summary statistics for visualization
print("\n\nData Summary for Visualization:")
print("=" * 60)
print("Score ranges:")
print(f"  Before AI: {min(before_scores):.1f} - {max(before_scores):.1f}")
print(f"  After AI: {min(after_scores):.1f} - {max(after_scores):.1f}")
print("\nNumber of students who improved:", sum(1 for x in improvements if x > 0))
print("Number of students who declined:", sum(1 for x in improvements if x < 0))
print("Number of students with no change:", sum(1 for x in improvements if x == 0))

# Save data to CSV
with open('writing_scores_data.csv', 'w') as f:
    f.write('Student_ID,Before_AI,After_AI,Improvement\n')
    for i in range(n_students):
        f.write(f'{student_ids[i]},{before_scores[i]},{after_scores[i]},{improvements[i]}\n')
print("\nData saved to: writing_scores_data.csv")