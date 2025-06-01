import os
import pandas as pd

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def clean_train_delays_data():
    file_path = os.path.join(RAW_DATA_DIR, "train_delays.csv")
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Please download the data first.")
        return

    print(f"Processing file: {file_path}...")

    # Read the CSV file with header
    df = pd.read_csv(file_path, header=0)


    # Rename columns to match the database schema
    column_rename={
        'time period': 'date',
        'train operating company name': 'toc_name',
        'NR on TOC External': 'nr_on_toc_external',
        'NR on TOC Non Track Assets': 'nr_on_toc_non_track_assets',
        'NR on TOC Severe Weather': 'nr_on_toc_severe_weather',
        'NR on TOC Track': 'nr_on_toc_track',
        'TOC on Self Fleet': 'toc_on_self_fleet',
        'TOC on Self Operations': 'toc_on_self_operations',
        'TOC on Self Traincrew': 'toc_on_self_traincrew',
        'TOC on TOC Fleet': 'toc_on_toc_fleet',
        'TOC on TOC Operations': 'toc_on_toc_operations',
        'TOC on TOC Traincrew': 'toc_on_toc_traincrew'
        }
    df.rename(columns=column_rename, inplace=True)

    # Convert all columns except 'toc_name' and 'date' to numeric
    numeric_columns = [
        col for col in column_rename.values()
        if col not in ['toc_name', 'date']
    ]

    # Convert numeric columns to numeric types, fill NaN with 0 and round values
    df[numeric_columns] = (
        df[numeric_columns]
        .apply(pd.to_numeric, errors='coerce')
        .fillna(0)
        .round(0)
        .astype(int)
    )

    # Save the cleaned data to a new CSV file
    output_path = os.path.join(PROCESSED_DATA_DIR, "train_delays_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned train delays data saved to {output_path}")


def clean_punctuality_data():
    file_path = os.path.join(RAW_DATA_DIR, "punctuality.csv")

    # Read the CSV file with header
    df = pd.read_csv(file_path, header=0)

    # Drop rows with all NaN values
    df = df.dropna(subset=['operator'])

    # Clean the 'number_of_stops' column
    df['number_of_stops'] = df['number_of_stops'].replace({',': ''}, regex=True).astype(int)


    # Save the cleaned data to a new CSV file
    output_path = os.path.join(PROCESSED_DATA_DIR, "punctuality_avg_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned punctuality data saved to {output_path}")


def clean_cancellation_data():
    file_path = os.path.join(RAW_DATA_DIR, "cancellations.csv")

    df = pd.read_csv(file_path, skiprows=4)
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')

    # Confirm structure of data
    print("Columns in cancellation data:", df.columns)
    print(df.head())


    df.columns = df.columns.str.strip().str.lower()
    df.drop_duplicates(inplace=True)

    # Specify starting year from 'financial_period_key'
    df['start_year'] = df['financial_period_key'].str.extract(r'(\d{4})')[0].astype(int)

    # Filter out rows starting in 2025, 2024, 2023, and 2022
    df = df[df['start_year'].isin([2022, 2023, 2024, 2025])]

    # Drop the 'start_year' column after filtering
    df.drop(columns=['start_year'], inplace=True)

    output_path = os.path.join(PROCESSED_DATA_DIR, "cancellation_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned cancellation data saved to {output_path}")

def transform_data():
    clean_train_delays_data()
    clean_punctuality_data()
    clean_cancellation_data()
    print("Data transformation completed.")

if __name__ == "__main__":
    transform_data()
    print("Data transformation script executed.")
