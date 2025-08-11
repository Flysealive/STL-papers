import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_rel
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Create sample dataset of 20 students
n_students = 20

# Generate student IDs
student_ids = [f"S{i:03d}" for i in range(1, n_students + 1)]

# Generate baseline scores (before AI tools) - normally distributed around 72 with SD of 8
baseline_scores = np.random.normal(72, 8, n_students)
baseline_scores = np.clip(baseline_scores, 50, 95)  # Keep scores in reasonable range

# Generate improvement effect - most students improve, but with variability
# Average improvement of 5 points with SD of 3
improvement = np.random.normal(5, 3, n_students)

# Generate post-AI scores
post_ai_scores = baseline_scores + improvement
post_ai_scores = np.clip(post_ai_scores, 50, 100)  # Keep scores in reasonable range

# Round scores to 1 decimal place
baseline_scores = np.round(baseline_scores, 1)
post_ai_scores = np.round(post_ai_scores, 1)

# Create DataFrame
df = pd.DataFrame({
    'Student_ID': student_ids,
    'Before_AI': baseline_scores,
    'After_AI': post_ai_scores,
    'Improvement': np.round(post_ai_scores - baseline_scores, 1)
})

# Display the dataset
print("Sample Dataset: Writing Scores Before and After Using AI Tools")
print("=" * 60)
print(df.to_string(index=False))
print("\n")

# Basic descriptive statistics
print("Descriptive Statistics")
print("=" * 60)
print(f"Before AI - Mean: {df['Before_AI'].mean():.2f}, SD: {df['Before_AI'].std():.2f}")
print(f"After AI  - Mean: {df['After_AI'].mean():.2f}, SD: {df['After_AI'].std():.2f}")
print(f"Mean Improvement: {df['Improvement'].mean():.2f}, SD: {df['Improvement'].std():.2f}")
print("\n")

# Check normality of differences (assumption for paired t-test)
differences = df['After_AI'] - df['Before_AI']
shapiro_stat, shapiro_p = stats.shapiro(differences)
print("Normality Test (Shapiro-Wilk) for Score Differences")
print("=" * 60)
print(f"Statistic: {shapiro_stat:.4f}, p-value: {shapiro_p:.4f}")
if shapiro_p > 0.05:
    print("Differences appear to be normally distributed (p > 0.05)")
else:
    print("Differences may not be normally distributed (p < 0.05)")
print("\n")

# Perform paired t-test
t_stat, p_value = ttest_rel(df['Before_AI'], df['After_AI'])
mean_diff = df['After_AI'].mean() - df['Before_AI'].mean()
se_diff = differences.std() / np.sqrt(n_students)
ci_lower = mean_diff - 1.96 * se_diff
ci_upper = mean_diff + 1.96 * se_diff

print("Paired t-test Results")
print("=" * 60)
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
print(f"Mean difference: {mean_diff:.2f}")
print(f"95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]")
if p_value < 0.05:
    print("Result: Statistically significant improvement (p < 0.05)")
else:
    print("Result: No statistically significant improvement (p >= 0.05)")
print("\n")

# Calculate effect size (Cohen's d for paired samples)
# For paired samples: d = mean(differences) / SD(differences)
cohens_d = differences.mean() / differences.std()

# Also calculate using pooled SD for comparison
pooled_sd = np.sqrt((df['Before_AI'].var() + df['After_AI'].var()) / 2)
cohens_d_pooled = mean_diff / pooled_sd

print("Effect Size")
print("=" * 60)
print(f"Cohen's d (paired): {cohens_d:.3f}")
print(f"Cohen's d (pooled SD): {cohens_d_pooled:.3f}")
if abs(cohens_d) < 0.2:
    effect_interpretation = "negligible"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "small"
elif abs(cohens_d) < 0.8:
    effect_interpretation = "medium"
else:
    effect_interpretation = "large"
print(f"Interpretation: {effect_interpretation} effect size")
print("\n")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Writing Scores: Before vs After AI Tool Usage', fontsize=16, fontweight='bold')

# 1. Box plot comparison
ax1 = axes[0, 0]
data_for_box = pd.melt(df[['Before_AI', 'After_AI']], var_name='Condition', value_name='Score')
sns.boxplot(data=data_for_box, x='Condition', y='Score', ax=ax1, palette=['lightcoral', 'lightblue'])
sns.swarmplot(data=data_for_box, x='Condition', y='Score', ax=ax1, color='black', alpha=0.5, size=4)
ax1.set_title('Score Distribution Comparison', fontsize=12, fontweight='bold')
ax1.set_xlabel('Condition', fontsize=11)
ax1.set_ylabel('Writing Score', fontsize=11)
ax1.set_xticklabels(['Before AI', 'After AI'])

# Add mean lines
for i, condition in enumerate(['Before_AI', 'After_AI']):
    mean_val = df[condition].mean()
    ax1.hlines(mean_val, i-0.4, i+0.4, colors='red', linestyles='dashed', linewidth=2)

# 2. Paired scores plot
ax2 = axes[0, 1]
for i in range(len(df)):
    ax2.plot(['Before', 'After'], [df.iloc[i]['Before_AI'], df.iloc[i]['After_AI']], 
             'o-', color='gray', alpha=0.5, markersize=4)
ax2.plot(['Before', 'After'], [df['Before_AI'].mean(), df['After_AI'].mean()], 
         'o-', color='red', linewidth=3, markersize=8, label='Mean')
ax2.set_title('Individual Score Changes', fontsize=12, fontweight='bold')
ax2.set_xlabel('Condition', fontsize=11)
ax2.set_ylabel('Writing Score', fontsize=11)
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Distribution of improvements
ax3 = axes[1, 0]
ax3.hist(df['Improvement'], bins=10, color='green', alpha=0.7, edgecolor='black')
ax3.axvline(df['Improvement'].mean(), color='red', linestyle='dashed', linewidth=2, 
            label=f'Mean = {df["Improvement"].mean():.2f}')
ax3.axvline(0, color='black', linestyle='solid', linewidth=1, alpha=0.5)
ax3.set_title('Distribution of Score Improvements', fontsize=12, fontweight='bold')
ax3.set_xlabel('Score Improvement', fontsize=11)
ax3.set_ylabel('Frequency', fontsize=11)
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Statistical summary
ax4 = axes[1, 1]
ax4.axis('off')
summary_text = f"""Statistical Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sample Size: {n_students} students

Before AI:
  Mean ± SD: {df['Before_AI'].mean():.2f} ± {df['Before_AI'].std():.2f}
  Range: [{df['Before_AI'].min():.1f}, {df['Before_AI'].max():.1f}]

After AI:
  Mean ± SD: {df['After_AI'].mean():.2f} ± {df['After_AI'].std():.2f}
  Range: [{df['After_AI'].min():.1f}, {df['After_AI'].max():.1f}]

Paired t-test:
  t({n_students-1}) = {t_stat:.3f}, p = {p_value:.4f}
  Mean difference: {mean_diff:.2f} (95% CI: [{ci_lower:.2f}, {ci_upper:.2f}])
  
Effect Size:
  Cohen's d = {cohens_d:.3f} ({effect_interpretation} effect)

Conclusion:
  {'Significant improvement in writing scores after AI tool usage (p < 0.05)' if p_value < 0.05 else 'No significant improvement detected (p ≥ 0.05)'}
"""
ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=11, 
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.3))

plt.tight_layout()
plt.savefig('paired_ttest_results.png', dpi=300, bbox_inches='tight')
plt.show()

# Save the dataset to CSV
df.to_csv('writing_scores_dataset.csv', index=False)
print(f"Dataset saved to: writing_scores_dataset.csv")
print(f"Visualization saved to: paired_ttest_results.png")