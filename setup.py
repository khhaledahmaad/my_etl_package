from setuptools import setup, find_packages

setup(
    name="etl_pipeline",
    version="0.1.0",
    description="A package for ETL pipeline operations",
    author="Khaled Ahmed",
    author_email="khhaledahmaad@gmail.com",
    packages=find_packages(include=["etl_pipeline", "etl_pipeline.*"]),
    python_requires=">=3.10",
    install_requires=[
        "python-dotenv",
        "numpy",
        "pandas",
        "sqlalchemy",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Build Packages",
        "Topic :: ETL",
    ],
)
