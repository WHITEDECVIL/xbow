"""
AI/ML Classification Engine for Vulnerability Analysis
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np

from src.utils.logger import logger, color_logger
from src.utils.helpers import RiskLevel
from src.threat_intelligence import ThreatIntelligence


class VulnerabilityClassifier:
    """Machine Learning classifier for vulnerability severity"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or Path(__file__).parent.parent.parent / "models" / "classifier.pkl"
        self.model = None
        self.threat_intel = ThreatIntelligence()  # Add threat intelligence
        self._load_or_create_model()
        
        # Feature weights
        self.feature_weights = {
            'exploitability': 0.25,
            'impact': 0.35,
            'affected_systems': 0.15,
            'public_exploit': 0.15,
            'proof_of_concept': 0.10,
        }
    
    def _load_or_create_model(self):
        """Load pre-trained model or create new one"""
        try:
            if Path(self.model_path).exists():
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                color_logger.success("Loaded ML model", "AI")
        except Exception as e:
            logger.warning(f"Could not load model: {e}, using rule-based classification")
            self.model = None
    
    def classify_vulnerability(self, vuln_data: Dict) -> Tuple[str, float]:
        """
        Classify vulnerability severity
        Returns: (severity_level, confidence)
        """
        
        if self.model:
            return self._ml_classify(vuln_data)
        else:
            return self._rule_based_classify(vuln_data)
    
    def _rule_based_classify(self, vuln_data: Dict) -> Tuple[str, float]:
        """Rule-based classification"""
        
        score = 0.0
        factors = 0
        
        # Analyze vulnerability name
        name = vuln_data.get('name', '').lower()
        
        critical_keywords = ['rce', 'code execution', 'remote execution', 'authentication bypass']
        high_keywords = ['sql injection', 'xss', 'csrf', 'buffer overflow', 'privilege escalation']
        medium_keywords = ['weak', 'missing', 'insecure', 'exposure', 'misconfiguration']
        
        if any(kw in name for kw in critical_keywords):
            score += 5.0 * self.feature_weights['exploitability']
            factors += 1
        elif any(kw in name for kw in high_keywords):
            score += 4.0 * self.feature_weights['exploitability']
            factors += 1
        elif any(kw in name for kw in medium_keywords):
            score += 3.0 * self.feature_weights['exploitability']
            factors += 1
        
        # Check exploitation difficulty
        if vuln_data.get('easy_exploit'):
            score += 1.0 * self.feature_weights['exploitability']
            factors += 1
        
        # Check if PoC available
        if vuln_data.get('has_poc'):
            score += 0.8 * self.feature_weights['proof_of_concept']
            factors += 1
        
        # Check public exploit
        if vuln_data.get('public_exploit'):
            score += 0.9 * self.feature_weights['public_exploit']
            factors += 1
        
        # Determine severity
        if score >= 4.0:
            severity = RiskLevel.CRITICAL
            confidence = 0.85
        elif score >= 3.0:
            severity = RiskLevel.HIGH
            confidence = 0.80
        elif score >= 2.0:
            severity = RiskLevel.MEDIUM
            confidence = 0.75
        elif score >= 1.0:
            severity = RiskLevel.LOW
            confidence = 0.70
        else:
            severity = RiskLevel.INFO
            confidence = 0.60
        
        return severity, confidence
    
    def _ml_classify(self, vuln_data: Dict) -> Tuple[str, float]:
        """ML-based classification"""
        try:
            features = self._extract_features(vuln_data)
            prediction = self.model.predict([features])[0]
            confidence = max(self.model.predict_proba([features])[0])
            
            severity_map = {0: RiskLevel.INFO, 1: RiskLevel.LOW, 2: RiskLevel.MEDIUM,
                          3: RiskLevel.HIGH, 4: RiskLevel.CRITICAL}
            
            return severity_map.get(prediction, RiskLevel.MEDIUM), confidence
        except Exception as e:
            logger.error(f"ML classification failed: {e}")
            return RiskLevel.MEDIUM, 0.5
    
    def _extract_features(self, vuln_data: Dict) -> List[float]:
        """Extract numerical features from vulnerability data"""
        features = []
        
        # Exploitability score (0-5)
        exploitability = 2.0
        if vuln_data.get('easy_exploit'):
            exploitability = 4.0
        features.append(exploitability / 5.0)
        
        # Impact score (0-5)
        impact = 2.0
        if 'rce' in vuln_data.get('name', '').lower():
            impact = 5.0
        features.append(impact / 5.0)
        
        # Affected systems count (normalized)
        affected = len(vuln_data.get('affected_systems', []))
        features.append(min(affected / 100, 1.0))
        
        # Public exploit (0 or 1)
        features.append(1.0 if vuln_data.get('public_exploit') else 0.0)
        
        # PoC availability (0 or 1)
        features.append(1.0 if vuln_data.get('has_poc') else 0.0)
        
        return features


class VulnerabilityPredictor:
    """Predicts additional vulnerabilities based on findings"""
    
    def __init__(self):
        self.vulnerability_relationships = {
            'Missing Security Headers': ['Weak SSL/TLS Configuration', 'Unencrypted Communication'],
            'SQL Injection': ['Authentication Bypass', 'Data Breach'],
            'XSS': ['Session Hijacking', 'Credential Theft'],
            'RCE': ['Lateral Movement', 'Data Exfiltration'],
            'Weak Credentials': ['Unauthorized Access', 'Account Takeover'],
        }
    
    def predict_related_vulnerabilities(self, found_vulnerabilities: List[Dict]) -> List[Dict]:
        """Predict related vulnerabilities based on findings"""
        color_logger.info("Analyzing vulnerability patterns", "PREDICT")
        
        predictions = []
        
        for vuln in found_vulnerabilities:
            vuln_name = vuln.get('name', '')
            
            for pattern, related in self.vulnerability_relationships.items():
                if pattern.lower() in vuln_name.lower():
                    for related_vuln in related:
                        prediction = {
                            'predicted_vulnerability': related_vuln,
                            'probability': 0.65,
                            'reason': f"Often found with: {vuln_name}",
                        }
                        predictions.append(prediction)
                        color_logger.info(f"Predicted: {related_vuln} (65%)", "PREDICT")
        
        return predictions
    
    def estimate_impact(self, vulnerabilities: List[Dict]) -> Dict:
        """Estimate overall impact of vulnerabilities"""
        
        impact = {
            'confidentiality': 0.0,
            'integrity': 0.0,
            'availability': 0.0,
            'overall_risk': 'MEDIUM',
        }
        
        impact_scores = []
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'MEDIUM')
            severity_value = RiskLevel.SEVERITY_MAP.get(severity, 3)
            impact_scores.append(severity_value)
            
            name = vuln.get('name', '').lower()
            
            if 'confidentiality' in name or 'disclosure' in name:
                impact['confidentiality'] += 0.2
            if 'injection' in name or 'bypass' in name:
                impact['integrity'] += 0.2
            if 'dos' in name or 'availability' in name:
                impact['availability'] += 0.2
        
        if impact_scores:
            avg_score = sum(impact_scores) / len(impact_scores)
            if avg_score >= 4.5:
                impact['overall_risk'] = RiskLevel.CRITICAL
            elif avg_score >= 3.5:
                impact['overall_risk'] = RiskLevel.HIGH
            elif avg_score >= 2.5:
                impact['overall_risk'] = RiskLevel.MEDIUM
            else:
                impact['overall_risk'] = RiskLevel.LOW
        
        return impact


class ThreatAnalyzer:
    """Analyzes threats and generates risk scores"""
    
    def __init__(self):
        self.classifier = VulnerabilityClassifier()
        self.predictor = VulnerabilityPredictor()
    
    def analyze_findings(self, findings: Dict) -> Dict:
        """Comprehensive threat analysis"""
        color_logger.info("Performing AI threat analysis", "ANALYSIS")
        
        analysis = {
            'timestamp': str(__import__('datetime').datetime.now()),
            'vulnerabilities': [],
            'predictions': [],
            'impact_assessment': {},
            'risk_rating': 'MEDIUM',
        }
        
        # Classify each vulnerability
        for vuln in findings.get('vulnerabilities', []):
            severity, confidence = self.classifier.classify_vulnerability(vuln)
            vuln['ai_severity'] = severity
            vuln['confidence'] = confidence
            analysis['vulnerabilities'].append(vuln)
        
        # Predict related vulnerabilities
        analysis['predictions'] = self.predictor.predict_related_vulnerabilities(
            analysis['vulnerabilities']
        )
        
        # Assess impact
        analysis['impact_assessment'] = self.predictor.estimate_impact(
            analysis['vulnerabilities']
        )
        
        # Overall risk rating
        if any(v.get('ai_severity') == RiskLevel.CRITICAL for v in analysis['vulnerabilities']):
            analysis['risk_rating'] = RiskLevel.CRITICAL
        elif any(v.get('ai_severity') == RiskLevel.HIGH for v in analysis['vulnerabilities']):
            analysis['risk_rating'] = RiskLevel.HIGH
        elif any(v.get('ai_severity') == RiskLevel.MEDIUM for v in analysis['vulnerabilities']):
            analysis['risk_rating'] = RiskLevel.MEDIUM
        
        return analysis
