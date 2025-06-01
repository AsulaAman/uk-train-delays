import pandas as pd
import psycopg2
import traceback

def load_train_delays_to_postgres():
    print("Loading data to PostgreSQL...")
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="uk_trains",
        host="postgres",
        user="asulaaman",
        password="project2025",
        port="5432"  # Default PostgreSQL port
    )
    cursor = conn.cursor()

    # Oppen the CSV file
    df = pd.read_csv('data/raw/train_delays.csv')

        # Load the data into the PostgreSQL table
    for index, row in df.iterrows():
        print(f"Inserting row {index}...")
        try:
            cursor.execute("""
                INSERT INTO train_delays (
                    toc_name,
                    date,
                    nr_on_toc_external,
                    nr_on_toc_non_track_assets,
                    nr_on_toc_severe_weather,
                    nr_on_toc_track,
                    toc_on_self_fleet,
                    toc_on_self_operations,
                    toc_on_self_traincrew,
                    toc_on_toc_fleet,
                    toc_on_toc_operations,
                    toc_on_toc_traincrew
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['toc_name'],
                row['date'],
                round(row['nr_on_toc_external']),
                round(row['nr_on_toc_non_track_assets']),
                round(row['nr_on_toc_severe_weather']),
                round(row['nr_on_toc_track']),
                round(row['toc_on_self_fleet']),
                round(row['toc_on_self_operations']),
                round(row['toc_on_self_traincrew']),
                round(row['toc_on_toc_fleet']),
                round(row['toc_on_toc_operations']),
                round(row['toc_on_toc_traincrew']),
            ))
        except Exception as e:
            print(f"Error inserting row {index}: {e}")
            traceback.print_exc()
            conn.rollback()
        else:
            conn.commit()

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Data loaded successfully!")

if __name__ == "__main__":
    load_train_delays_to_postgres()
