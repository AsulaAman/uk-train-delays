import pandas as pd
import psycopg2

# This script connects to a PostgreSQL database and loads cleaned CSV data into a specified table.
def load_cancellations_to_postgres():
    # Load the cleaned CSV file
    df = pd.read_csv('data/processed/cancellations_cleaned.csv')

    # Remove incomplete rows
    df = df[df['national_or_operator'].notnull()]

    # Remove the first tow if it contains a header
    df = df[df['textbox22'] != 'Periodic cancellations score']

    # Check if the data is loaded correctly
    print(f"Rows after cleaning: {len(df)}")


    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="uk_trains",
        host="postgres",
        user="asulaaman",
        password="project2025",
        port="5432"  # Default PostgreSQL port
    )
    cursor = conn.cursor()

    # Load the data into the PostgreSQL table
    for index, row in df.iterrows():
        try:
            cursor.execute("""
            INSERT INTO train_delays (toc_name, date, total_trains, partially_cancelled, cancellation_count, cancellation_score, cancellation_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['national_or_operator'],
                row['financial_period_key'],
                int(str(row['trains_planned']).replace(',', '') or 0),
                int(str(row['trains_part_cancelled1']).replace(',', '') or 0),
                int(str(row['trains_full_cancelled']).replace(',', '') or 0),
                float(str(row['cancellation_score__number_']).replace(',', '') or 0),
                float(str(row['percent_cancelled_periodic']).replace(',', '') or 0),
            ))
        except Exception as e:
            print(f"Error inserting row {index}: {e}")
            conn.rollback()
        else:
            conn.commit()

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_cancellations_to_postgres()
