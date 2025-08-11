# Systematic Literature Review: Deep Learning Models for Medical Vessel Analysis Using Point Cloud Representations

## Executive Summary

This systematic literature review examines deep learning models for medical vessel analysis using point cloud representations, focusing on architectures including PointNet/PointNet++, Dynamic Graph CNN (DGCNN), PointConv, and Graph Neural Networks (GNNs). The review covers papers from 2017 onwards, synthesizing findings from multiple databases including PubMed, arXiv, and academic search engines.

## 1. PointNet and PointNet++ Applications in Medical Vessel Analysis

### Seminal Works
- **PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation** (Qi et al., 2017)
  - arXiv: https://arxiv.org/abs/1612.00593
  - GitHub: https://github.com/charlesq34/pointnet
  - Key contribution: First architecture to directly process unordered point clouds with permutation invariance

- **PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space** (Qi et al., 2017)
  - GitHub: https://github.com/charlesq34/pointnet2
  - Key contribution: Hierarchical feature learning with local context awareness

### Medical Applications

#### Key Findings:
1. **Cervical Vertebrae Segmentation** (2021)
   - PubMed: https://pubmed.ncbi.nlm.nih.gov/33545639/
   - Achieved 96.15% accuracy using PointNet++
   - Demonstrated superior performance compared to CNN methods on CT scan datasets

2. **Medical Point Cloud Challenges** (2025)
   - arXiv: https://arxiv.org/html/2504.13015v1
   - PointNet++ showed inferior performance to PointNet on medical data
   - Local patterns of medical points are difficult to distinguish in fixed spatial contexts
   - Suggests careful design needed for medical applications

### Technical Details:
- **Architecture**: MLPs for local feature extraction, max pooling for global features
- **Limitations**: Cannot adequately handle local feature extraction in complex medical structures
- **Preprocessing**: Minimal preprocessing with point cloud normalization
- **Augmentation**: Random rotation, jittering, and scaling

## 2. Dynamic Graph CNN (DGCNN) for Medical Shape Analysis

### Core Paper
- **Dynamic Graph CNN for Learning on Point Clouds** (Wang et al., 2019)
  - arXiv: https://arxiv.org/abs/1801.07829
  - ACM: https://dl.acm.org/doi/10.1145/3326362
  - GitHub: https://github.com/antao97/dgcnn.pytorch

### Key Components:
1. **EdgeConv Module**: Captures local geometric structure while maintaining permutation invariance
2. **Dynamic Graph Construction**: K-NN algorithm recomputes graphs in each layer
3. **Performance**: State-of-the-art results on ModelNet40 and S3DIS benchmarks

### Medical Applications:
- Limited direct applications to vessel segmentation
- Strong performance in general 3D medical shape analysis
- Suitable for capturing fine-grained geometric properties of vessels

### Recent Improvements:
- **MP-DGCNN** (2024)
  - Nature: https://www.nature.com/articles/s40494-024-01289-z
  - Mix Pooling Dynamic Graph CNN for ancient architecture segmentation
  - Achieved 90.19% OA, 65.34% mIOU, and 79.41% mAcc

## 3. PointConv and Convolution-Based Approaches

### Core Paper
- **PointConv: Deep Convolutional Networks on 3D Point Clouds** (Wu et al., 2019)
  - CVPR: https://openaccess.thecvf.com/content_CVPR_2019/papers/Wu_PointConv_Deep_Convolutional_Networks_on_3D_Point_Clouds_CVPR_2019_paper.pdf
  - arXiv: https://ar5iv.labs.arxiv.org/html/1811.07246

### Key Features:
1. **Convolution on Point Clouds**: Extends dynamic filters to point cloud convolution
2. **Memory Efficiency**: Reformulation for handling large channel sizes
3. **Performance**: State-of-the-art on ShapeNet and ScanNet segmentation

### Medical Context:
- No direct vessel segmentation applications found
- Principles applicable to vascular structure analysis
- Hierarchical structure suitable for multi-scale vessel features

## 4. Graph Neural Networks for Vessel Segmentation

### Key Papers and Applications:

#### 1. **Deep Vessel Segmentation by Learning Graphical Connectivity** (2019)
- ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S1361841519300982
- Combines GNN with CNN to exploit local and global vessel structures

#### 2. **3D Graph-Connectivity Constrained Network** (2023)
- PubMed: https://pubmed.ncbi.nlm.nih.gov/34613925/
- IEEE Trans Med Imaging. 2023 Jan;42(1):183-195
- Integrates connectivity prior of hepatic vessels into CNN

#### 3. **Graph Convolutional Network for Head and Neck Vessel Labeling** (2020)
- SpringerLink: https://link.springer.com/chapter/10.1007/978-3-030-59861-7_48
- Labels 13 major head and neck vessels using point cloud representation
- Improves over conventional CNN methods

#### 4. **Vessel Segmentation via Link Prediction of GNNs** (2022)
- SpringerLink: https://link.springer.com/chapter/10.1007/978-3-031-18814-5_4
- Uses link prediction for maintaining vessel topology

### Advantages:
- Models inherent connectivity of vascular networks
- Captures long-range dependencies
- Handles irregular and complex vessel structures

## 5. Deep Learning Models for Medical Point Cloud Data

### Recent Developments:

#### 1. **3D Medical Point Transformer** (2021)
- arXiv: https://arxiv.org/abs/2112.04863
- Introduces Transformer architecture for medical point clouds
- Addresses complex biological structures

#### 2. **DeepVesselNet** (2020)
- PubMed: https://pubmed.ncbi.nlm.nih.gov/33363452/
- arXiv: https://arxiv.org/pdf/1803.09340
- Vessel segmentation, centerline prediction, and bifurcation detection
- Works on clinical MRA and CTA microscopy scans

#### 3. **VesselNet** (2019)
- PubMed: https://pubmed.ncbi.nlm.nih.gov/31220699/
- Multi-pathway CNN for hepatic vessel segmentation
- First 3D liver vessel segmentation using deep learning

## 6. Preprocessing and Augmentation Techniques

### Preprocessing Methods:
1. **Minimal Processing**: Min/max intensity normalization
2. **Noise Reduction**: Non-local mean filters
3. **Format Conversion**: DICOM to PNG/point cloud formats
4. **Centerline Extraction**: Using YOLO V7 for anchor points

### Data Augmentation:
1. **Geometric**: Rotation, scaling, jittering
2. **Elastic Transformation**: For vessel deformation
3. **Synthetic Data**: Gaussian kernel for stenosis patches
4. **Augmentation Factors**: 10x, 20x, 30x training data expansion

## 7. Performance Metrics and Benchmarks

### Common Metrics:
- **Segmentation**: IoU, Dice coefficient, F1 score
- **Classification**: Accuracy, precision, recall
- **Vessel-specific**: Centerline accuracy, connectivity preservation

### Reported Performance:
- PointNet++ (vertebrae): 96.15% accuracy
- DGCNN variants: 90.19% OA, 65.34% mIOU
- Vessel segmentation: F1 scores up to 0.917
- Processing time: ~0.04s per angiogram

## 8. Research Gaps and Future Directions

### Identified Gaps:
1. Limited direct application of point cloud methods to vessel segmentation
2. Lack of standardized benchmarks for medical point cloud vessel analysis
3. Integration challenges between point cloud and traditional medical imaging
4. Insufficient handling of thin, tortuous vessel structures

### Future Research Directions:
1. **Hybrid Approaches**: Combining point cloud methods with traditional CNNs
2. **Multi-modal Integration**: Fusing point cloud with CT/MRI data
3. **Real-time Processing**: Optimizing for clinical deployment
4. **Topology Preservation**: Better methods for maintaining vessel connectivity
5. **Uncertainty Quantification**: Addressing high uncertainty in vessel boundaries

## 9. Conclusions

The application of point cloud deep learning methods to medical vessel analysis is an emerging field with significant potential. While architectures like PointNet, DGCNN, and GNNs have shown success in general medical imaging tasks, their specific application to vessel segmentation from point cloud data remains limited. The unique challenges of medical vessel analysis—including thin structures, complex topology, and varying scales—require careful adaptation of these methods.

Graph Neural Networks show particular promise due to their ability to model vessel connectivity, while recent transformer-based approaches offer new possibilities for capturing global context. Future research should focus on developing hybrid approaches that leverage the strengths of multiple architectures while addressing the specific requirements of medical vessel analysis.

## References

This review synthesized findings from over 30 papers across PubMed, arXiv, and other academic databases. Key databases searched include:
- PubMed/MEDLINE
- arXiv
- IEEE Xplore
- Nature
- ScienceDirect
- SpringerLink
- ACM Digital Library

Search period: 2017-2025
Last updated: August 2025