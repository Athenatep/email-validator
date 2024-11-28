import asyncio
import aiosmtplib
from typing import Dict
import logging
import dns.resolver

class SMTPValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def validate_smtp(self, email: str) -> Dict[str, bool]:
        """
        Validates email using SMTP checks.
        
        Args:
            email: Email to validate
            
        Returns:
            Dict containing SMTP validation results
        """
        try:
            domain = email.split('@')[1]
            
            # Get MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                return {
                    "smtp_valid": False,
                    "reason": "No MX records found"
                }
                
            # Get primary MX server
            mx_host = str(mx_records[0].exchange)
            
            # Try SMTP connection
            smtp = aiosmtplib.SMTP(hostname=mx_host, port=25, timeout=10)
            await smtp.connect()
            
            # Perform SMTP validation
            code, message = await smtp.helo()
            code, message = await smtp.mail("test@example.com")
            code, message = await smtp.rcpt(email)
            
            await smtp.quit()
            
            is_valid = code == 250
            
            return {
                "smtp_valid": is_valid,
                "reason": None if is_valid else f"SMTP check failed: {message}"
            }
            
        except Exception as e:
            self.logger.error(f"Error validating SMTP for {email}: {str(e)}")
            return {
                "smtp_valid": False,
                "reason": f"SMTP validation error: {str(e)}"
            }