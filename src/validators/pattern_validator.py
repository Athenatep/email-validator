import logging
from typing import Dict, List, Pattern
import re

class PatternValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.patterns: List[Dict[str, Pattern]] = [
            {
                "pattern": re.compile(r'^test\d*@'),
                "name": "test_email",
                "description": "Test email pattern"
            },
            {
                "pattern": re.compile(r'^[a-z]{1,2}\d{4,}@'),
                "name": "bot_pattern",
                "description": "Common bot email pattern"
            },
            {
                "pattern": re.compile(r'^(?!.*[aeiou].*[aeiou].*[aeiou])'),
                "name": "consonant_spam",
                "description": "Suspicious consonant pattern"
            }
        ]
        
    def check_patterns(self, email: str) -> Dict:
        """
        Check email against suspicious patterns.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing pattern check results
        """
        try:
            matches = []
            
            for pattern_dict in self.patterns:
                if pattern_dict["pattern"].match(email.lower()):
                    matches.append({
                        "pattern_name": pattern_dict["name"],
                        "description": pattern_dict["description"]
                    })
                    
            return {
                "suspicious": bool(matches),
                "matches": matches,
                "total_matches": len(matches)
            }
            
        except Exception as e:
            self.logger.error(f"Error checking patterns: {str(e)}")
            return {
                "suspicious": False,
                "matches": [],
                "total_matches": 0
            }