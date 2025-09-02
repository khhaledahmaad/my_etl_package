import os
import pytest
from my_etl_package.utils import PostgresConnector
from unittest.mock import patch
from sqlalchemy.engine import Engine


# Connector to the database
connector = PostgresConnector()


def test_get_db_connection():
    """
    Test that PostgresConnector generates the correct SQLAlchemy engine
    when all required environment variables are present.
    """
    # Load env vars from the connector
    ENV_VARS = {
        "DB_HOST": connector.host,
        "DB_NAME": connector.database,
        "DB_USER": connector.user,
        "DB_PASSWORD": connector.password,
        "DB_PORT": connector.port,
    }

    with patch.dict(os.environ, ENV_VARS):
        engine = connector.get_db_connection()

        # Assert type
        assert isinstance(engine, Engine)

        # Assert connection string
        actual = engine.url.render_as_string(hide_password=False)
        expected = f"postgresql://{connector.user}:{connector.password}@{connector.host}:{connector.port}/{connector.database}"
        assert actual == expected


def test_missing_environment_variables():
    """
    Test that PostgresConnector raises a ValueError when required
    environment variables are missing.
    """
    incomplete_env = {
        "DB_HOST": "localhost",
        "DB_USER": "test_user",
        # Missing DB_NAME and DB_PASSWORD
    }

    with patch.dict(os.environ, incomplete_env, clear=True):
        with pytest.raises(ValueError, match="Missing database connection details"):
            PostgresConnector().get_db_connection()


@pytest.mark.xfail(
    reason="Expected to fail if no real PostgreSQL DB is running", strict=False
)
def test_get_db_connection_real_db():
    # Sample invalid credentials for database
    ENV_VARS = {
        "DB_HOST": "localhost",
        "DB_NAME": "test_db",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_pass",
        "DB_PORT": "5432",
    }

    os.environ.update(ENV_VARS)
    connector = PostgresConnector()
    engine = connector.get_db_connection()

    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        assert result.scalar() == 1
