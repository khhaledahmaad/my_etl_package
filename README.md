# My ETL Package

This package implements a simple **Extract–Transform–Load (ETL)** pipeline using Python.  
It processes CSV files from an input directory, transforms and integrate them into a single dataset, saves the results to an output directory, and loads the final dataset into a PostgreSQL database.

---
## 🔑 Pre-requisites

1. **Working Python environment**  
   Make sure you have a working Python environment set up, either locally or in Jupyter.  
   If you haven’t already, follow this guide:  
   [Setting up a Basic Python Development Environment](https://medium.com/@khhaledahmaad/setting-up-a-basic-python-development-environment-fd67e749825e)

2. **PostgreSQL database**  
   Ensure you have a PostgreSQL database installed and configured.  
   If you don’t have one already, download and install both PostgreSQL and PgAdmin from the official sources below, then use PgAdmin to create your first database:

   - [Download PostgreSQL](https://www.postgresql.org/download/)  
   - [Download PgAdmin](https://www.pgadmin.org/download/)  

   Once installed, you can follow this step-by-step guide to create a new database in PgAdmin:  
   [Creating a Database using PgAdmin](https://www.tutorialsteacher.com/postgresql/create-database)

---

## 📦 Installation

Install directly from **PyPI**:

```bash
pip install my-etl-package
````

Set up your environment variables in a `.env` file (required for PostgreSQL connection):

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
```

---

## ⚙️ Package Contents

After installation, you can inspect the available functions:

```python
import my_etl_package
help(my_etl_package)
```

Typical contents:

```
NAME
    my_etl_package

PACKAGE CONTENTS
    utils

FUNCTIONS
    read_csv(file_path: pathlib.Path) -> pandas.DataFrame
    transform_data(dfs: List[pandas.DataFrame]) -> pandas.DataFrame
    write_csv(df: pandas.DataFrame, output_path: pathlib.Path) -> None
    load_to_db(df: pd.DataFrame, table_name: str, engine: sqlalchemy.engine.Engine) -> None
```

Utilities inside `my_etl_package.utils`:

```
FUNCTIONS
    list_csv_files(directory_path: pathlib.Path) -> List[pathlib.Path]
    PostgresConnector().get_db_connection() -> sqlalchemy.engine.Engine
```

---

## 📂 Data Directory Structure (Recommended but not Mandatory)

When running locally, organize your data as follows (relative to your **current working directory**):

```
pwd/
├── .env              # Environment variables (PostgreSQL credentials)
└── data/
    ├── raw/          # Place input CSV files here
    └── processed/    # Processed output CSVs will be written here
```

---

## 🛠️ Usage

### 1. Use Methods Individually

#### List all CSV files in a directory

```python
from pathlib import Path
from my_etl_package.utils import list_csv_files

input_directory = Path().absolute() / "data/raw"  # or any other directory you stored your input files as a pathlib.Path object
files = list_csv_files(input_directory)
print(files)
```

#### Read a CSV file

```python
from my_etl_package import read_csv

df = read_csv(Path().absolute() / "data/test/sample.csv")
print(df.head())
```

#### Transform multiple CSVs

```python
from my_etl_package import transform_data, read_csv

csv_files = [Path().absolute() / "data/raw/file1.csv", Path().absolute() / "data/raw/file2.csv"]
dfs = (read_csv(f) for f in csv_files)
combined_df = transform_data(dfs)
print(combined_df.head())
```

#### Write processed DataFrame to CSV

```python
from pathlib import Path
from my_etl_package import write_csv

output_path = Path().absolute() / "data/processed/processed.csv")
write_csv(combined_df, output_path)
```

#### Load DataFrame into PostgreSQL

```python
from my_etl_package.utils import PostgresConnector
from my_etl_package import load_to_db


# Load environment variables
load_dotenv()

# If .env is in a different location, specify the path:
# load_dotenv('./some_other_location/.env')

engine = PostgresConnector().get_db_connection()
load_to_db(combined_df, "processed_table", engine)
```

---

### 2. Run the Full ETL Pipeline

Here’s an end-to-end pipeline script:

In `etl_pipeline.py` (name as you wish) in the current working directory ->

```python
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

```

Run it:

```bash
python etl_pipeline.py
```

---

## ✅ Features

* 🔎 Automatically detects all CSV files in `data/raw/`
* 🛠️ Cleans and transforms raw datasets
* 💾 Stores processed results in `data/processed/`
* 🗄️ Loads final output into a PostgreSQL table

---

## 📝 Notes

* Ensure PostgreSQL is running and accessible with the credentials in your `.env` file.
* Place your input CSV files in the same input directory before running the pipeline.

---