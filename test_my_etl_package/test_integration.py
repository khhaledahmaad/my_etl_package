import pytest
import pandas as pd
from sqlalchemy import text
from my_etl_package.utils import PostgresConnector
from my_etl_package.read_data import read_csv
from my_etl_package.write_data import write_csv
from my_etl_package import load_to_db


@pytest.fixture
def test_data():
    # Sample test DataFrame
    return pd.DataFrame({"a": [1, 2], "b": [3, 4]})


@pytest.fixture
def db_connection():
    # Get database connection string from custom connector
    return PostgresConnector().get_db_connection()


@pytest.fixture(scope="function", autouse=True)
def teardown_table(db_connection):
    # Cleanup fixture to drop the test table after each test
    yield  # Run the following test first
    engine = db_connection
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS test_table"))
    engine.dispose()


def test_etl_pipeline_integration(tmp_path, test_data, db_connection):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    table_name = "test_table"

    # Save input DataFrame to CSV file
    test_data.to_csv(input_file, index=False)

    # Read CSV file into DataFrame using read_csv
    read_df = read_csv(input_file)

    # Write DataFrame back to CSV file using write_csv
    write_csv(read_df, output_file)

    # Load DataFrame into database table using load_to_db
    load_to_db(read_df, table_name, db_connection)

    # Read back the CSV written by write_csv
    written_df = read_csv(output_file)

    # Create engine and read table from database for validation
    engine = db_connection
    db_df = pd.read_sql_table(table_name, db_connection)
    engine.dispose()

    # Assert DataFrames are equal to ensure data integrity across ETL pipeline
    pd.testing.assert_frame_equal(read_df, written_df)
    pd.testing.assert_frame_equal(read_df, db_df)
