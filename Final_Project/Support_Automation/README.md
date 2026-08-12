# Support Operations Automation: Incident Responder

This project is a Technical Support Engineering tool designed to automate log analysis and incident response (TSE/CSE workflow).

## Overview
Technical Support Engineers (TSEs) frequently deal with production outages. This tool simulates an automated **Level 3 Support** workflow:
1. **Log Ingestion:** Uses Regex to parse standard Nginx/Apache logs.
2. **Anomaly Detection:** Identifies traffic spikes, DDoS attempts (429 HTTP codes), and backend crashes (5xx errors).
3. **Automated Root Cause Analysis (RCA):** Generates a Markdown document summarizing the outage.
4. **Alerting:** Simulates a webhook payload dispatch to an external system like Slack, PagerDuty, or Jira.

## How to use
1. Run `python generate_mock_logs.py` to create a fake 5000-line server log that includes a simulated brute-force attack from a specific IP.
2. Run `python log_analyzer.py` to parse the logs, detect the attack, and auto-generate the `RCA_Report.md`.
