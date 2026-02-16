python
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage

# --- CONFIGURATION ---
API_KEY = "ko7tzgOaMrMJatcDu4mXy8B2fJyzfgUx"
EMAIL_ADDRESS = "azpaulbelt@gmail.com"
EMAIL_PASSWORD = "quhzyd-cujbuC-giwze8"

def get_big_money_targets():
    # Fetch stocks with high institutional ownership using FMP's free tier
    url = f"https://financialmodelingprep.com{API_KEY}"
    response = requests.get(url).json()
    return [stock['symbol'] for stock in response]

def create_report(tickers):
    plt.figure(figsize=(10, 6))
    for ticker in tickers:
        data = yf.download(ticker, period="3mo", interval="1d")
        plt.plot(data['Close'], label=ticker)
    
    plt.title("3-Month Performance of Big Money Targets")
    plt.legend()
    plt.savefig("report_chart.png")
    plt.close()

def send_email():
    msg = EmailMessage()
    msg['Subject'] = "Weekly Big Money Wall Street Report"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content("Attached is this week's tracking of heavy institutional activity.")
    
    with open("report_chart.png", "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename="chart.png")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# Execute
targets = get_big_money_targets()
create_report(targets)
send_email()
print("Report Sent!")