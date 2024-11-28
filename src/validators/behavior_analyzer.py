import logging
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict

class BehaviorAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.submission_history = defaultdict(list)
        self.ip_history = defaultdict(list)
        self.suspicious_threshold = 5
        
    def analyze_behavior(self, email: str, ip: str = None) -> Dict:
        """
        Analyze submission patterns and behavior.
        
        Args:
            email: Email being submitted
            ip: IP address of submission
            
        Returns:
            Dict containing behavior analysis results
        """
        try:
            now = datetime.now()
            domain = email.split('@')[1]
            
            results = {
                "suspicious": False,
                "reasons": [],
                "risk_score": 0
            }
            
            # Check submission frequency
            self.submission_history[domain].append(now)
            self._cleanup_history(domain)
            
            frequency = self._analyze_frequency(domain)
            if frequency["suspicious"]:
                results["suspicious"] = True
                results["reasons"].extend(frequency["reasons"])
                results["risk_score"] += frequency["risk_score"]
                
            # IP-based analysis
            if ip:
                self.ip_history[ip].append(now)
                ip_analysis = self._analyze_ip_behavior(ip)
                if ip_analysis["suspicious"]:
                    results["suspicious"] = True
                    results["reasons"].extend(ip_analysis["reasons"])
                    results["risk_score"] += ip_analysis["risk_score"]
                    
            return results
            
        except Exception as e:
            self.logger.error(f"Error in behavior analysis: {str(e)}")
            return {"suspicious": False, "reasons": ["Error during analysis"]}
            
    def _cleanup_history(self, domain: str):
        """Remove entries older than 24 hours."""
        cutoff = datetime.now() - timedelta(hours=24)
        self.submission_history[domain] = [
            dt for dt in self.submission_history[domain]
            if dt > cutoff
        ]
        
    def _analyze_frequency(self, domain: str) -> Dict:
        """Analyze submission frequency patterns."""
        results = {
            "suspicious": False,
            "reasons": [],
            "risk_score": 0
        }
        
        submissions = self.submission_history[domain]
        
        # Check submission count
        if len(submissions) > self.suspicious_threshold:
            results["suspicious"] = True
            results["reasons"].append(f"High submission frequency: {len(submissions)} in 24h")
            results["risk_score"] += 2
            
        # Check for burst patterns
        if len(submissions) >= 3:
            intervals = [
                (submissions[i] - submissions[i-1]).total_seconds()
                for i in range(1, len(submissions))
            ]
            avg_interval = sum(intervals) / len(intervals)
            
            if avg_interval < 60:  # Less than 1 minute average
                results["suspicious"] = True
                results["reasons"].append("Rapid-fire submissions detected")
                results["risk_score"] += 3
                
        return results
        
    def _analyze_ip_behavior(self, ip: str) -> Dict:
        """Analyze IP-based submission patterns."""
        results = {
            "suspicious": False,
            "reasons": [],
            "risk_score": 0
        }
        
        submissions = self.ip_history[ip]
        
        # Check submission volume
        if len(submissions) > self.suspicious_threshold * 2:
            results["suspicious"] = True
            results["reasons"].append(f"High volume from IP: {len(submissions)} submissions")
            results["risk_score"] += 2
            
        # Check for automated patterns
        if len(submissions) >= 3:
            intervals = [
                (submissions[i] - submissions[i-1]).total_seconds()
                for i in range(1, len(submissions))
            ]
            
            # Check for consistent intervals (bot-like behavior)
            interval_diffs = [
                abs(intervals[i] - intervals[i-1])
                for i in range(1, len(intervals))
            ]
            
            if interval_diffs and max(interval_diffs) < 1:  # Very consistent timing
                results["suspicious"] = True
                results["reasons"].append("Bot-like submission pattern detected")
                results["risk_score"] += 4
                
        return results