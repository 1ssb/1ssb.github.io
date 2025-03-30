import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Configuration from environment variables (set these as GitHub Secrets)
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Automated Analytics Report")

# Path to your analytics CSV file
DATA_FILE = "analytics.csv"

def load_data(file_path=DATA_FILE):
    try:
        df = pd.read_csv(file_path, parse_dates=['timestamp'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def filter_last_5_minutes(df):
    """
    For testing, filter data from the past 5 minutes.
    In production, you might filter by week.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(minutes=5)
    return df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]

def compose_report_body(df):
    body = "Automated Analytics Report\n\n"
    if df.empty:
        body += "No data available for the past 5 minutes.\n"
        return body

    # Example aggregation: total visits (assumes a 'visits' column; adjust as needed)
    total_visits = df['visits'].sum() if 'visits' in df.columns else len(df)
    body += f"Total visits in the last 5 minutes: {total_visits}\n"
    
    # You can add more granular details here (e.g., country, device, etc.)
    return body

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    df = load_data()
    filtered_data = filter_last_5_minutes(df)
    report_body = compose_report_body(filtered_data)
    print(report_body)  # For logging purposes
    send_email(EMAIL_SUBJECT, report_body)

if __name__ == "__main__":
    main()
