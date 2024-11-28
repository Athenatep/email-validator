import asyncio
import aiosmtplib
from typing import Dict
import logging
import dns.resolver

class CatchallDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def check_catchall(self, domain: str) -> Dict[str, bool]:
        """
        Detects if a domain has catch-all email configuration.
        
        Args:
            domain: Domain to check
            
        Returns:
            Dict containing catch-all detection results
        """
        try:
            # Generate a random email that's unlikely to exist
            test_email = f"nonexistent_random_user_123456@{domain}"
            
            # Get MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                return {"is_catchall": False, "reason": "No MX records found"}
                
            # Get the primary MX server
            mx_host = str(mx_records[0].exchange)
            
            # Try SMTP connection
            smtp = aiosmtplib.SMTP(hostname=mx_host, port=25, timeout=10)
            await smtp.connect()
            
            # Try RCPT command with the test email
            code, message = await smtp.helo()
            code, message = await smtp.mail("test@example.com")
            code, message = await smtp.rcpt(test_email)
            
            await smtp.quit()
            
            # If the server accepts the non-existent email, it's likely a catch-all
            is_catchall = code == 250
            
            return {
                "is_catchall": is_catchall,
                "reason": "Domain accepts all emails" if is_catchall else None
            }
            
        except Exception as e:
            self.logger.error(f"Error checking catch-all for {domain}: {str(e)}")
            return {"is_catchall": False, "reason": "Error during check"}