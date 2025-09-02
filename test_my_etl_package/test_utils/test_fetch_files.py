import pytest
from my_etl_package.utils import list_csv_files


@pytest.fixture
def temp_csv_directory(tmp_path):
    """
    Fixture to create a temporary directory with CSV and non-CSV files.
    """
    # Create sample CSV files
    (tmp_path / "file1.csv").write_text("a,b,c\n1,2,3")
    (tmp_path / "file2.csv").write_text("x,y,z\n4,5,6")

    # Create a non-CSV file
    (tmp_path / "notes.txt").write_text("This is a text file.")

    return tmp_path


def test_list_csv_files(temp_csv_directory):
    """
    Test that only CSV files are returned by list_csv_files.
    """
    result = list_csv_files(temp_csv_directory)
    csv_file_names = sorted([f.name for f in result])

    assert "file1.csv" in csv_file_names
    assert "file2.csv" in csv_file_names
    assert "notes.txt" not in csv_file_names
    assert len(result) == 2


def test_empty_directory(tmp_path):
    """
    Test that list_csv_files returns an empty list for an empty directory.
    """
    result = list_csv_files(tmp_path)
    assert result == []
