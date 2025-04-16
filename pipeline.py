import requests
import os
import json
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
from google.api_core.exceptions import NotFound, Conflict
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Step 1: Fetch crypto data from API
def fetch_crypto_data():
    url = "https://coinranking1.p.rapidapi.com/coins"
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open("crypto_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Crypto data fetched and saved to crypto_data.json")
    else:
        print(f"❌ Error fetching data: {response.status_code}")
        print(response.text)
        raise Exception("Failed to fetch crypto data")

# Step 2: Transform JSON data to DataFrame and save as CSV
def transform_data():
    with open("crypto_data.json", "r") as f:
        data = json.load(f)

    coins = data["data"]["coins"]
    df = pd.DataFrame(coins)

    # Add timestamp for Looker Studio (using UTC-aware datetime)
    df["fetched_at"] = datetime.now(timezone.utc).isoformat()

    # Select relevant columns for Looker Studio
    df = df[[
        "uuid", "symbol", "name", "price", "marketCap", "change", "rank", "24hVolume", "fetched_at"
    ]]

    # Convert numeric columns to string to avoid pyarrow errors in BigQuery
    df["price"] = df["price"].astype(str)
    df["marketCap"] = df["marketCap"].astype(str)
    df["change"] = df["change"].astype(str)
    df["24hVolume"] = df["24hVolume"].astype(str)

    # Ensure that the 'fetched_at' column is a string (it's a timestamp)
    df["fetched_at"] = df["fetched_at"].astype(str)

    # Save to CSV for local review if needed
    df.to_csv("crypto_data.csv", index=False)
    print("✅ Data transformed and saved to crypto_data.csv")
    return df

# Step 3: Upload DataFrame to BigQuery (with dataset creation if necessary)
def upload_to_bigquery(df):
    client = bigquery.Client.from_service_account_json("keys/service_account_key.json")
    dataset_id = "rock-bonus-452311-h8"  # Your project ID
    dataset_name = "crypto_data"  # Your dataset name
    table_id = f"{dataset_id}.{dataset_name}"

    # Check if the dataset exists, create it if not
    try:
        client.get_dataset(f"{dataset_id}.{dataset_name}")  # Try fetching the dataset
        print(f"✅ Dataset {dataset_id}.{dataset_name} already exists.")
    except NotFound:
        print(f"❌ Dataset {dataset_id}.{dataset_name} not found. Creating it...")
        dataset = bigquery.Dataset(f"{dataset_id}.{dataset_name}")
        dataset = client.create_dataset(dataset)  # Create the dataset
        print(f"✅ Dataset {dataset_id}.{dataset_name} created.")
    except Conflict:
        print(f"❌ Dataset {dataset_id}.{dataset_name} already exists. Skipping creation.")

    # Upload DataFrame to BigQuery
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Wait for job to complete
    print("✅ Data uploaded to BigQuery!")

def main():
    fetch_crypto_data()
    df = transform_data()
    upload_to_bigquery(df)

if __name__ == "__main__":
    main()
