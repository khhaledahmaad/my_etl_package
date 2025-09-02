import logging
from pathlib import Path
from dotenv import load_dotenv
from my_etl_package.utils import list_csv_files, PostgresConnector
from my_etl_package import read_csv, transform_data, write_csv, load_to_db

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()
logging.info("Environment variables loaded.")

# Set up workspace
base = Path().absolute() / "data"
input_directory = base / "raw"
output_directory = base / "processed"
output_filename = "etl_pipeline_processed.csv"
output_path = output_directory / output_filename

# Create output directory if it doesn't exist
output_directory.mkdir(exist_ok=True)
logging.info(f"Output directory set to: {output_directory}")


def main():
    logging.info("Starting ETL pipeline...")

    # Configuration
    table_name = "etl_pipeline_processed"
    engine = PostgresConnector().get_db_connection()
    logging.info(f"Using table: {table_name}")

    # Extract
    logging.info(f"Looking for CSV files in: {input_directory}")
    file_paths = list_csv_files(input_directory)
    logging.info(f"Found {len(file_paths)} CSV files.")

    # Read
    dfs = (read_csv(f) for f in file_paths)

    # Transform
    logging.info("Transforming data...")
    combined_df = transform_data(dfs)
    logging.info("Data transformation complete.")

    # Load - write to CSV
    logging.info("Writing processed data to CSV...")
    write_csv(combined_df, output_path)
    logging.info("Data written to CSV.")

    # Load - load into Postgres
    logging.info("Loading data into PostgreSQL...")
    load_to_db(combined_df, table_name, engine)
    logging.info("Data successfully loaded into PostgreSQL.")

    logging.info("ETL pipeline finished.")


if __name__ == "__main__":
    main()
