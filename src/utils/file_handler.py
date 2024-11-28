import logging
from typing import List, Dict
import pandas as pd
from pathlib import Path

class FileHandler:
    """Handles file operations for email validation."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def read_file(self, file_path: str) -> List[str]:
        """
        Read emails from file.
        
        Args:
            file_path: Path to input file
            
        Returns:
            List of email addresses
        """
        try:
            path = Path(file_path)
            suffix = path.suffix.lower()
            
            if suffix == '.csv':
                return self._read_csv(file_path)
            elif suffix == '.xlsx' or suffix == '.xls':
                return self._read_excel(file_path)
            elif suffix == '.txt':
                return self._read_text(file_path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")
                
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {str(e)}")
            raise
            
    def export_results(self, results: List[Dict], file_path: str):
        """
        Export validation results.
        
        Args:
            results: List of validation results
            file_path: Output file path
        """
        try:
            path = Path(file_path)
            suffix = path.suffix.lower()
            
            if suffix == '.csv':
                self._export_csv(results, file_path)
            elif suffix == '.json':
                self._export_json(results, file_path)
            else:
                raise ValueError(f"Unsupported export format: {suffix}")
                
        except Exception as e:
            self.logger.error(f"Error exporting results to {file_path}: {str(e)}")
            raise
            
    def _read_csv(self, file_path: str) -> List[str]:
        """Read emails from CSV file."""
        df = pd.read_csv(file_path)
        # Try to find email column
        email_columns = [col for col in df.columns if 'email' in col.lower()]
        if email_columns:
            return df[email_columns[0]].dropna().tolist()
        # If no email column found, use first column
        return df.iloc[:, 0].dropna().tolist()
        
    def _read_excel(self, file_path: str) -> List[str]:
        """Read emails from Excel file."""
        df = pd.read_excel(file_path)
        email_columns = [col for col in df.columns if 'email' in col.lower()]
        if email_columns:
            return df[email_columns[0]].dropna().tolist()
        return df.iloc[:, 0].dropna().tolist()
        
    def _read_text(self, file_path: str) -> List[str]:
        """Read emails from text file."""
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
            
    def _export_csv(self, results: List[Dict], file_path: str):
        """Export results to CSV."""
        df = pd.DataFrame(results)
        # Flatten nested structures
        df['issues'] = df['issues'].apply(lambda x: '|'.join(x))
        df['suggestions'] = df['suggestions'].apply(lambda x: '|'.join(x))
        df.to_csv(file_path, index=False)
        
    def _export_json(self, results: List[Dict], file_path: str):
        """Export results to JSON."""
        pd.DataFrame(results).to_json(file_path, orient='records', indent=2)