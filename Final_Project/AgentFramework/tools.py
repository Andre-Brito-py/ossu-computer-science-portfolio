import os
import requests
import smtplib
from email.mime.text import MIMEText

# Real Tools for Autonomous Agent
# Requires Environment Variables to run correctly.

def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email using SMTP."""
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    
    if not smtp_user or not smtp_pass:
        return "[Error] SMTP credentials missing in environment variables."
        
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            
        return f"[Success] Email sent to {to_email}"
    except Exception as e:
        return f"[Error] Failed to send email: {str(e)}"

def generate_boleto(customer_cpf: str, value: float, due_date: str) -> str:
    """
    Generate a bank slip (Boleto) using the Asaas API.
    Asaas is a popular Brazilian payment gateway.
    """
    api_key = os.environ.get("ASAAS_API_KEY")
    if not api_key:
        return "[Error] ASAAS_API_KEY missing in environment variables."
        
    # Asaas sandbox URL
    url = "https://sandbox.asaas.com/api/v3/payments"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": api_key
    }
    
    # In a real scenario, you first need to query or create the customer to get their internal Asaas ID.
    # For demonstration, we assume customer_cpf is the customer internal ID 'cus_00000503'
    payload = {
        "billingType": "BOLETO",
        "customer": customer_cpf,
        "value": value,
        "dueDate": due_date,
        "description": "Fatura gerada via Agente Autônomo."
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        invoice_url = data.get("invoiceUrl", "URL não encontrada")
        return f"[Success] Boleto gerado com sucesso. Link: {invoice_url}"
    except requests.exceptions.RequestException as e:
        return f"[Error] Falha na API do banco: {str(e)}"

# Dictionary mapping tool names to python functions
AVAILABLE_TOOLS = {
    "send_email": send_email,
    "generate_boleto": generate_boleto
}
