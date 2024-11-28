import logging
import asyncio
from typing import List, Dict, Callable
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from pathlib import Path

class BatchProcessor:
    """Handles batch processing of email validations."""
    
    def __init__(self, validator, batch_size: int = 100):
        self.logger = logging.getLogger(__name__)
        self.validator = validator
        self.batch_size = batch_size
        self.progress_callback = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def set_progress_callback(self, callback: Callable[[int, int], None]):
        """Set callback for progress updates."""
        self.progress_callback = callback
        
    async def process_file(self, file_path: str) -> List[Dict]:
        """
        Process emails from a file in batches.
        
        Args:
            file_path: Path to file containing emails
            
        Returns:
            List of validation results
        """
        try:
            emails = self._load_emails(file_path)
            return await self.process_emails(emails)
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return []
            
    async def process_emails(self, emails: List[str]) -> List[Dict]:
        """
        Process a list of emails in batches.
        
        Args:
            emails: List of emails to validate
            
        Returns:
            List of validation results
        """
        try:
            total_emails = len(emails)
            results = []
            processed = 0
            
            # Process in batches
            for i in range(0, total_emails, self.batch_size):
                batch = emails[i:i + self.batch_size]
                batch_results = await self._process_batch(batch)
                results.extend(batch_results)
                
                processed += len(batch)
                if self.progress_callback:
                    self.progress_callback(processed, total_emails)
                    
            return results
            
        except Exception as e:
            self.logger.error(f"Error in batch processing: {str(e)}")
            return []
            
    async def _process_batch(self, batch: List[str]) -> List[Dict]:
        """Process a single batch of emails."""
        try:
            tasks = [
                self.validator.validate(email)
                for email in batch
            ]
            return await asyncio.gather(*tasks)
            
        except Exception as e:
            self.logger.error(f"Error processing batch: {str(e)}")
            return []
            
    def _load_emails(self, file_path: str) -> List[str]:
        """Load emails from file."""
        try:
            path = Path(file_path)
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
                # Assume first column contains emails
                return df.iloc[:, 0].tolist()
            else:
                with open(file_path, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
                    
        except Exception as e:
            self.logger.error(f"Error loading emails from {file_path}: {str(e)}")
            return []