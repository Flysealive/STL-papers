# AI/ML in Interventional Cardiology Literature Matrix (2019-2024)

## Literature Matrix

| Paper Title | Authors | Year | ML Methods | Performance Metrics | Clinical Validation | Code Availability | Key Contributions |
|-------------|---------|------|------------|-------------------|-------------------|------------------|-------------------|
| **Catheter Navigation & Assistance** |
| Automating Catheterization Labs with Real-Time Perception | Fan Yang, Benjamin Planche, Meng Zheng, Cheng Chen, Terrence Chen, Ziyan Wu | 2024 | Visual perception system (AutoCBCT) for C-arm CBCT imaging | Not specified | Successfully deployed in lab and clinical settings | Not mentioned | Eliminates manual operations, improves workflow efficiency |
| Auxiliary Input in Training: Incorporating Catheter Features into Deep Learning Models | Not specified | 2024 | Deep learning with catheter feature incorporation | Not specified | Not mentioned | Not mentioned | ECG-Free Dynamic Coronary Roadmapping, real-time navigation without repeated contrast |
| Autonomous Catheterization with Open-source Simulator | Tudor Jianu, Baoru Huang, Tuan Vo, et al. | 2024 | CathSim simulator with multimodal expert navigation network | Not specified | Not mentioned | https://github.com/airvlab/cathsim | First open-source simulator for endovascular intervention |
| **Point Cloud Processing** |
| Multi-objective Point Cloud Autoencoders for MI Prediction | Marcel Beetz, Abhirup Banerjee, Vicente Grau | 2023 | Geometric deep learning with 3D point cloud representations | AUC outperformed ML benchmarks by 19% | UK Biobank dataset validation | Not mentioned | Novel geometric approach for MI prediction |
| Geometry-based Cascaded Neural Network for Coronary Artery Segmentation | Not specified | 2023 | Cascaded segmentation with geometric deformation networks | Dice: 0.778 (CCA-200), 0.895 (ASOCA) | Tested on CCA-200 and ASOCA datasets | Not mentioned | Vascular tree vectorization capability |
| FFR Estimation Using Point Clouds | Not specified | 2024 | Hybrid neural network with PointNet++ adaptations | Not specified | Not mentioned | Not mentioned | Virtual FFR estimation from vessel geometry |
| **Predictive Models** |
| Catheter-Related Thrombosis Prediction | Not specified | 2024 | RandomForest, ExtraTreesEntr, WeightedEnsemble, CatBoost | AUCs: 0.85-0.89 | 3,337 breast cancer patients with CVCs | Not mentioned | High-accuracy thrombosis prediction |
| Catheter-Induced Dissection Prediction | Not specified | 2022 | Logistic regression, Decision Tree, Random Forest, Naive Bayes, K-NN, XGBoost | Not specified | 124 dissection cases from 84,223 procedures | Not mentioned | Identified key predictors: Guiding catheter (OR 7.49), small/stenotic ostium (OR 5.53) |
| PICC Line Detection System | Not specified | 2021 | Cascading segmentation AI with fully convolutional neural networks | Mean absolute distance: 3.10 mm | Not specified | Not mentioned | Accurate PICC line placement detection |

## Technology Summary

### Key ML/AI Architectures:
- **PointNet++ adaptations** - For processing vascular structures as 3D point clouds
- **Vision Transformers (ViT)** - For catheter pose estimation
- **Multimodal neural networks** - For navigation combining multiple data sources
- **Cascading CNNs** - For progressive segmentation tasks
- **Ensemble methods** - For robust risk prediction (RandomForest, CatBoost, XGBoost)

### Performance Benchmarks:
- **Segmentation**: Dice scores ranging from 0.778 to 0.895
- **Prediction**: AUCs ranging from 0.85 to 0.89
- **Detection**: Positioning accuracy within 3.10 mm
- **MI Prediction**: 19% improvement over traditional ML benchmarks

## Research Gaps Identified

### 1. **Limited Code Availability**
- Only 1 out of 10 papers provides public code repository (CathSim)
- Reproducibility challenges for most studies

### 2. **Transradial Approach Gap**
- No dedicated ML models for transradial complication prediction
- RAO rates documented (1.28% distal vs 4.76% proximal) but no predictive models

### 3. **Clinical Validation Limitations**
- Most models validated retrospectively
- Only AutoCBCT reported actual clinical deployment
- Limited prospective validation studies

### 4. **Real-time Performance Metrics**
- Few papers report computational efficiency/speed
- Critical for interventional applications but often missing

### 5. **Multimodal Integration**
- Limited studies combining imaging, hemodynamic, and clinical data
- Opportunity for more comprehensive models

## Future Research Directions

### 1. **Clinical Translation**
- Focus on prospective validation studies
- Real-world deployment and outcome tracking
- Regulatory pathway development for AI tools

### 2. **Open Science Initiatives**
- Develop more open-source tools following CathSim example
- Create standardized datasets for benchmarking
- Establish common evaluation protocols

### 3. **Specific Application Areas**
- **Transradial complications**: Develop dedicated prediction models
- **Real-time guidance**: Improve latency for intraoperative use
- **Personalized risk assessment**: Patient-specific models

### 4. **Technical Innovations**
- **Federated learning**: For multi-center collaboration
- **Explainable AI**: Critical for clinical acceptance
- **Edge computing**: For real-time processing in cath labs

### 5. **Integration Challenges**
- **Workflow integration**: Seamless incorporation into existing systems
- **Multimodal fusion**: Combining angiography, IVUS, OCT, and clinical data
- **Standardization**: Common data formats and APIs

### 6. **Emerging Technologies**
- **AR/VR integration**: For pre-procedural planning and training
- **Robot-assisted PCI**: AI navigation for robotic systems
- **Digital twins**: Patient-specific procedural simulation

## Key Observations

1. **Maturity Gradient**: Point cloud processing and predictive models show more mature implementations compared to real-time navigation systems

2. **Clinical Gap**: Strong technical performance but limited clinical deployment evidence

3. **Data Availability**: Major barrier to reproducibility and advancement

4. **Interdisciplinary Nature**: Success requires collaboration between ML engineers, interventional cardiologists, and medical physicists

5. **Safety Considerations**: Need for fail-safe mechanisms and clinician override capabilities in autonomous systems

## Recommendations for Future Studies

1. **Standardize Reporting**: Include computational requirements, real-time performance, and clinical integration details
2. **Prioritize Open Science**: Share code, data (when possible), and detailed methodologies
3. **Focus on Clinical Outcomes**: Move beyond technical metrics to patient-centered outcomes
4. **Address Regulatory Requirements**: Consider FDA/CE approval pathways early in development
5. **Develop Validation Frameworks**: Establish standards for testing AI systems in interventional cardiology