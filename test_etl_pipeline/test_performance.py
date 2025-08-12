import pytest
import pandas as pd
from etl_pipeline import read_csv, transform_data, write_csv, load_to_db
from etl_pipeline.utils import PostgresConnector, list_csv_files


# def test_performance(benchmark, tmp_path):
#     """
#     Benchmark test for list_csv_files with a large number of files.
#     """
#     # Create tmp files
#     num_files = 1000
#     for i in range(num_files):
#         (tmp_path / f"file_{i}.csv").write_text("col1,col2\n1,2")
#         (tmp_path / f"doc_{i}.txt").write_text("not a csv")

#     # Run bechmark on list_csv_files func
#     @benchmark
#     def test_list_csv_files():
#         result = list_csv_files(tmp_path)
#         assert all(f.suffix == ".csv" for f in result)
#         assert len(result) == num_files


@pytest.mark.benchmark
def test_full_etl_pipeline_with_list_csv_benchmark(benchmark, tmp_path):
    """
    Benchmark the full ETL pipeline including:
    - Generating CSV files
    - Listing them
    - Reading and transforming
    - Writing to new CSV
    - Loading into DB
    """

    # Setup: Create multiple CSV files
    num_files = 5
    for i in range(num_files):
        df = pd.DataFrame(
            {"col1": range(1000), "col2": range(1000, 2000), "col3": [None] * 1000}
        )
        df.to_csv(tmp_path / f"sample_{i}.csv", index=False)

    output_file = tmp_path / "output.csv"

    def run_etl():
        file_paths = list_csv_files(tmp_path)
        dfs = (read_csv(f) for f in file_paths)
        transformed_df = transform_data(dfs)
        write_csv(transformed_df, output_file)
        engine = PostgresConnector().get_db_connection()
        load_to_db(transformed_df, "test_etl_table", engine)

    # Run the benchmark
    benchmark(run_etl)

    # tmp_path handles teardown automatically
