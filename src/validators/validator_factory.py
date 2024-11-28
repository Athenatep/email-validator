import logging
from typing import Dict, Type
from .basic.syntax_validator import SyntaxValidator
from .basic.domain_validator import DomainValidator
from .security.spam_detector import SpamDetector
from .security.disposable_detector import DisposableDetector
from .verification.smtp_validator import SMTPValidator
from .verification.reputation_validator import ReputationValidator
from .quality.duplicate_detector import DuplicateDetector
from .quality.typo_detector import TypoDetector

class ValidatorFactory:
    """Factory for creating validator instances."""
    
    _validators: Dict[str, Type] = {
        'syntax': SyntaxValidator,
        'domain': DomainValidator,
        'spam': SpamDetector,
        'disposable': DisposableDetector,
        'smtp': SMTPValidator,
        'reputation': ReputationValidator,
        'duplicate': DuplicateDetector,
        'typo': TypoDetector
    }

    @classmethod
    def create(cls, validator_type: str):
        """
        Create a validator instance.
        
        Args:
            validator_type: Type of validator to create
            
        Returns:
            Validator instance
        """
        validator_class = cls._validators.get(validator_type)
        if not validator_class:
            raise ValueError(f"Unknown validator type: {validator_type}")
        return validator_class()