# Large Language Models in Academic Writing: Recent Research Summary (2023-2025)

## Executive Summary

This document summarizes recent research papers on the applications of large language models (LLMs) in academic writing from 2023-2025, with a focus on methodology improvements and evaluation metrics. The literature reveals rapid adoption of LLMs in scientific writing, significant methodological advances, and evolving evaluation frameworks.

## Key Findings

### 1. Widespread Adoption and Impact

- **At least 13.5% of 2024 biomedical abstracts** were processed with LLMs, with some subcorpora reaching 40% (Kobak et al., 2024)
- **Computer science papers show the largest growth** at up to 17.5% LLM usage (2024)
- **35% of arXiv computer science abstracts** estimated to be ChatGPT-revised (May 2024)
- **6.5%-16.9% of peer reviews** at major AI conferences show substantial LLM modification (ICLR 2024, NeurIPS 2023)

### 2. Major Research Papers

#### Comprehensive Surveys
1. **"A Survey on Evaluation of Large Language Models"** (arXiv:2307.03109, Dec 2023)
   - Examines LLMs from three key dimensions
   - Focuses on evaluation at task and societal levels

2. **"Evaluating Large Language Models: A Comprehensive Survey"** (arXiv:2310.19736, Nov 2023)
   - Highlights risks: private data leaks, harmful content generation
   - Discusses automatic evaluation metrics (F1, Exact Match, Perplexity)

3. **"A Systematic Survey and Critical Review on Evaluating LLMs"** (arXiv:2407.04069v1, July 2024)
   - Challenges: reproducibility, reliability, robustness
   - Emphasizes human evaluation for qualitative assessments

#### 2025 Developments
1. **"Robustness in Large Language Models"** (arXiv:2505.18658v1, May 2025)
   - Addresses covariate shift and concept shift challenges
   - Measures stability when prompts are rephrased

2. **"Large language models for automated scholarly paper review"** (arXiv:2501.10326v2, June 2025)
   - Examines LLMs in automated scholarly paper review (ASPR)
   - Discusses evolving influence on scholarly evaluation

3. **"LLM Penetration in Scholarly Writing and Peer Review"** (arXiv:2502.11193v1, Feb 2025)
   - Shows increasing penetration rates starting in 2023
   - Higher rates in abstracts than in reviews

### 3. Methodology Improvements

#### Detection and Benchmarking
- **GPABench2**: 2.8 million comparative samples for detectability studies
- Detection challenges due to human-like output and stochastic word choice
- Existing detection tools show modest to poor performance

#### Advanced Prompting Techniques
- Zero-shot Chain-of-Thought Prompting
- Automatic Prompt Engineer (APE)
- Self-critique Prompting
- Few-shot and Least-to-Most Prompting

#### Specialized Scientific LLMs
- **SciLitLLM**: 3.6% improvement on SciAssess, 10.1% on SciRIFF
- Outperforms larger models (70B parameters) on certain benchmarks
- Two development strategies:
  1. Supervised fine-tuning with scientific instructions
  2. Pre-training with scientific corpora

### 4. Evaluation Metrics and Frameworks

#### Traditional Metrics
- **BLEU**: Precision-based comparison to reference texts
- **ROUGE**: Recall-oriented evaluation for gisting
- **Perplexity**: Language model quality measure

#### Modern LLM-Based Metrics
- **LLM-as-a-Judge**: Using strong LLMs to evaluate other LLM outputs
- **G-Eval**: Framework for task-specific metrics with better human alignment
- **Multi-dimensional assessment**: Evaluating multiple quality aspects simultaneously

#### Academic Writing Specific Criteria
- Factual accuracy and faithfulness
- Coherence and logical flow
- Academic vocabulary usage
- Citation accuracy
- Methodological soundness

### 5. Vocabulary and Style Changes

Tracking LLM-induced vocabulary changes reveals specific words with excess usage in 2024:
- "delves" (r = 28.0)
- "underscores" (r = 13.8)
- "showcasing" (r = 10.7)
- Common words: "potential" (δ = 0.052), "findings" (δ = 0.041), "crucial" (δ = 0.037)

### 6. Applications and Tools

#### Literature Review Automation
- **AutoSurvey**: RAG-based system for retrieving latest papers
- Multi-LLM-as-judge for evaluating citation and content quality

#### Writing Assistance
- Equation formatting
- Spelling and grammar correction
- Rephrasing complex ideas
- Text reformatting
- Flow and readability improvement

### 7. Challenges and Limitations

#### Reproducibility Issues
- Missing model version documentation
- Different dataset subsets used across studies
- Lack of sampling strategy documentation

#### Quality Concerns
- Superficial comments in LLM-generated reviews
- Lack of criticism or novelty assessment
- Potential for output homogenization
- Risk of reducing feedback variation

#### Ethical Considerations
- Challenges to research integrity
- Need for disclosure policies
- Impact on peer review quality
- Concerns about academic authenticity

### 8. Future Directions

1. **Hybrid Human-AI Evaluation Systems**: Combining automation with human oversight
2. **Domain-Specific Quality Indicators**: Developing specialized metrics for different fields
3. **Interpretability and Explainability**: Making evaluation results more transparent
4. **Quality Filtering**: Developing better classifiers for low-quality text
5. **Standardization**: Creating consistent evaluation frameworks across disciplines

## Conclusions

The research from 2023-2025 demonstrates that LLMs have fundamentally transformed academic writing methodologies. While adoption is widespread and growing rapidly, significant challenges remain in detection, quality assurance, and maintaining academic integrity. The field is moving toward more sophisticated evaluation frameworks that combine automated metrics with human judgment, emphasizing the need for domain-specific approaches and transparent, reproducible methods.

## Key Recommendations for Researchers

1. Use specialized scientific LLMs when available (e.g., SciLitLLM)
2. Implement multi-dimensional evaluation approaches
3. Combine automated tools with human oversight
4. Document LLM usage transparently
5. Consider field-specific evaluation criteria
6. Stay updated on detection methods and ethical guidelines