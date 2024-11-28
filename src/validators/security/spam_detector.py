import logging
from typing import Dict
import re
from collections import Counter

class SpamDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.suspicious_patterns = [
            r'^test\d*@',
            r'^[a-z]{1,2}\d{4,}@',
            r'^(?!.*[aeiou].*[aeiou].*[aeiou])',
            r'^abuse@',
            r'^postmaster@',
            r'^spam@',
            r'^noreply@',
            r'^no-reply@',
            r'^admin@'
        ]
        self.role_addresses = {
            'info', 'sales', 'support', 'contact', 'admin', 'webmaster',
            'hostmaster', 'postmaster', 'abuse', 'security'
        }

    def analyze(self, email: str) -> Dict[str, any]:
        """
        Analyzes email for spam patterns and suspicious characteristics.
        
        Args:
            email: Email to analyze
            
        Returns:
            Dict containing spam analysis results
        """
        try:
            email = email.lower()
            local_part, domain = email.split('@')

            results = {
                "is_suspicious": False,
                "is_spam_trap": False,
                "risk_score": 0,
                "issues": [],
                "patterns_matched": []
            }

            # Check patterns
            for pattern in self.suspicious_patterns:
                if re.match(pattern, email):
                    results["patterns_matched"].append(pattern)
                    results["risk_score"] += 2

            # Check role-based addresses
            if local_part in self.role_addresses:
                results["is_spam_trap"] = True
                results["issues"].append("Role-based email detected")
                results["risk_score"] += 3

            # Analyze character distribution
            char_stats = self._analyze_char_distribution(local_part)
            if char_stats["suspicious"]:
                results["issues"].extend(char_stats["issues"])
                results["risk_score"] += char_stats["risk_score"]

            # Set final results
            results["is_suspicious"] = (
                results["is_spam_trap"] or 
                bool(results["patterns_matched"]) or 
                results["risk_score"] > 5
            )

            return results

        except Exception as e:
            self.logger.error(f"Error in spam analysis for {email}: {str(e)}")
            return {
                "is_suspicious": False,
                "is_spam_trap": False,
                "risk_score": 0,
                "issues": ["Error during analysis"],
                "patterns_matched": []
            }

    def _analyze_char_distribution(self, text: str) -> Dict[str, any]:
        """Analyze character distribution for suspicious patterns."""
        results = {
            "suspicious": False,
            "issues": [],
            "risk_score": 0
        }

        # Count character types
        counts = Counter({
            'letters': len(re.findall(r'[a-z]', text)),
            'digits': len(re.findall(r'\d', text)),
            'special': len(re.findall(r'[^a-z0-9]', text))
        })

        # Check distributions
        if counts['digits'] > len(text) * 0.5:
            results["suspicious"] = True
            results["issues"].append("High number of digits")
            results["risk_score"] += 2

        if counts['special'] > len(text) * 0.3:
            results["suspicious"] = True
            results["issues"].append("High number of special characters")
            results["risk_score"] += 2

        return results