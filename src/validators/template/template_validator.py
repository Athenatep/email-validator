import logging
from typing import Dict, List, Optional, Pattern
import re
from dataclasses import dataclass

@dataclass
class EmailTemplate:
    """Email template definition"""
    name: str
    pattern: Pattern
    description: str
    examples: List[str]
    validation_rules: Dict[str, any]

class TemplateValidator:
    """Validates emails against predefined templates and patterns"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._load_templates()
        
    def _load_templates(self):
        """Load predefined email templates."""
        self.templates = [
            EmailTemplate(
                name="corporate",
                pattern=re.compile(r"^[a-z]+\.[a-z]+@[a-z0-9-]+\.[a-z]{2,}$"),
                description="Standard corporate email format (firstname.lastname)",
                examples=["john.doe@company.com"],
                validation_rules={
                    "min_length": 3,
                    "max_length": 64,
                    "allowed_chars": r"[a-z0-9.-]"
                }
            ),
            EmailTemplate(
                name="support",
                pattern=re.compile(r"^support(?:\+[a-z0-9]+)?@[a-z0-9-]+\.[a-z]{2,}$"),
                description="Support email with optional department",
                examples=["support@company.com", "support+sales@company.com"],
                validation_rules={
                    "allowed_prefixes": ["support", "help", "contact"],
                    "max_department_length": 20
                }
            ),
            EmailTemplate(
                name="no-reply",
                pattern=re.compile(r"^(?:no-?reply|noreply|donotreply)@[a-z0-9-]+\.[a-z]{2,}$"),
                description="Automated no-reply address",
                examples=["noreply@company.com", "no-reply@company.com"],
                validation_rules={
                    "allowed_variations": ["noreply", "no-reply", "donotreply"]
                }
            )
        ]
        
    def validate(self, email: str) -> Dict[str, any]:
        """
        Validate email against known templates.
        
        Args:
            email: Email to validate
            
        Returns:
            Dict containing validation results
        """
        try:
            email = email.lower().strip()
            results = {
                "matches_template": False,
                "template_name": None,
                "validation_errors": [],
                "suggestions": []
            }
            
            # Check against each template
            for template in self.templates:
                if template.pattern.match(email):
                    results["matches_template"] = True
                    results["template_name"] = template.name
                    
                    # Validate against template rules
                    validation_errors = self._validate_rules(
                        email, template.validation_rules
                    )
                    if validation_errors:
                        results["validation_errors"].extend(validation_errors)
                    break
                    
            # Generate suggestions if no match
            if not results["matches_template"]:
                results["suggestions"] = self._generate_suggestions(email)
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating template: {str(e)}")
            return {
                "matches_template": False,
                "template_name": None,
                "validation_errors": [f"Validation error: {str(e)}"],
                "suggestions": []
            }
            
    def _validate_rules(self, email: str, rules: Dict) -> List[str]:
        """Validate email against template-specific rules."""
        errors = []
        local_part = email.split('@')[0]
        
        if "min_length" in rules and len(local_part) < rules["min_length"]:
            errors.append(f"Local part too short (min {rules['min_length']} chars)")
            
        if "max_length" in rules and len(local_part) > rules["max_length"]:
            errors.append(f"Local part too long (max {rules['max_length']} chars)")
            
        if "allowed_chars" in rules:
            invalid_chars = re.findall(f"[^{rules['allowed_chars']}]", local_part)
            if invalid_chars:
                errors.append(f"Invalid characters found: {set(invalid_chars)}")
                
        if "allowed_prefixes" in rules:
            prefix = local_part.split('+')[0]
            if prefix not in rules["allowed_prefixes"]:
                errors.append(f"Invalid prefix. Allowed: {rules['allowed_prefixes']}")
                
        if "allowed_variations" in rules and local_part not in rules["allowed_variations"]:
            errors.append(f"Invalid variation. Allowed: {rules['allowed_variations']}")
            
        return errors
        
    def _generate_suggestions(self, email: str) -> List[str]:
        """Generate template suggestions for non-matching email."""
        suggestions = []
        local_part, domain = email.split('@')
        
        # Suggest corporate format if appears to be a name
        if re.match(r"^[a-z]+[a-z0-9]*$", local_part):
            suggestions.append(f"{local_part}.lastname@{domain}")
            
        # Suggest support format if contains support-related words
        if any(word in local_part for word in ["help", "support", "contact"]):
            suggestions.append(f"support@{domain}")
            suggestions.append(f"support+{local_part}@{domain}")
            
        return suggestions