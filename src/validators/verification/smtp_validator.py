import logging
from typing import Dict
import asyncio
import aiosmtplib
import dns.resolver

class SMTPValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.timeout = 10
        self.max_retries = 2

    async def verify(self, email: str) -> Dict[str, any]:
        """
        Verifies email existence using SMTP.
        
        Args:
            email: Email to verify
            
        Returns:
            Dict containing SMTP verification results
        """
        try:
            domain = email.split('@')[1]
            results = {
                "is_valid": False,
                "mx_found": False,
                "smtp_check": False,
                "issues": []
            }

            # Get MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                if not mx_records:
                    results["issues"].append("No MX records found")
                    return results
                results["mx_found"] = True
                mx_host = str(mx_records[0].exchange)
            except Exception as e:
                results["issues"].append(f"MX lookup failed: {str(e)}")
                return results

            # SMTP verification
            for attempt in range(self.max_retries):
                try:
                    smtp = aiosmtplib.SMTP(
                        hostname=mx_host,
                        port=25,
                        timeout=self.timeout
                    )
                    await smtp.connect()
                    
                    code, _ = await smtp.helo()
                    if code != 250:
                        results["issues"].append("HELO failed")
                        continue

                    code, _ = await smtp.mail("test@example.com")
                    if code != 250:
                        results["issues"].append("MAIL FROM failed")
                        continue

                    code, message = await smtp.rcpt(email)
                    if code == 250:
                        results["smtp_check"] = True
                        results["is_valid"] = True
                        break
                    else:
                        results["issues"].append(f"RCPT TO failed: {message}")

                    await smtp.quit()
                    break

                except Exception as e:
                    results["issues"].append(f"SMTP check failed: {str(e)}")
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(1)  # Wait before retry
                    continue

            return results

        except Exception as e:
            self.logger.error(f"Error in SMTP verification for {email}: {str(e)}")
            return {
                "is_valid": False,
                "mx_found": False,
                "smtp_check": False,
                "issues": [f"Verification error: {str(e)}"]
            }