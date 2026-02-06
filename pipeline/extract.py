"""File to extract data from RDS and store it locally."""

from os import environ as ENV, makedirs, path
from dotenv import load_dotenv
from pymysql import connect, Connection, Error
import pandas as pd


def get_db_connection() -> Connection:
    """Return database connection."""
    try:
        conn = connect(
            host=ENV["DB_HOST"],
            port=int(ENV["DB_PORT"]),
            database=ENV["DB_NAME"],
            user=ENV["DB_USER"],
            password=ENV["DB_PASSWORD"]
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def extract_data(conn: Connection, table_name: str) -> pd.DataFrame:
    """Return data from specified table as DataFrame."""
    query = f"SELECT * FROM `{table_name}`"

    with conn.cursor() as cursor:
        cursor.execute(query)

        df = pd.DataFrame(
            cursor.fetchall(),
            columns=[desc[0] for desc in cursor.description]
        )

    return df


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save DataFrame to a CSV file."""

    folder = path.dirname(file_path)
    if not path.exists(folder):
        makedirs(folder)

    df.to_csv(file_path, index=False)


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_connection()

    if conn:
        df = extract_data(conn, "DIM_Truck")
        save_data(df, "./clean_data/DIM_Truck.csv")

        df = extract_data(conn, "FACT_Transaction")
        save_data(df, "./raw_data/FACT_Transaction.csv")

        df = extract_data(conn, "DIM_Payment_Method")
        save_data(df, "./clean_data/DIM_Payment_Method.csv")

    conn.close()
