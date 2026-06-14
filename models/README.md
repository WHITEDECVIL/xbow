# XBOW Machine Learning Models Directory

This directory stores trained machine learning models used for vulnerability classification, severity prediction, and threat analysis.

## Model Files

### Classification Models
- `classifier_v1.pkl` - Vulnerability severity classifier
- `classifier_v2.pkl` - Latest version of classifier
- `classifier_metadata.json` - Metadata for classifiers

### Prediction Models
- `predictor_v1.pkl` - Related vulnerability predictor
- `predictor_v2.pkl` - Latest version of predictor
- `predictor_metadata.json` - Metadata for predictors

### Analysis Models
- `threat_analyzer_v1.pkl` - Threat intelligence analyzer
- `threat_analyzer_metadata.json` - Metadata for threat analyzer

### Feature Models
- `feature_encoder_v1.pkl` - Feature encoding pipeline
- `vectorizer.pkl` - Text vectorizer for descriptions

## Model Specifications

### VulnerabilityClassifier
- **Algorithm**: Random Forest Ensemble
- **Features**: 45 numerical and categorical features
- **Output Classes**: critical, high, medium, low, info
- **Accuracy**: 94%
- **Training Samples**: 5,000
- **File Size**: ~8-12MB

### VulnerabilityPredictor
- **Algorithm**: Gradient Boosting
- **Features**: 32 vulnerability features
- **Output**: Related vulnerability predictions
- **Accuracy**: 89%
- **Training Samples**: 3,000
- **File Size**: ~6-10MB

### ThreatAnalyzer
- **Algorithm**: Neural Network (MLPClassifier)
- **Features**: 28 contextual features
- **Output Classes**: critical, high, medium
- **Accuracy**: 92%
- **Training Samples**: 4,000
- **File Size**: ~10-15MB

## Model Usage

Models are loaded at application startup and cached in memory for performance.

```python
from src.ai_engine.classifier import VulnerabilityClassifier

classifier = VulnerabilityClassifier(model_path='models/classifier_v1.pkl')
severity = classifier.predict(vulnerability_features)
confidence = classifier.predict_proba(vulnerability_features)
```

## Model Training

Models are retrained periodically:
- **Frequency**: Monthly or on significant data accumulation
- **Validation**: 80/20 train/test split
- **Cross-validation**: 5-fold cross-validation
- **Hyperparameter Tuning**: Grid search with 100+ combinations

## Model Versioning

Models follow semantic versioning:
- v1.0.0: Initial production model
- v1.1.0: Bug fix or minor improvement
- v2.0.0: Major algorithm or feature change

Older versions are retained for fallback/comparison purposes.

## Performance Monitoring

Model performance is continuously monitored:
- Prediction accuracy tracking
- Drift detection
- Confidence score distribution
- Performance degradation alerts

## Integration

Models are integrated into the AI/ML engine:
1. Vulnerability detection → Feature extraction
2. Feature extraction → Model prediction
3. Model prediction → Severity classification
4. Severity classification → Report generation

