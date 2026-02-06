"""File for loading transaction data into the database."""

from os import environ as ENV, _Environ
from dotenv import load_dotenv

from boto3 import Session
import pandas as pd
import awswrangler as wr


def get_s3_session(config: _Environ) -> Session:
    """Returns a live S3 session."""

    return Session(
        aws_access_key_id=config["AWS_ACCESS_KEY"],
        aws_secret_access_key=config["AWS_SECRET_KEY"]
    )


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a DataFrame."""

    return pd.read_csv(file_path)


def upload_transaction_data(s3: Session,
                            s3_bucket: str,
                            transaction_df: pd.DataFrame,
                            truck_df: pd.DataFrame,
                            payment_method_df: pd.DataFrame) -> None:
    """Uploads transaction data to the database."""

    transaction_df['at'] = pd.to_datetime(transaction_df['at'])
    transaction_df['year'] = transaction_df['at'].dt.year
    transaction_df['month'] = transaction_df['at'].dt.month
    transaction_df['day'] = transaction_df['at'].dt.day
    transaction_df["hour"] = transaction_df['at'].dt.hour

    wr.s3.to_parquet(
        df=transaction_df,
        boto3_session=s3,
        path=f"s3://{s3_bucket}/transactions/",
        dataset=True,
        partition_cols=['year', 'month', 'day', 'hour']
    )

    wr.s3.to_parquet(
        df=truck_df,
        boto3_session=s3,
        path=f"s3://{s3_bucket}/dim_truck/",
        dataset=True
    )

    wr.s3.to_parquet(
        df=payment_method_df,
        boto3_session=s3,
        path=f"s3://{s3_bucket}/dim_payment_method/",
        dataset=True
    )


if __name__ == "__main__":

    load_dotenv()

    s3 = get_s3_session(ENV)
    s3_bucket = "c21-kieran-food-truck/input"

    payment_method_df = load_data("clean_data/DIM_Payment_Method.csv")
    truck_df = load_data("clean_data/DIM_Truck.csv")
    transaction_df = load_data("clean_data/FACT_Transaction.csv")

    upload_transaction_data(s3,
                            s3_bucket,
                            transaction_df,
                            truck_df,
                            payment_method_df)
