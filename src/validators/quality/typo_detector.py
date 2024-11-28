import logging
from typing import Dict, List
import re
from Levenshtein import distance

class TypoDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.common_domains = {
            'gmail.com': ['gmai.com', 'gmial.com', 'gmal.com', 'gmale.com'],
            'yahoo.com': ['yaho.com', 'yahooo.com', 'yahou.com'],
            'hotmail.com': ['hotmai.com', 'hotmal.com', 'hotmial.com'],
            'outlook.com': ['outlok.com', 'outlool.com', 'outlock.com']
        }
        self.keyboard_patterns = {
            'qwerty': ['qwert', 'qwerty', 'qwertz'],
            'asdfgh': ['asdf', 'asdfg', 'asdfgh'],
            'zxcvbn': ['zxcv', 'zxcvb', 'zxcvbn']
        }

    def check(self, email: str) -> Dict[str, any]:
        """
        Check for common email typos and suggest corrections.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing typo detection results
        """
        try:
            email = email.lower().strip()
            local_part, domain = email.split('@')
            
            results = {
                "has_typos": False,
                "suggestions": [],
                "issues": [],
                "confidence": 0
            }

            # Check domain typos
            domain_check = self._check_domain_typos(domain)
            if domain_check["has_typos"]:
                results["has_typos"] = True
                results["suggestions"].extend(
                    f"{local_part}@{d}" for d in domain_check["suggestions"]
                )
                results["confidence"] = max(results["confidence"], domain_check["confidence"])
                results["issues"].extend(domain_check["issues"])

            # Check local part typos
            local_check = self._check_local_part_typos(local_part)
            if local_check["has_typos"]:
                results["has_typos"] = True
                results["suggestions"].extend(
                    f"{s}@{domain}" for s in local_check["suggestions"]
                )
                results["confidence"] = max(results["confidence"], local_check["confidence"])
                results["issues"].extend(local_check["issues"])

            return results

        except Exception as e:
            self.logger.error(f"Error checking typos for {email}: {str(e)}")
            return {
                "has_typos": False,
                "suggestions": [],
                "issues": [f"Typo check failed: {str(e)}"],
                "confidence": 0
            }

    def _check_domain_typos(self, domain: str) -> Dict[str, any]:
        """Check for common domain typos."""
        results = {
            "has_typos": False,
            "suggestions": [],
            "issues": [],
            "confidence": 0
        }

        # Check against known typos
        for correct_domain, typos in self.common_domains.items():
            if domain in typos:
                results.update({
                    "has_typos": True,
                    "suggestions": [correct_domain],
                    "issues": [f"Possible typo of {correct_domain}"],
                    "confidence": 0.9
                })
                return results

        # Check for similar domains
        for correct_domain in self.common_domains.keys():
            if distance(domain, correct_domain) <= 2:
                results.update({
                    "has_typos": True,
                    "suggestions": [correct_domain],
                    "issues": [f"Similar to {correct_domain}"],
                    "confidence": 0.7
                })
                return results

        return results

    def _check_local_part_typos(self, local_part: str) -> Dict[str, any]:
        """Check for common local part typos."""
        results = {
            "has_typos": False,
            "suggestions": [],
            "issues": [],
            "confidence": 0
        }

        # Check for repeated characters
        if re.search(r'(.)\1{2,}', local_part):
            fixed = re.sub(r'(.)\1{2,}', r'\1\1', local_part)
            results["suggestions"].append(fixed)
            results["has_typos"] = True
            results["issues"].append("Multiple repeated characters")
            results["confidence"] = 0.6

        # Check for keyboard patterns
        for pattern, variants in self.keyboard_patterns.items():
            if any(v in local_part.lower() for v in variants):
                results["has_typos"] = True
                results["issues"].append("Keyboard pattern detected")
                results["confidence"] = 0.5

        return results