# 🪙 Real-Time Crypto Market Dashboard

This is a real-time cryptocurrency analytics pipeline that collects live data from the [Coinranking API](https://coinranking.com), processes it using Python, stores it in **Google BigQuery**, and visualizes trends through an interactive **Looker Studio dashboard**.

## 🚀 Features
- 🔄 Daily crypto data collection via API
- 📈 Interactive Looker Studio dashboard with time-based trends
- ☁️ Automated data uploads to BigQuery using service accounts
- 💰 Market Cap, Volume, and Rank analysis for Top Cryptos

## 🛠️ Tech Stack
- **Python** (requests, pandas)
- **BigQuery** (via Google Cloud Client)
- **Looker Studio**
- **Coinranking API**
- **Service Account Authentication**

## 📊 Dashboard Highlights
- **Top 10 Cryptos by Rank Over Time**
- **Volatility Over Time (Price Change)**
- **Correlation Between Price and 24h Volume**
- **Market Share**
- **Market Cap & Volume Visualizations**
- **Interactive Filters by Symbol & Date**
- **Live Data Ingestion Timestamps**

## 📊 Dashboard Preview

> ** [Real-Time Crypto Market Dashboard](https://lookerstudio.google.com/s/u082dTM6sAQ)

![Dashboard Preview]
![Real-Time Crypto Market Dashboard](https://github.com/user-attachments/assets/0fd976d0-e12d-42dd-89e1-4a1bc61f7b27)

---

## 📁 Folder Structure
crypto-pulse/
├── data/
│   ├── crypto_data.csv
│   └── crypto_data.json
├── keys/
│   └── service_account_key.json  (add this to .gitignore)
├── pipeline.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md

