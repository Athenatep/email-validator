import logging
from typing import Dict
import re
import numpy as np
from collections import Counter

class AIValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.entropy_threshold = 3.5
        
    def analyze_email(self, email: str) -> Dict:
        """
        Use AI/ML techniques to detect suspicious emails.
        
        Args:
            email: Email to analyze
            
        Returns:
            Dict containing AI analysis results
        """
        try:
            local_part = email.split('@')[0].lower()
            
            results = {
                "suspicious": False,
                "reasons": [],
                "entropy": 0,
                "patterns": []
            }
            
            # Calculate entropy
            entropy = self._calculate_entropy(local_part)
            results["entropy"] = entropy
            
            if entropy > self.entropy_threshold:
                results["suspicious"] = True
                results["reasons"].append("High entropy - possibly random generation")
                
            # Check character distribution
            char_dist = self._analyze_char_distribution(local_part)
            if char_dist["suspicious"]:
                results["suspicious"] = True
                results["reasons"].extend(char_dist["reasons"])
                
            # Pattern recognition
            patterns = self._detect_patterns(local_part)
            if patterns["suspicious"]:
                results["suspicious"] = True
                results["reasons"].extend(patterns["reasons"])
                results["patterns"] = patterns["detected"]
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error in AI analysis: {str(e)}")
            return {"suspicious": False, "reasons": ["Error during analysis"]}
            
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text."""
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        return -sum(p * np.log2(p) for p in prob)
        
    def _analyze_char_distribution(self, text: str) -> Dict:
        """Analyze character distribution for anomalies."""
        results = {"suspicious": False, "reasons": []}
        
        # Count character types
        counts = Counter({
            'letters': len(re.findall(r'[a-z]', text)),
            'digits': len(re.findall(r'\d', text)),
            'special': len(re.findall(r'[^a-z0-9]', text))
        })
        
        # Check for unusual distributions
        if counts['digits'] > len(text) * 0.5:
            results["suspicious"] = True
            results["reasons"].append("Unusually high number of digits")
            
        if counts['special'] > len(text) * 0.3:
            results["suspicious"] = True
            results["reasons"].append("Unusually high number of special characters")
            
        return results
        
    def _detect_patterns(self, text: str) -> Dict:
        """Detect suspicious patterns in text."""
        patterns = {
            'repeated_chars': r'(.)\1{2,}',
            'number_sequence': r'\d{3,}',
            'keyboard_pattern': r'(?:qwerty|asdfgh|zxcvbn)',
            'alternating': r'(?:[a-z]\d){3,}'
        }
        
        results = {
            "suspicious": False,
            "reasons": [],
            "detected": []
        }
        
        for name, pattern in patterns.items():
            if re.search(pattern, text):
                results["suspicious"] = True
                results["reasons"].append(f"Detected {name.replace('_', ' ')}")
                results["detected"].append(name)
                
        return results