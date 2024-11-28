import logging
from typing import Dict, List
import re
from collections import Counter

class ContentAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.load_patterns()
        
    def load_patterns(self):
        """Load pattern databases."""
        self.temp_patterns = [
            r'temp\d*',
            r'throwaway',
            r'tempmail',
            r'tmpmail'
        ]
        
        self.suspicious_keywords = {
            'spam', 'test', 'temp', 'fake', 'dummy',
            'disposable', 'trash', 'junk', 'anon'
        }
        
        self.common_services = {
            'gmail.com': ['googlemail.com'],
            'outlook.com': ['hotmail.com', 'live.com'],
            'yahoo.com': ['ymail.com', 'rocketmail.com']
        }
        
    def analyze_content(self, email: str) -> Dict:
        """
        Analyze email content for suspicious patterns.
        
        Args:
            email: Email to analyze
            
        Returns:
            Dict containing content analysis results
        """
        try:
            local_part, domain = email.lower().split('@')
            
            results = {
                "suspicious": False,
                "reasons": [],
                "suggestions": [],
                "risk_factors": []
            }
            
            # Check for temporary email patterns
            if any(re.search(pattern, local_part) for pattern in self.temp_patterns):
                results["suspicious"] = True
                results["reasons"].append("Temporary email pattern detected")
                results["risk_factors"].append("temp_pattern")
                
            # Keyword analysis
            words = set(re.findall(r'[a-z]+', local_part))
            suspicious_words = words.intersection(self.suspicious_keywords)
            if suspicious_words:
                results["suspicious"] = True
                results["reasons"].append(f"Suspicious keywords: {', '.join(suspicious_words)}")
                results["risk_factors"].append("suspicious_keywords")
                
            # Check for alternative domains
            for main_domain, alternatives in self.common_services.items():
                if domain in alternatives:
                    results["suggestions"].append(f"Consider using {main_domain}")
                    
            # Analyze local part structure
            structure_analysis = self._analyze_structure(local_part)
            if structure_analysis["suspicious"]:
                results["suspicious"] = True
                results["reasons"].extend(structure_analysis["reasons"])
                results["risk_factors"].extend(structure_analysis["risk_factors"])
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error in content analysis: {str(e)}")
            return {"suspicious": False, "reasons": ["Error during analysis"]}
            
    def _analyze_structure(self, local_part: str) -> Dict:
        """Analyze the structure of the local part."""
        results = {
            "suspicious": False,
            "reasons": [],
            "risk_factors": []
        }
        
        # Check for excessive numbers
        num_count = len(re.findall(r'\d', local_part))
        if num_count > len(local_part) * 0.4:
            results["suspicious"] = True
            results["reasons"].append("Excessive number usage")
            results["risk_factors"].append("high_number_ratio")
            
        # Check for random-looking strings
        if re.match(r'^[a-z0-9]{10,}$', local_part):
            char_counts = Counter(local_part)
            unique_ratio = len(char_counts) / len(local_part)
            
            if unique_ratio > 0.8:  # High variety of characters
                results["suspicious"] = True
                results["reasons"].append("Random-looking string detected")
                results["risk_factors"].append("random_pattern")
                
        # Check for repeating patterns
        if re.search(r'(.{2,})\1{2,}', local_part):
            results["suspicious"] = True
            results["reasons"].append("Repeating pattern detected")
            results["risk_factors"].append("repeating_pattern")
            
        return results