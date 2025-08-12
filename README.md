# my_etl_package

A Python package for building and managing ETL (Extract, Transform, Load) pipelines.

## Features

- Extract data from various sources
- Transform data using customizable steps
- Load data into target destinations
- Modular and extensible design

## Installation

```bash
pip install my_etl_package
```

## Usage

```python
from my_etl_package import ETLPipeline

pipeline = ETLPipeline(
    extractors=[...],
    transformers=[...],
    loaders=[...]
)
pipeline.run()
```

## Documentation

See the [docs](docs/) directory for detailed usage and API reference.

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.