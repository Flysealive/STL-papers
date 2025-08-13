# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is an academic research project focused on AI/ML applications in interventional cardiology, specifically examining catheter exchange prediction using point cloud deep learning approaches. The project follows a structured research workflow with comprehensive literature reviews, statistical analyses, and manuscript preparation.

## Development Commands

### Python Dependencies
The project requires Python 3.8+ with the following key packages:
- numpy, pandas, scipy, statsmodels
- matplotlib, seaborn  
- scikit-learn
- lifelines (for survival analysis)
- pingouin (optional, for advanced statistics)
- forestplot (for meta-analysis visualizations)

### Running Statistical Analyses
```bash
# Run paired t-test analysis
python 07_Statistical_Analysis/paired_ttest_analysis.py

# Run simple paired t-test
python 07_Statistical_Analysis/simple_paired_ttest.py

# Create text visualizations
python 07_Statistical_Analysis/create_text_visualization.py
```

### Using Core Tools
```bash
# Citation management
python 06_References/citation_manager.py

# Medical statistics toolkit (import as module)
python -c "from medical_stats_toolkit import *"
```

## Architecture and Key Components

### Research Structure
The project follows a standard academic research workflow with numbered directories:
- **01_Literature_Review**: Systematic reviews, literature matrices, and research summaries focusing on AI/ML in interventional cardiology
- **04_Manuscripts**: Draft papers using IMRAD format templates
- **06_References**: Citation management system supporting APA, Vancouver, MLA, Chicago, and IEEE styles
- **07_Statistical_Analysis**: Comprehensive medical statistics toolkit with hypothesis testing, survival analysis, and meta-analysis capabilities
- **10_Project_Management**: Research protocols and systematic review checklists (PRISMA 2020)

### Key Python Modules

**medical_stats_toolkit.py** (07_Statistical_Analysis/)
- Comprehensive statistical framework for medical research
- Classes: DescriptiveStatistics, HypothesisTesting, EffectSizeCalculator, SurvivalAnalysis, MetaAnalysis
- Includes power analysis, multiple comparisons correction, and ML evaluation metrics
- Requires lifelines for survival analysis, pingouin for advanced tests (optional)

**citation_manager.py** (06_References/)
- CitationManager class for reference management
- Format conversion between citation styles
- DOI/URL validation and duplicate detection
- Import/export from CSV and JSON

### Research Focus
Current research investigates predicting catheter exchange necessity in left transradial coronary angiography using point cloud deep learning methodologies. Literature reviews cover 2019-2024 publications on AI/ML in interventional cardiology.

## Important Notes
- Statistical analyses should use the medical_stats_toolkit for consistency
- Citations should follow Vancouver style for medical journals unless specified otherwise
- Jupyter notebooks (statistical_analysis_template.ipynb) available for interactive analysis
- No build/test scripts currently configured - analyses run directly as Python scripts

## Recent Work and Context (2025-08-13)

### Manuscript Update - ML Comparison Study
Recently updated `04_Manuscripts/complete_scientific_paper.md` with new results from the subclavian-artery-pointnet GitHub repository. Key findings:

**Performance Results:**
- Random Forest: 82.98% ± 3.91% (BEST)
- Gradient Boosting: 82.98% ± 6.12% (TIED)
- Hybrid Multi-Modal DL: 79.77% ± 4.03%
- XGBoost: 77.60% ± 4.28%

**Key Insights:**
- Traditional ML outperforms deep learning with small datasets (n=95)
- Random Forest offers best stability and <1 second training time
- Deep learning expected to excel with 500+ samples
- Anatomical measurements contribute 23% feature importance

**Implementation Strategy:**
- n < 100: Use Random Forest with 51 geometric features
- n = 100-500: Ensemble traditional ML methods
- n > 500: Transition to deep learning approaches

### GitHub Integration
- Repository: https://github.com/Flysealive/subclavian-artery-pointnet
- Main manuscript: `04_Manuscripts/complete_scientific_paper.md`
- Updated to reflect comparative ML approach rather than single deep learning focus
- Staged implementation roadmap based on data availability

### Next Steps
- External validation of Random Forest model
- Web-based calculator development for clinical deployment
- Multi-center data collection to reach n=500 for deep learning transition
- Consider transfer learning and synthetic data augmentation