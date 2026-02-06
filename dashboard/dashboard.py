""""""

import streamlit as st
import pandas as pd
import altair as alt
from pyathena import connect


def get_db_connection(s3_staging_dir: str, region_name: str):
    """Returns a connection to Athena."""
    return connect(
        s3_staging_dir=s3_staging_dir,
        region_name=region_name
    )


def execute_query(conn, query: str) -> pd.DataFrame:
    """Execute a query and return results as a DataFrame."""
    with conn.cursor() as cur:
        cur.execute(query)

        results = cur.fetchall()
        print(results)
        columns = [desc[0] for desc in cur.description]
        print(columns)

    return pd.DataFrame(results, columns=columns)


if __name__ == "__main__":
    # st.title("Transaction Dashboard")

    s3_staging_dir = "s3://c21-kieran-food-truck/output/"
    region_name = "eu-west-2"

    conn = get_db_connection(s3_staging_dir, region_name)

    query = "SELECT * FROM transactions LIMIT 10;"

    transaction_df = execute_query(conn, query)

    print(transaction_df)

    # transaction_df['at'] = pd.to_datetime(transaction_df['at'])

    # st.subheader("Raw Transaction Data")
    # st.dataframe(transaction_df)

    # st.subheader("Transactions Over Time")
    # line_chart = alt.Chart(transaction_df).mark_line().encode(
    #     x='at:T',
    #     y='amount:Q'
    # ).properties(
    #     width=700,
    #     height=400
    # )
    # st.altair_chart(line_chart, use_container_width=True)
