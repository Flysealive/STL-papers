# Paired t-Test Analysis: Writing Scores Before and After AI Tool Usage

## Executive Summary

This analysis examined the impact of AI tool usage on writing scores for 20 students using a paired t-test design. The results show a **statistically significant improvement** in writing scores after AI tool implementation.

## Key Findings

### Statistical Results
- **Mean improvement**: 4.28 points (95% CI: 2.86 to 5.71)
- **t-statistic**: 6.30 (df = 19)
- **p-value**: < 0.001 (highly significant)
- **Effect size (Cohen's d)**: 1.41 (large effect)

### Descriptive Statistics
- **Before AI**: Mean = 72.21 (SD = 5.28)
- **After AI**: Mean = 76.49 (SD = 5.14)
- **Improvement**: Mean = 4.29 (SD = 3.04)

### Student Outcomes
- 19 out of 20 students (95%) showed improvement
- 1 student showed a slight decline (-2.9 points)
- 0 students showed no change

## Data Files Generated
1. `writing_scores_data.csv` - Raw dataset with all student scores
2. `simple_paired_ttest.py` - Analysis script without external dependencies
3. `paired_ttest_analysis.py` - Full analysis script with visualization (requires numpy, pandas, matplotlib)
4. `create_text_visualization.py` - Text-based visualization generator

## Interpretation

The analysis provides strong evidence that AI tool usage leads to meaningful improvement in writing scores:

1. **Statistical Significance**: The p-value < 0.001 indicates that the observed improvement is highly unlikely to have occurred by chance.

2. **Practical Significance**: The Cohen's d of 1.41 represents a large effect size, indicating that the improvement is not only statistically significant but also practically meaningful.

3. **Consistency**: The improvement was consistent across most students, with 95% showing gains.

4. **Magnitude**: The average improvement of 4.28 points represents approximately 6% increase in scores, which could translate to a letter grade improvement for many students.

## Recommendations

Based on these findings:
1. The AI tools appear to be effective in improving writing performance
2. Implementation should continue with ongoing monitoring
3. Investigation into why one student showed decline may provide insights for optimization
4. Consider examining which aspects of writing (grammar, structure, clarity) show the most improvement

## Technical Notes

- The paired t-test was appropriate for this analysis as it accounts for the within-subject design
- Assumptions of normality were reasonable given the sample size and distribution of differences
- The large effect size suggests the intervention has substantial practical impact beyond statistical significance