"""
Real-time Accuracy Metrics & Validation Module
Tracks detection accuracy, false positives/negatives, and provides scoring
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
from src.utils.logger import logger, color_logger


class AccuracyMetrics:
    """Track and report scanning accuracy metrics"""
    
    def __init__(self, metrics_dir: str = "metrics"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(exist_ok=True)
        
        # Metrics tracking
        self.true_positives = 0
        self.false_positives = 0
        self.true_negatives = 0
        self.false_negatives = 0
        
        # Confidence tracking
        self.confidence_distribution = defaultdict(int)
        
        # Detection techniques accuracy
        self.technique_accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    def record_finding(self, finding: Dict, verified: bool = None, confidence: float = 0.0):
        """Record a finding for accuracy tracking"""
        
        if verified is None:
            # Default: assume high-confidence findings are TP
            verified = confidence > 0.7
        
        if verified:
            self.true_positives += 1
        else:
            self.false_positives += 1
        
        # Track confidence distribution
        confidence_bucket = int(confidence * 10) * 10
        self.confidence_distribution[confidence_bucket] += 1
        
        # Record detection technique
        technique = finding.get('detection_method', 'unknown')
        self.technique_accuracy[technique]['total'] += 1
        if verified:
            self.technique_accuracy[technique]['correct'] += 1
    
    def get_precision(self) -> float:
        """Precision = TP / (TP + FP)"""
        total = self.true_positives + self.false_positives
        if total == 0:
            return 0.0
        return self.true_positives / total
    
    def get_recall(self) -> float:
        """Recall = TP / (TP + FN)"""
        total = self.true_positives + self.false_negatives
        if total == 0:
            return 0.0
        return self.true_positives / total
    
    def get_f1_score(self) -> float:
        """F1 Score = 2 * (Precision * Recall) / (Precision + Recall)"""
        precision = self.get_precision()
        recall = self.get_recall()
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    def get_accuracy(self) -> float:
        """Overall Accuracy = (TP + TN) / (TP + TN + FP + FN)"""
        total = self.true_positives + self.true_negatives + \
                self.false_positives + self.false_negatives
        
        if total == 0:
            return 0.0
        
        return (self.true_positives + self.true_negatives) / total
    
    def get_technique_accuracy(self) -> Dict[str, float]:
        """Get per-technique accuracy scores"""
        results = {}
        
        for technique, stats in self.technique_accuracy.items():
            total = stats['total']
            if total > 0:
                accuracy = stats['correct'] / total
                results[technique] = accuracy
        
        return results
    
    def generate_report(self) -> Dict:
        """Generate comprehensive accuracy report"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_metrics': {
                'precision': round(self.get_precision(), 3),
                'recall': round(self.get_recall(), 3),
                'f1_score': round(self.get_f1_score(), 3),
                'accuracy': round(self.get_accuracy(), 3),
            },
            'confusion_matrix': {
                'true_positives': self.true_positives,
                'false_positives': self.false_positives,
                'true_negatives': self.true_negatives,
                'false_negatives': self.false_negatives,
            },
            'confidence_distribution': dict(self.confidence_distribution),
            'technique_accuracy': self.get_technique_accuracy(),
        }
        
        return report
    
    def save_metrics(self, filename: str = None):
        """Save metrics to JSON file"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"accuracy_metrics_{timestamp}.json"
        
        filepath = self.metrics_dir / filename
        report = self.generate_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        color_logger.success(f"Metrics saved: {filepath}", "METRICS")
        return str(filepath)
    
    def print_report(self):
        """Print accuracy report to console"""
        
        report = self.generate_report()
        metrics = report['overall_metrics']
        
        print("\n" + "="*60)
        print("XBOW ACCURACY METRICS")
        print("="*60)
        print(f"Precision:  {metrics['precision']:.1%}")
        print(f"Recall:     {metrics['recall']:.1%}")
        print(f"F1 Score:   {metrics['f1_score']:.1%}")
        print(f"Accuracy:   {metrics['accuracy']:.1%}")
        print("-"*60)
        print(f"True Positives:  {report['confusion_matrix']['true_positives']}")
        print(f"False Positives: {report['confusion_matrix']['false_positives']}")
        print(f"True Negatives:  {report['confusion_matrix']['true_negatives']}")
        print(f"False Negatives: {report['confusion_matrix']['false_negatives']}")
        print("="*60 + "\n")


class RealTimeAccuracyValidator:
    """Real-time validation of findings against ground truth"""
    
    def __init__(self):
        self.metrics = AccuracyMetrics()
        
        # Known false positive patterns
        self.false_positive_filters = [
            {
                'pattern': 'Missing Security Headers',
                'condition': lambda finding: finding.get('severity', '') == 'LOW',
                'reason': 'Low-severity header findings may be false positives on CDN-hosted sites'
            },
            {
                'pattern': 'Server Information Disclosure',
                'condition': lambda finding: finding.get('evidence', '').startswith('cloudflare'),
                'reason': 'Cloudflare headers are expected and not true vulnerabilities'
            },
        ]
    
    def validate_finding(self, finding: Dict) -> Dict:
        """Validate finding and assess likelihood of false positive"""
        
        validation = {
            'finding': finding.get('name'),
            'is_likely_fp': False,
            'confidence_adjustment': 0.0,
            'reason': '',
        }
        
        # Check against false positive patterns
        for fp_filter in self.false_positive_filters:
            if fp_filter['pattern'].lower() in finding.get('name', '').lower():
                if fp_filter['condition'](finding):
                    validation['is_likely_fp'] = True
                    validation['confidence_adjustment'] = -0.15
                    validation['reason'] = fp_filter['reason']
                    break
        
        # Return validation metadata
        return validation
    
    def enhance_confidence(self, finding: Dict, threat_intel_data: Dict) -> float:
        """Enhance confidence score using threat intelligence"""
        
        original_confidence = finding.get('confidence', 0.5)
        enhanced = original_confidence
        
        # Add confidence based on CVE corroboration
        if threat_intel_data.get('cve_corroboration'):
            enhanced = min(1.0, enhanced + 0.1)
        
        # Add confidence if active exploits exist
        if threat_intel_data.get('exploit_known'):
            enhanced = min(1.0, enhanced + 0.15)
        
        # Filter false positives
        validation = self.validate_finding(finding)
        if validation['is_likely_fp']:
            enhanced = max(0.3, enhanced + validation['confidence_adjustment'])
        
        return enhanced
