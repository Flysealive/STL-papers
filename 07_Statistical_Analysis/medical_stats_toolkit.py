"""
Medical Statistics Toolkit
=========================

A comprehensive statistical analysis framework for medical and scientific research.
This toolkit provides functions and classes for descriptive statistics, hypothesis testing,
effect size calculations, survival analysis, meta-analysis, and medical research visualizations.

Author: Medical Statistics Toolkit
Date: August 2025
Version: 1.0

Requirements:
    numpy>=1.21.0
    pandas>=1.3.0
    scipy>=1.7.0
    matplotlib>=3.4.0
    seaborn>=0.11.0
    statsmodels>=0.12.0
    lifelines>=0.27.0
    scikit-learn>=1.0.0
    pingouin>=0.5.0
    forestplot>=0.3.0
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2_contingency, fisher_exact
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report
from sklearn.metrics import precision_recall_curve, average_precision_score
import statsmodels.api as sm
import statsmodels.stats.power as smp
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from statsmodels.stats.multitest import multipletests
import warnings
warnings.filterwarnings('ignore')

# Optional dependencies with graceful handling
try:
    from lifelines import KaplanMeierFitter, CoxPHFitter
    from lifelines.statistics import logrank_test, multivariate_logrank_test
    LIFELINES_AVAILABLE = True
except ImportError:
    LIFELINES_AVAILABLE = False
    print("Warning: lifelines not available. Survival analysis functions will be limited.")

try:
    import pingouin as pg
    PINGOUIN_AVAILABLE = True
except ImportError:
    PINGOUIN_AVAILABLE = False
    print("Warning: pingouin not available. Some advanced statistical tests will be limited.")


class DescriptiveStatistics:
    """
    Class for calculating descriptive statistics with confidence intervals.
    Designed for medical research reporting standards.
    """
    
    @staticmethod
    def summary_statistics(data, confidence_level=0.95):
        """
        Calculate comprehensive descriptive statistics.
        
        Parameters:
        -----------
        data : array-like
            Numeric data
        confidence_level : float
            Confidence level for intervals (default: 0.95)
            
        Returns:
        --------
        dict : Dictionary with statistics
        """
        data = np.array(data)
        data_clean = data[~np.isnan(data)]
        n = len(data_clean)
        
        if n == 0:
            return {"error": "No valid data points"}
        
        mean = np.mean(data_clean)
        std = np.std(data_clean, ddof=1)
        sem = std / np.sqrt(n)
        
        # Confidence interval for mean
        alpha = 1 - confidence_level
        t_critical = stats.t.ppf(1 - alpha/2, n-1)
        ci_lower = mean - t_critical * sem
        ci_upper = mean + t_critical * sem
        
        # Additional statistics
        median = np.median(data_clean)
        q1, q3 = np.percentile(data_clean, [25, 75])
        iqr = q3 - q1
        
        # Test for normality
        if n >= 8:
            shapiro_stat, shapiro_p = stats.shapiro(data_clean)
        else:
            shapiro_stat, shapiro_p = np.nan, np.nan
            
        return {
            'n': n,
            'missing': len(data) - n,
            'mean': mean,
            'std': std,
            'sem': sem,
            'median': median,
            'q1': q1,
            'q3': q3,
            'iqr': iqr,
            'min': np.min(data_clean),
            'max': np.max(data_clean),
            'range': np.max(data_clean) - np.min(data_clean),
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'confidence_level': confidence_level,
            'shapiro_stat': shapiro_stat,
            'shapiro_p': shapiro_p,
            'normal_distribution': shapiro_p > 0.05 if not np.isnan(shapiro_p) else None
        }
    
    @staticmethod
    def categorical_summary(data, sort_by_freq=True):
        """
        Calculate summary statistics for categorical data.
        
        Parameters:
        -----------
        data : array-like
            Categorical data
        sort_by_freq : bool
            Sort by frequency (default: True)
            
        Returns:
        --------
        pandas.DataFrame : Summary with counts, percentages, and confidence intervals
        """
        data = pd.Series(data).dropna()
        n_total = len(data)
        
        if n_total == 0:
            return pd.DataFrame()
        
        counts = data.value_counts(sort=sort_by_freq)
        percentages = (counts / n_total) * 100
        
        # Wilson confidence intervals for proportions
        results = []
        for category, count in counts.items():
            p = count / n_total
            ci_lower, ci_upper = proportion_confint(count, n_total, method='wilson')
            results.append({
                'category': category,
                'count': count,
                'percentage': percentages[category],
                'ci_lower': ci_lower * 100,
                'ci_upper': ci_upper * 100
            })
        
        return pd.DataFrame(results)


class HypothesisTests:
    """
    Class for various hypothesis tests commonly used in medical research.
    """
    
    @staticmethod
    def t_test_independent(group1, group2, equal_var=True, alternative='two-sided'):
        """
        Independent samples t-test.
        
        Parameters:
        -----------
        group1, group2 : array-like
            Data for the two groups
        equal_var : bool
            Assume equal variances (default: True)
        alternative : str
            Alternative hypothesis ('two-sided', 'less', 'greater')
            
        Returns:
        --------
        dict : Test results with interpretation
        """
        g1 = np.array(group1)[~np.isnan(group1)]
        g2 = np.array(group2)[~np.isnan(group2)]
        
        # Descriptive statistics
        desc1 = DescriptiveStatistics.summary_statistics(g1)
        desc2 = DescriptiveStatistics.summary_statistics(g2)
        
        # Levene's test for equal variances
        levene_stat, levene_p = stats.levene(g1, g2)
        
        # T-test
        if equal_var:
            t_stat, p_value = stats.ttest_ind(g1, g2, alternative=alternative)
        else:
            t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=False, alternative=alternative)
        
        # Degrees of freedom
        if equal_var:
            df = len(g1) + len(g2) - 2
        else:
            # Welch's degrees of freedom
            s1_sq, s2_sq = np.var(g1, ddof=1), np.var(g2, ddof=1)
            n1, n2 = len(g1), len(g2)
            df = (s1_sq/n1 + s2_sq/n2)**2 / ((s1_sq/n1)**2/(n1-1) + (s2_sq/n2)**2/(n2-1))
        
        # Effect size (Cohen's d)
        cohen_d = EffectSizes.cohens_d(g1, g2)
        
        return {
            'test': 'Independent samples t-test',
            't_statistic': t_stat,
            'p_value': p_value,
            'degrees_of_freedom': df,
            'alternative': alternative,
            'equal_variances_assumed': equal_var,
            'levene_statistic': levene_stat,
            'levene_p_value': levene_p,
            'equal_variances_supported': levene_p > 0.05,
            'cohens_d': cohen_d,
            'group1_stats': desc1,
            'group2_stats': desc2,
            'significant': p_value < 0.05,
            'interpretation': HypothesisTests._interpret_t_test(t_stat, p_value, cohen_d)
        }
    
    @staticmethod
    def t_test_paired(before, after, alternative='two-sided'):
        """
        Paired samples t-test.
        
        Parameters:
        -----------
        before, after : array-like
            Paired observations
        alternative : str
            Alternative hypothesis ('two-sided', 'less', 'greater')
            
        Returns:
        --------
        dict : Test results with interpretation
        """
        before = np.array(before)
        after = np.array(after)
        
        # Remove pairs with missing data
        mask = ~(np.isnan(before) | np.isnan(after))
        before_clean = before[mask]
        after_clean = after[mask]
        
        differences = after_clean - before_clean
        
        # Descriptive statistics
        desc_before = DescriptiveStatistics.summary_statistics(before_clean)
        desc_after = DescriptiveStatistics.summary_statistics(after_clean)
        desc_diff = DescriptiveStatistics.summary_statistics(differences)
        
        # T-test
        t_stat, p_value = stats.ttest_rel(before_clean, after_clean, alternative=alternative)
        df = len(differences) - 1
        
        # Effect size
        cohen_d = np.mean(differences) / np.std(differences, ddof=1)
        
        return {
            'test': 'Paired samples t-test',
            't_statistic': t_stat,
            'p_value': p_value,
            'degrees_of_freedom': df,
            'n_pairs': len(differences),
            'alternative': alternative,
            'cohens_d': cohen_d,
            'before_stats': desc_before,
            'after_stats': desc_after,
            'difference_stats': desc_diff,
            'significant': p_value < 0.05,
            'interpretation': HypothesisTests._interpret_paired_t_test(t_stat, p_value, cohen_d, np.mean(differences))
        }
    
    @staticmethod
    def mann_whitney_u(group1, group2, alternative='two-sided'):
        """
        Mann-Whitney U test (Wilcoxon rank-sum test).
        
        Parameters:
        -----------
        group1, group2 : array-like
            Data for the two groups
        alternative : str
            Alternative hypothesis ('two-sided', 'less', 'greater')
            
        Returns:
        --------
        dict : Test results
        """
        g1 = np.array(group1)[~np.isnan(group1)]
        g2 = np.array(group2)[~np.isnan(group2)]
        
        statistic, p_value = stats.mannwhitneyu(g1, g2, alternative=alternative)
        
        # Effect size (r = Z / sqrt(N))
        n1, n2 = len(g1), len(g2)
        n_total = n1 + n2
        z_score = stats.norm.ppf(1 - p_value/2) if alternative == 'two-sided' else stats.norm.ppf(1 - p_value)
        effect_size_r = abs(z_score) / np.sqrt(n_total)
        
        return {
            'test': 'Mann-Whitney U test',
            'u_statistic': statistic,
            'p_value': p_value,
            'alternative': alternative,
            'n_group1': n1,
            'n_group2': n2,
            'effect_size_r': effect_size_r,
            'significant': p_value < 0.05,
            'median_group1': np.median(g1),
            'median_group2': np.median(g2)
        }
    
    @staticmethod
    def chi_square_test(contingency_table):
        """
        Chi-square test of independence.
        
        Parameters:
        -----------
        contingency_table : array-like
            2D contingency table
            
        Returns:
        --------
        dict : Test results including effect sizes
        """
        table = np.array(contingency_table)
        chi2_stat, p_value, dof, expected = chi2_contingency(table)
        
        n = np.sum(table)
        
        # Effect sizes
        cramers_v = np.sqrt(chi2_stat / (n * (min(table.shape) - 1)))
        phi = np.sqrt(chi2_stat / n) if table.shape == (2, 2) else None
        
        # Fisher's exact test for 2x2 tables
        if table.shape == (2, 2):
            odds_ratio, fisher_p = fisher_exact(table)
        else:
            odds_ratio, fisher_p = None, None
        
        return {
            'test': 'Chi-square test of independence',
            'chi2_statistic': chi2_stat,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'cramers_v': cramers_v,
            'phi': phi,
            'odds_ratio': odds_ratio,
            'fisher_exact_p': fisher_p,
            'expected_frequencies': expected,
            'significant': p_value < 0.05,
            'minimum_expected': np.min(expected),
            'assumption_met': np.min(expected) >= 5
        }
    
    @staticmethod
    def _interpret_t_test(t_stat, p_value, cohen_d):
        """Helper function to interpret t-test results."""
        interpretation = []
        
        if p_value < 0.001:
            interpretation.append("Highly significant difference (p < 0.001)")
        elif p_value < 0.01:
            interpretation.append("Very significant difference (p < 0.01)")
        elif p_value < 0.05:
            interpretation.append("Significant difference (p < 0.05)")
        else:
            interpretation.append("No significant difference (p >= 0.05)")
        
        # Effect size interpretation
        abs_d = abs(cohen_d)
        if abs_d < 0.2:
            interpretation.append("Negligible effect size")
        elif abs_d < 0.5:
            interpretation.append("Small effect size")
        elif abs_d < 0.8:
            interpretation.append("Medium effect size")
        else:
            interpretation.append("Large effect size")
        
        return "; ".join(interpretation)
    
    @staticmethod
    def _interpret_paired_t_test(t_stat, p_value, cohen_d, mean_diff):
        """Helper function to interpret paired t-test results."""
        interpretation = []
        
        if p_value < 0.001:
            interpretation.append("Highly significant change (p < 0.001)")
        elif p_value < 0.01:
            interpretation.append("Very significant change (p < 0.01)")
        elif p_value < 0.05:
            interpretation.append("Significant change (p < 0.05)")
        else:
            interpretation.append("No significant change (p >= 0.05)")
        
        if mean_diff > 0:
            interpretation.append("Increase from baseline")
        elif mean_diff < 0:
            interpretation.append("Decrease from baseline")
        else:
            interpretation.append("No change from baseline")
        
        return "; ".join(interpretation)


class EffectSizes:
    """
    Class for calculating various effect sizes commonly used in medical research.
    """
    
    @staticmethod
    def cohens_d(group1, group2, paired=False):
        """
        Calculate Cohen's d effect size.
        
        Parameters:
        -----------
        group1, group2 : array-like
            Data for comparison
        paired : bool
            Whether data is paired (default: False)
            
        Returns:
        --------
        float : Cohen's d effect size
        """
        g1 = np.array(group1)[~np.isnan(group1)]
        g2 = np.array(group2)[~np.isnan(group2)]
        
        if paired:
            differences = g1 - g2
            return np.mean(differences) / np.std(differences, ddof=1)
        else:
            n1, n2 = len(g1), len(g2)
            s1, s2 = np.std(g1, ddof=1), np.std(g2, ddof=1)
            pooled_std = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
            return (np.mean(g1) - np.mean(g2)) / pooled_std
    
    @staticmethod
    def odds_ratio_ci(a, b, c, d, confidence_level=0.95):
        """
        Calculate odds ratio with confidence interval.
        
        Parameters:
        -----------
        a, b, c, d : int
            Cells of 2x2 contingency table:
            [a, b]
            [c, d]
        confidence_level : float
            Confidence level (default: 0.95)
            
        Returns:
        --------
        dict : Odds ratio and confidence interval
        """
        if a == 0 or b == 0 or c == 0 or d == 0:
            # Add continuity correction
            a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
        
        or_value = (a * d) / (b * c)
        log_or = np.log(or_value)
        se_log_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
        
        alpha = 1 - confidence_level
        z_critical = stats.norm.ppf(1 - alpha/2)
        
        ci_lower = np.exp(log_or - z_critical * se_log_or)
        ci_upper = np.exp(log_or + z_critical * se_log_or)
        
        return {
            'odds_ratio': or_value,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'log_or': log_or,
            'se_log_or': se_log_or
        }
    
    @staticmethod
    def relative_risk_ci(a, b, c, d, confidence_level=0.95):
        """
        Calculate relative risk with confidence interval.
        
        Parameters:
        -----------
        a, b, c, d : int
            Cells of 2x2 contingency table
        confidence_level : float
            Confidence level (default: 0.95)
            
        Returns:
        --------
        dict : Relative risk and confidence interval
        """
        risk1 = a / (a + b)
        risk2 = c / (c + d)
        rr = risk1 / risk2
        
        log_rr = np.log(rr)
        se_log_rr = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))
        
        alpha = 1 - confidence_level
        z_critical = stats.norm.ppf(1 - alpha/2)
        
        ci_lower = np.exp(log_rr - z_critical * se_log_rr)
        ci_upper = np.exp(log_rr + z_critical * se_log_rr)
        
        return {
            'relative_risk': rr,
            'risk1': risk1,
            'risk2': risk2,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper
        }


class PowerAnalysis:
    """
    Class for sample size and power calculations.
    """
    
    @staticmethod
    def power_t_test_independent(effect_size, n1, n2=None, alpha=0.05, alternative='two-sided'):
        """
        Power calculation for independent samples t-test.
        
        Parameters:
        -----------
        effect_size : float
            Cohen's d effect size
        n1 : int
            Sample size for group 1
        n2 : int
            Sample size for group 2 (default: same as n1)
        alpha : float
            Type I error rate (default: 0.05)
        alternative : str
            Alternative hypothesis ('two-sided', 'larger', 'smaller')
            
        Returns:
        --------
        float : Statistical power
        """
        if n2 is None:
            n2 = n1
        
        return smp.ttest_power(effect_size, n1, alpha, alternative=alternative, n2=n2)
    
    @staticmethod
    def sample_size_t_test_independent(effect_size, power=0.8, alpha=0.05, ratio=1, alternative='two-sided'):
        """
        Sample size calculation for independent samples t-test.
        
        Parameters:
        -----------
        effect_size : float
            Cohen's d effect size
        power : float
            Desired statistical power (default: 0.8)
        alpha : float
            Type I error rate (default: 0.05)
        ratio : float
            Ratio of sample sizes n2/n1 (default: 1)
        alternative : str
            Alternative hypothesis
            
        Returns:
        --------
        dict : Sample size calculations
        """
        n1 = smp.tt_ind_solve_power(effect_size, power=power, alpha=alpha, 
                                   ratio=ratio, alternative=alternative)
        n2 = n1 * ratio
        
        return {
            'n1': int(np.ceil(n1)),
            'n2': int(np.ceil(n2)),
            'total_n': int(np.ceil(n1 + n2)),
            'effect_size': effect_size,
            'power': power,
            'alpha': alpha,
            'ratio': ratio
        }
    
    @staticmethod
    def power_proportion_test(p1, p2, n1, n2=None, alpha=0.05, alternative='two-sided'):
        """
        Power calculation for comparing two proportions.
        
        Parameters:
        -----------
        p1, p2 : float
            Proportions to compare
        n1 : int
            Sample size for group 1
        n2 : int
            Sample size for group 2 (default: same as n1)
        alpha : float
            Type I error rate (default: 0.05)
            
        Returns:
        --------
        float : Statistical power
        """
        if n2 is None:
            n2 = n1
            
        return smp.zt_ind_solve_power(effect_size=None, nobs1=n1, alpha=alpha, 
                                     power=None, ratio=n2/n1, alternative=alternative,
                                     prop2=p2, prop1=p1)


class SurvivalAnalysis:
    """
    Class for survival analysis functions.
    Requires lifelines package.
    """
    
    @staticmethod
    def kaplan_meier_analysis(durations, event_observed, groups=None, alpha=0.05):
        """
        Kaplan-Meier survival analysis.
        
        Parameters:
        -----------
        durations : array-like
            Duration until event or censoring
        event_observed : array-like
            Whether event was observed (1) or censored (0)
        groups : array-like, optional
            Group labels for comparison
        alpha : float
            Significance level for confidence intervals
            
        Returns:
        --------
        dict : Survival analysis results
        """
        if not LIFELINES_AVAILABLE:
            return {"error": "lifelines package not available"}
        
        if groups is None:
            # Single group analysis
            kmf = KaplanMeierFitter(alpha=alpha)
            kmf.fit(durations, event_observed)
            
            return {
                'survival_function': kmf.survival_function_,
                'confidence_interval': kmf.confidence_interval_,
                'median_survival': kmf.median_survival_time_,
                'median_ci': kmf.confidence_interval_survival_times_,
                'event_table': kmf.event_table
            }
        else:
            # Group comparison
            results = {}
            unique_groups = np.unique(groups)
            
            for group in unique_groups:
                mask = groups == group
                kmf = KaplanMeierFitter(alpha=alpha, label=str(group))
                kmf.fit(durations[mask], event_observed[mask])
                
                results[group] = {
                    'survival_function': kmf.survival_function_,
                    'confidence_interval': kmf.confidence_interval_,
                    'median_survival': kmf.median_survival_time_,
                    'event_table': kmf.event_table
                }
            
            # Log-rank test
            if len(unique_groups) == 2:
                group1_mask = groups == unique_groups[0]
                group2_mask = groups == unique_groups[1]
                
                logrank_result = logrank_test(
                    durations[group1_mask], durations[group2_mask],
                    event_observed[group1_mask], event_observed[group2_mask]
                )
                
                results['logrank_test'] = {
                    'test_statistic': logrank_result.test_statistic,
                    'p_value': logrank_result.p_value,
                    'degrees_of_freedom': 1,
                    'significant': logrank_result.p_value < 0.05
                }
            
            return results
    
    @staticmethod
    def cox_regression(durations, event_observed, covariates_df, alpha=0.05):
        """
        Cox proportional hazards regression.
        
        Parameters:
        -----------
        durations : array-like
            Duration until event or censoring
        event_observed : array-like
            Whether event was observed (1) or censored (0)
        covariates_df : pandas.DataFrame
            Covariates for regression
        alpha : float
            Significance level
            
        Returns:
        --------
        dict : Cox regression results
        """
        if not LIFELINES_AVAILABLE:
            return {"error": "lifelines package not available"}
        
        # Prepare data
        data = covariates_df.copy()
        data['duration'] = durations
        data['event'] = event_observed
        
        # Fit Cox model
        cph = CoxPHFitter(alpha=alpha)
        cph.fit(data, duration_col='duration', event_col='event')
        
        return {
            'summary': cph.summary,
            'hazard_ratios': cph.hazard_ratios_,
            'confidence_intervals': cph.confidence_intervals_,
            'p_values': cph.summary['p'],
            'concordance_index': cph.concordance_index_,
            'log_likelihood': cph.log_likelihood_,
            'aic': cph.AIC_,
            'partial_aic': cph.AIC_partial_
        }


class MetaAnalysis:
    """
    Class for meta-analysis functions.
    """
    
    @staticmethod
    def fixed_effects_meta(effect_sizes, variances, study_names=None):
        """
        Fixed-effects meta-analysis.
        
        Parameters:
        -----------
        effect_sizes : array-like
            Effect sizes from individual studies
        variances : array-like
            Variances of effect sizes
        study_names : array-like, optional
            Names of studies
            
        Returns:
        --------
        dict : Meta-analysis results
        """
        es = np.array(effect_sizes)
        var = np.array(variances)
        weights = 1 / var
        
        # Pooled effect size
        pooled_es = np.sum(weights * es) / np.sum(weights)
        pooled_var = 1 / np.sum(weights)
        pooled_se = np.sqrt(pooled_var)
        
        # Confidence interval
        z_critical = stats.norm.ppf(0.975)
        ci_lower = pooled_es - z_critical * pooled_se
        ci_upper = pooled_es + z_critical * pooled_se
        
        # Test of overall effect
        z_score = pooled_es / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        # Heterogeneity
        q_stat = np.sum(weights * (es - pooled_es)**2)
        df = len(es) - 1
        q_p_value = 1 - stats.chi2.cdf(q_stat, df)
        i_squared = max(0, (q_stat - df) / q_stat * 100)
        
        return {
            'pooled_effect_size': pooled_es,
            'pooled_se': pooled_se,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'z_score': z_score,
            'p_value': p_value,
            'q_statistic': q_stat,
            'q_p_value': q_p_value,
            'i_squared': i_squared,
            'tau_squared': 0,  # Fixed effects assumes tau² = 0
            'weights': weights,
            'significant': p_value < 0.05,
            'heterogeneity': 'Low' if i_squared < 25 else 'Moderate' if i_squared < 75 else 'High'
        }
    
    @staticmethod
    def random_effects_meta(effect_sizes, variances, study_names=None, method='DL'):
        """
        Random-effects meta-analysis using DerSimonian-Laird method.
        
        Parameters:
        -----------
        effect_sizes : array-like
            Effect sizes from individual studies
        variances : array-like
            Variances of effect sizes
        study_names : array-like, optional
            Names of studies
        method : str
            Method for tau² estimation (default: 'DL')
            
        Returns:
        --------
        dict : Meta-analysis results
        """
        es = np.array(effect_sizes)
        var = np.array(variances)
        
        # First, calculate Q statistic using fixed effects
        weights_fe = 1 / var
        pooled_es_fe = np.sum(weights_fe * es) / np.sum(weights_fe)
        q_stat = np.sum(weights_fe * (es - pooled_es_fe)**2)
        df = len(es) - 1
        
        # Estimate tau²
        if method == 'DL':
            c = np.sum(weights_fe) - np.sum(weights_fe**2) / np.sum(weights_fe)
            tau_squared = max(0, (q_stat - df) / c)
        else:
            tau_squared = 0
        
        # Random effects weights
        weights_re = 1 / (var + tau_squared)
        
        # Pooled effect size
        pooled_es = np.sum(weights_re * es) / np.sum(weights_re)
        pooled_var = 1 / np.sum(weights_re)
        pooled_se = np.sqrt(pooled_var)
        
        # Confidence interval
        z_critical = stats.norm.ppf(0.975)
        ci_lower = pooled_es - z_critical * pooled_se
        ci_upper = pooled_es + z_critical * pooled_se
        
        # Test of overall effect
        z_score = pooled_es / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        # Heterogeneity statistics
        q_p_value = 1 - stats.chi2.cdf(q_stat, df)
        i_squared = max(0, (q_stat - df) / q_stat * 100)
        
        return {
            'pooled_effect_size': pooled_es,
            'pooled_se': pooled_se,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'z_score': z_score,
            'p_value': p_value,
            'q_statistic': q_stat,
            'q_p_value': q_p_value,
            'i_squared': i_squared,
            'tau_squared': tau_squared,
            'weights': weights_re,
            'significant': p_value < 0.05,
            'heterogeneity': 'Low' if i_squared < 25 else 'Moderate' if i_squared < 75 else 'High'
        }


class MLEvaluationMetrics:
    """
    Class for machine learning evaluation metrics commonly used in medical AI.
    """
    
    @staticmethod
    def binary_classification_metrics(y_true, y_pred, y_scores=None, pos_label=1):
        """
        Comprehensive binary classification metrics.
        
        Parameters:
        -----------
        y_true : array-like
            True binary labels
        y_pred : array-like
            Predicted binary labels
        y_scores : array-like, optional
            Prediction scores/probabilities
        pos_label : int or str
            Positive class label
            
        Returns:
        --------
        dict : Classification metrics
        """
        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[1-pos_label, pos_label]).ravel()
        
        # Basic metrics
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        ppv = tp / (tp + fp) if (tp + fp) > 0 else 0  # Precision/PPV
        npv = tn / (tn + fn) if (tn + fn) > 0 else 0
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        
        # F1 score
        f1 = 2 * (ppv * sensitivity) / (ppv + sensitivity) if (ppv + sensitivity) > 0 else 0
        
        # Likelihood ratios
        lr_positive = sensitivity / (1 - specificity) if specificity < 1 else np.inf
        lr_negative = (1 - sensitivity) / specificity if specificity > 0 else np.inf
        
        results = {
            'confusion_matrix': {'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn},
            'sensitivity_recall': sensitivity,
            'specificity': specificity,
            'precision_ppv': ppv,
            'npv': npv,
            'accuracy': accuracy,
            'f1_score': f1,
            'lr_positive': lr_positive,
            'lr_negative': lr_negative
        }
        
        # ROC and PR curves if scores provided
        if y_scores is not None:
            fpr, tpr, roc_thresholds = roc_curve(y_true, y_scores, pos_label=pos_label)
            auc_roc = auc(fpr, tpr)
            
            precision, recall, pr_thresholds = precision_recall_curve(y_true, y_scores, pos_label=pos_label)
            auc_pr = auc(recall, precision)
            
            results.update({
                'auc_roc': auc_roc,
                'auc_pr': auc_pr,
                'roc_curve': {'fpr': fpr, 'tpr': tpr, 'thresholds': roc_thresholds},
                'pr_curve': {'precision': precision, 'recall': recall, 'thresholds': pr_thresholds}
            })
        
        return results
    
    @staticmethod
    def diagnostic_test_evaluation(y_true, y_pred, prevalence=None):
        """
        Evaluation metrics for diagnostic tests.
        
        Parameters:
        -----------
        y_true : array-like
            True labels (1 for disease, 0 for no disease)
        y_pred : array-like
            Predicted labels
        prevalence : float, optional
            Disease prevalence in population
            
        Returns:
        --------
        dict : Diagnostic test metrics
        """
        metrics = MLEvaluationMetrics.binary_classification_metrics(y_true, y_pred)
        
        sensitivity = metrics['sensitivity_recall']
        specificity = metrics['specificity']
        
        # If prevalence provided, calculate predictive values for population
        if prevalence is not None:
            ppv_pop = (sensitivity * prevalence) / (sensitivity * prevalence + (1 - specificity) * (1 - prevalence))
            npv_pop = (specificity * (1 - prevalence)) / (specificity * (1 - prevalence) + (1 - sensitivity) * prevalence)
            
            metrics.update({
                'population_prevalence': prevalence,
                'ppv_population': ppv_pop,
                'npv_population': npv_pop
            })
        
        return metrics


class MedicalVisualizations:
    """
    Class for medical research visualizations.
    """
    
    @staticmethod
    def forest_plot(effect_sizes, variances, study_names, title="Forest Plot", 
                   effect_label="Effect Size", figsize=(10, 8)):
        """
        Create a forest plot for meta-analysis.
        
        Parameters:
        -----------
        effect_sizes : array-like
            Effect sizes from studies
        variances : array-like
            Variances of effect sizes
        study_names : array-like
            Names of studies
        title : str
            Plot title
        effect_label : str
            Label for effect size
        figsize : tuple
            Figure size
            
        Returns:
        --------
        matplotlib.figure.Figure : Forest plot
        """
        es = np.array(effect_sizes)
        var = np.array(variances)
        se = np.sqrt(var)
        
        # Calculate confidence intervals
        ci_lower = es - 1.96 * se
        ci_upper = es + 1.96 * se
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        y_pos = np.arange(len(study_names))
        
        # Plot individual studies
        ax.errorbar(es, y_pos, xerr=[es - ci_lower, ci_upper - es], 
                   fmt='s', markersize=8, capsize=5, capthick=2)
        
        # Plot pooled estimate (example using fixed effects)
        weights = 1 / var
        pooled_es = np.sum(weights * es) / np.sum(weights)
        pooled_se = np.sqrt(1 / np.sum(weights))
        pooled_ci_lower = pooled_es - 1.96 * pooled_se
        pooled_ci_upper = pooled_es + 1.96 * pooled_se
        
        ax.errorbar(pooled_es, len(study_names), xerr=[[pooled_es - pooled_ci_lower], [pooled_ci_upper - pooled_es]], 
                   fmt='D', markersize=12, capsize=5, capthick=3, color='red', label='Pooled')
        
        # Formatting
        ax.set_yticks(y_pos)
        ax.set_yticklabels(study_names)
        ax.set_xlabel(effect_label)
        ax.set_title(title)
        ax.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def kaplan_meier_plot(durations, event_observed, groups=None, confidence_intervals=True, 
                         title="Kaplan-Meier Survival Curves", figsize=(10, 6)):
        """
        Create Kaplan-Meier survival plot.
        
        Parameters:
        -----------
        durations : array-like
            Time to event or censoring
        event_observed : array-like
            Event indicator (1=event, 0=censored)
        groups : array-like, optional
            Group labels for comparison
        confidence_intervals : bool
            Whether to show confidence intervals
        title : str
            Plot title
        figsize : tuple
            Figure size
            
        Returns:
        --------
        matplotlib.figure.Figure : Kaplan-Meier plot
        """
        if not LIFELINES_AVAILABLE:
            print("Error: lifelines package required for Kaplan-Meier plots")
            return None
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if groups is None:
            # Single group
            kmf = KaplanMeierFitter()
            kmf.fit(durations, event_observed, label='Overall')
            kmf.plot_survival_function(ax=ax, show_censors=True, ci_show=confidence_intervals)
        else:
            # Multiple groups
            unique_groups = np.unique(groups)
            colors = plt.cm.Set1(np.linspace(0, 1, len(unique_groups)))
            
            for i, group in enumerate(unique_groups):
                mask = groups == group
                kmf = KaplanMeierFitter()
                kmf.fit(durations[mask], event_observed[mask], label=f'Group {group}')
                kmf.plot_survival_function(ax=ax, show_censors=True, ci_show=confidence_intervals, color=colors[i])
        
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.set_ylabel('Survival Probability')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def roc_curve_plot(y_true, y_scores, title="ROC Curve", figsize=(8, 8)):
        """
        Create ROC curve plot.
        
        Parameters:
        -----------
        y_true : array-like
            True binary labels
        y_scores : array-like
            Prediction scores
        title : str
            Plot title
        figsize : tuple
            Figure size
            
        Returns:
        --------
        matplotlib.figure.Figure : ROC curve plot
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        auc_score = auc(fpr, tpr)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {auc_score:.3f})')
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
        
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate (1 - Specificity)')
        ax.set_ylabel('True Positive Rate (Sensitivity)')
        ax.set_title(title)
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


class MultipleComparisons:
    """
    Class for handling multiple comparisons corrections.
    """
    
    @staticmethod
    def adjust_p_values(p_values, method='holm', alpha=0.05):
        """
        Adjust p-values for multiple comparisons.
        
        Parameters:
        -----------
        p_values : array-like
            Unadjusted p-values
        method : str
            Correction method ('holm', 'bonferroni', 'fdr_bh', 'fdr_by')
        alpha : float
            Family-wise error rate
            
        Returns:
        --------
        dict : Adjusted p-values and significance
        """
        p_vals = np.array(p_values)
        
        reject, p_adjusted, alpha_sidak, alpha_bonf = multipletests(
            p_vals, alpha=alpha, method=method
        )
        
        return {
            'original_p_values': p_vals,
            'adjusted_p_values': p_adjusted,
            'significant_after_correction': reject,
            'method': method,
            'alpha': alpha,
            'n_comparisons': len(p_vals),
            'n_significant_original': np.sum(p_vals < alpha),
            'n_significant_adjusted': np.sum(reject)
        }


# Utility functions
def load_data(file_path, **kwargs):
    """
    Load data from various file formats.
    
    Parameters:
    -----------
    file_path : str
        Path to data file
    **kwargs : dict
        Additional arguments for pandas readers
        
    Returns:
    --------
    pandas.DataFrame : Loaded data
    """
    file_extension = file_path.lower().split('.')[-1]
    
    if file_extension == 'csv':
        return pd.read_csv(file_path, **kwargs)
    elif file_extension in ['xlsx', 'xls']:
        return pd.read_excel(file_path, **kwargs)
    elif file_extension == 'json':
        return pd.read_json(file_path, **kwargs)
    elif file_extension == 'sav':
        try:
            import pyreadstat
            return pd.read_spss(file_path, **kwargs)
        except ImportError:
            raise ImportError("pyreadstat required for SPSS files")
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def generate_sample_data(n_samples=100, seed=42):
    """
    Generate sample medical data for testing.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples
    seed : int
        Random seed
        
    Returns:
    --------
    pandas.DataFrame : Sample data
    """
    np.random.seed(seed)
    
    # Generate correlated variables
    age = np.random.normal(65, 15, n_samples)
    age = np.clip(age, 18, 100)
    
    # Binary variables
    gender = np.random.binomial(1, 0.6, n_samples)  # 1 = female
    diabetes = np.random.binomial(1, 0.3 + 0.01 * (age - 65), n_samples)
    
    # Treatment assignment
    treatment = np.random.binomial(1, 0.5, n_samples)
    
    # Outcome variable influenced by predictors
    outcome_prob = 0.3 + 0.2 * treatment - 0.01 * age + 0.15 * diabetes
    outcome_prob = np.clip(outcome_prob, 0.01, 0.99)
    outcome = np.random.binomial(1, outcome_prob, n_samples)
    
    # Continuous outcome
    continuous_outcome = 120 + 5 * treatment - 0.5 * age + 10 * diabetes + np.random.normal(0, 10, n_samples)
    
    # Survival data
    hazard = np.exp(-2 + 0.5 * treatment + 0.02 * age + 0.3 * diabetes)
    survival_time = np.random.exponential(1/hazard, n_samples)
    censoring_time = np.random.exponential(1/0.1, n_samples)  # Random censoring
    
    observed_time = np.minimum(survival_time, censoring_time)
    event_observed = (survival_time <= censoring_time).astype(int)
    
    return pd.DataFrame({
        'patient_id': range(1, n_samples + 1),
        'age': age,
        'gender': gender,
        'diabetes': diabetes,
        'treatment': treatment,
        'outcome': outcome,
        'continuous_outcome': continuous_outcome,
        'survival_time': observed_time,
        'event_observed': event_observed
    })


if __name__ == "__main__":
    # Example usage and testing
    print("Medical Statistics Toolkit - Example Usage")
    print("=" * 50)
    
    # Generate sample data
    data = generate_sample_data(n_samples=200)
    print(f"Generated sample data with {len(data)} patients")
    
    # Example 1: Descriptive statistics
    print("\n1. Descriptive Statistics")
    print("-" * 30)
    age_stats = DescriptiveStatistics.summary_statistics(data['age'])
    print(f"Age: Mean = {age_stats['mean']:.1f} ± {age_stats['std']:.1f}")
    print(f"95% CI: [{age_stats['ci_lower']:.1f}, {age_stats['ci_upper']:.1f}]")
    
    # Example 2: T-test
    print("\n2. Independent Samples T-test")
    print("-" * 30)
    treatment_group = data[data['treatment'] == 1]['continuous_outcome']
    control_group = data[data['treatment'] == 0]['continuous_outcome']
    
    t_result = HypothesisTests.t_test_independent(treatment_group, control_group)
    print(f"T-statistic: {t_result['t_statistic']:.3f}")
    print(f"P-value: {t_result['p_value']:.3f}")
    print(f"Cohen's d: {t_result['cohens_d']:.3f}")
    
    # Example 3: Power analysis
    print("\n3. Power Analysis")
    print("-" * 30)
    power = PowerAnalysis.power_t_test_independent(effect_size=0.5, n1=50, n2=50)
    print(f"Power for Cohen's d = 0.5 with n=50 per group: {power:.3f}")
    
    sample_size = PowerAnalysis.sample_size_t_test_independent(effect_size=0.5, power=0.8)
    print(f"Required sample size for 80% power: {sample_size['total_n']} total")
    
    print("\nToolkit loaded successfully! Ready for medical statistical analysis.")