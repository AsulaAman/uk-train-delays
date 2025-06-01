import psycopg2
import os


def load_punctuality_to_postgres():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="uk_trains",
        host="postgres",
        user="asulaaman",
        password="project2025",
        port="5432"  # Default PostgreSQL port
    )
    cursor = conn.cursor()

    # Open the cleaned CSV file
    csv_file_path = os.path.join("data", "processed", "punctuality_avg_cleaned.csv")
    with open(csv_file_path, 'r') as f:
        # Skip the header row
        next(f)

        # Use the COPY command to load data into the PostgreSQL table
        cursor.copy_from(f, 'punctuality', sep=',', columns=(
            'operator', 'financial_period',  'number_of_stops', 'on_time_percentage'
        ))
    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Data loaded successfully!")

if __name__ == "__main__":
    load_punctuality_to_postgres()
