import logging
from typing import Dict, Optional
from .validator_factory import ValidatorFactory
from ..cache.cache_manager import CacheManager
from ..cache.cache_key_builder import CacheKeyBuilder

class EmailValidator:
    """Main email validation coordinator with caching."""
    
    def __init__(self, cache_enabled: bool = True):
        self.logger = logging.getLogger(__name__)
        self.cache = CacheManager() if cache_enabled else None
        self.cache_key_builder = CacheKeyBuilder()
        
        # Initialize validators
        self.syntax_validator = ValidatorFactory.create('syntax')
        self.domain_validator = ValidatorFactory.create('domain')
        self.spam_detector = ValidatorFactory.create('spam')
        self.disposable_detector = ValidatorFactory.create('disposable')
        self.smtp_validator = ValidatorFactory.create('smtp')
        self.reputation_validator = ValidatorFactory.create('reputation')
        self.duplicate_detector = ValidatorFactory.create('duplicate')
        self.typo_detector = ValidatorFactory.create('typo')

    async def validate(self, email: str, validation_options: Optional[Dict] = None) -> Dict:
        """
        Perform comprehensive email validation with caching.
        
        Args:
            email: Email to validate
            validation_options: Optional validation configuration
            
        Returns:
            Dict containing validation results
        """
        try:
            # Check cache first if enabled
            if self.cache:
                cache_key = self.cache_key_builder.build_validation_key(
                    email, validation_options
                )
                cached_result = await self.cache.get(cache_key)
                if cached_result:
                    self.logger.info(f"Cache hit for email: {email}")
                    return cached_result

            options = validation_options or {
                "check_syntax": True,
                "check_domain": True,
                "check_spam": True,
                "check_disposable": True,
                "check_smtp": True,
                "check_reputation": True,
                "check_duplicates": True,
                "check_typos": True
            }

            results = {
                "email": email,
                "is_valid": False,
                "score": 100,
                "issues": [],
                "checks": {},
                "suggestions": []
            }

            # Basic syntax check (always performed)
            syntax_result = self.syntax_validator.validate(email)
            results["checks"]["syntax"] = syntax_result
            if not syntax_result["is_valid"]:
                results["issues"].extend(syntax_result["issues"])
                results["score"] -= 50
                return await self._finalize_results(results, cache_key)

            # Domain validation with caching
            if options.get("check_domain"):
                domain = email.split('@')[1]
                mx_cache_key = self.cache_key_builder.build_mx_key(domain)
                
                domain_result = await self.cache.get(mx_cache_key)
                if not domain_result:
                    domain_result = await self.domain_validator.validate(domain)
                    await self.cache.set(mx_cache_key, domain_result, ttl=3600)
                    
                results["checks"]["domain"] = domain_result
                if not domain_result["is_valid"]:
                    results["issues"].extend(domain_result["issues"])
                    results["score"] -= 30

            # Spam detection
            if options.get("check_spam"):
                spam_result = self.spam_detector.analyze(email)
                results["checks"]["spam"] = spam_result
                if spam_result["is_suspicious"]:
                    results["issues"].extend(spam_result["issues"])
                    results["score"] -= spam_result["risk_score"]

            # Disposable email check
            if options.get("check_disposable"):
                disposable_result = await self.disposable_detector.check(email)
                results["checks"]["disposable"] = disposable_result
                if disposable_result["is_disposable"]:
                    results["issues"].append("Disposable email detected")
                    results["score"] -= 20

            # SMTP verification
            if options.get("check_smtp"):
                smtp_result = await self.smtp_validator.verify(email)
                results["checks"]["smtp"] = smtp_result
                if not smtp_result["is_valid"]:
                    results["issues"].extend(smtp_result["issues"])
                    results["score"] -= 25

            # Reputation check with caching
            if options.get("check_reputation"):
                domain = email.split('@')[1]
                rep_cache_key = self.cache_key_builder.build_reputation_key(domain)
                
                reputation_result = await self.cache.get(rep_cache_key)
                if not reputation_result:
                    reputation_result = await self.reputation_validator.check_reputation(email)
                    await self.cache.set(rep_cache_key, reputation_result, ttl=3600)
                    
                results["checks"]["reputation"] = reputation_result
                if reputation_result["blacklisted"]:
                    results["issues"].extend(reputation_result["issues"])
                    results["score"] -= 40

            # Duplicate check
            if options.get("check_duplicates"):
                duplicate_result = self.duplicate_detector.check(email)
                results["checks"]["duplicate"] = duplicate_result
                if duplicate_result["is_duplicate"]:
                    results["issues"].extend(duplicate_result["issues"])
                    results["score"] -= 15

            # Typo detection
            if options.get("check_typos"):
                typo_result = self.typo_detector.check(email)
                results["checks"]["typo"] = typo_result
                if typo_result["has_typos"]:
                    results["issues"].extend(typo_result["issues"])
                    results["suggestions"].extend(typo_result["suggestions"])
                    results["score"] -= 5

            return await self._finalize_results(results, cache_key)

        except Exception as e:
            self.logger.error(f"Error validating email {email}: {str(e)}")
            return {
                "email": email,
                "is_valid": False,
                "score": 0,
                "issues": [f"Validation error: {str(e)}"],
                "checks": {},
                "suggestions": []
            }

    async def _finalize_results(self, results: Dict, cache_key: Optional[str] = None) -> Dict:
        """Finalize validation results and cache if enabled."""
        # Ensure score is within bounds
        results["score"] = max(0, min(100, results["score"]))
        
        # Determine final validity
        results["is_valid"] = (
            results["score"] >= 70 and  # Minimum acceptable score
            not any(  # Critical checks must pass
                check.get("is_valid") is False
                for check in results["checks"].values()
                if "is_valid" in check
            )
        )

        # Cache results if enabled
        if self.cache and cache_key:
            await self.cache.set(cache_key, results)

        return results