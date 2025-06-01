import os
import requests

DATA_URLS = {
    "train_delays": "https://dataportal.orr.gov.uk/statistics/performance/passenger-rail-performance/table-3184-delay-minutes-by-operator-and-cause-periodic/",
    "punctuality": "https://dataportal.orr.gov.uk/media/3025/table-3138.csv",
    "cancellations": "https://dataportal.orr.gov.uk/media/3024/table-3124.csv",
}

RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

def download_csv(name, url):
    local_path = os.path.join(RAW_DATA_DIR, f"{name}.csv")

    # Check if the file already exists
    if os.path.exists(local_path):
        print(f"File {local_path} already exists. Skipping download.")
        return

    print(f"Downloading {name}.csv...")

    # Add error handling around the request
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {name}.csv to {local_path}")
        return local_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {name}.csv: {e}")
        return None

if __name__ == "__main__":
    for name, url in DATA_URLS.items():
        if url:
            download_csv(name, url)
        else:
            print(f"No URL provided for {name}. Skipping download.")
