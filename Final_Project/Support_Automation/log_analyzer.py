import re
import collections
import json
from datetime import datetime

# Regex for parsing standard Apache/Nginx combined access logs
LOG_REGEX = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] '
    r'"(?P<method>\S+) (?P<endpoint>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
)

class IncidentResponder:
    def __init__(self, log_file):
        self.log_file = log_file
        self.error_counts = collections.Counter()
        self.ip_requests = collections.Counter()
        self.suspicious_ips = set()

    def parse_logs(self):
        print(f"[*] Analyzing logs from: {self.log_file}")
        with open(self.log_file, 'r') as f:
            for line in f:
                match = LOG_REGEX.search(line)
                if match:
                    data = match.groupdict()
                    status = int(data['status'])
                    ip = data['ip']
                    
                    self.ip_requests[ip] += 1
                    
                    if status >= 500:
                        self.error_counts['5xx_errors'] += 1
                    elif status == 429:
                        self.error_counts['429_ratelimit'] += 1
                        self.suspicious_ips.add(ip)

    def detect_anomalies(self):
        print("[*] Detecting anomalies...")
        # Threshold: More than 100 requests from a single IP is considered a DDoS/Brute-force attempt in this context
        for ip, count in self.ip_requests.items():
            if count > 100:
                self.suspicious_ips.add(ip)
                
        if self.error_counts['5xx_errors'] > 50 or len(self.suspicious_ips) > 0:
            return True
        return False

    def generate_rca_report(self):
        print("[*] Generating Root Cause Analysis (RCA) Report...")
        report = f"""# ROOT CAUSE ANALYSIS (RCA) - AUTOMATED REPORT
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. Incident Summary
An automated log analysis detected a severe traffic anomaly indicating a potential service disruption.

## 2. Technical Details
- **Total 5xx (Server Errors):** {self.error_counts.get('5xx_errors', 0)}
- **Total 429 (Rate Limited):** {self.error_counts.get('429_ratelimit', 0)}
- **Suspicious IPs identified:** {list(self.suspicious_ips)}

## 3. Investigation Steps
1. Ingested server access logs using Regex parsing.
2. Aggregated HTTP status codes.
3. Identified IP addresses exceeding normal rate thresholds.

## 4. Remediation Actions (Automated)
- [Simulated] Blocking IPs {list(self.suspicious_ips)} at the WAF level.
- [Simulated] Alert dispatched to Slack `#ops-alerts` channel.
"""
        with open("RCA_Report.md", "w") as f:
            f.write(report)
        print("[+] RCA_Report.md successfully generated.")

    def trigger_webhook_alert(self):
        # Simulating a webhook payload for Datadog / Slack / Jira
        payload = {
            "text": "🚨 *CRITICAL INCIDENT DETECTED* 🚨\nSpike in 5xx errors or DDoS attempt detected.",
            "suspicious_ips": list(self.suspicious_ips)
        }
        print(f"[+] Alert Payload Dispatched: {json.dumps(payload)}")

if __name__ == "__main__":
    responder = IncidentResponder("server_access.log")
    responder.parse_logs()
    
    if responder.detect_anomalies():
        print("[!] Critical Anomaly Detected! Initiating automated response...")
        responder.generate_rca_report()
        responder.trigger_webhook_alert()
    else:
        print("[+] No anomalies detected. System is healthy.")
