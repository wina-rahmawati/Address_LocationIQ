# Address_LocationIQ
This project is an Apache Airflow pipeline that processes project address data from JSON files, cleans and standardizes addresses, enriches them using a geocoding service, and writes the enriched result back to a JSON output file.

project-root/
├── dags/
│   └── etl_dag.py             # Airflow DAG definition
├── data/
│   ├── int_test_input/        # Source JSON files
│   └── int_test_output/       # Processed JSON output
├── src/
│   ├── integrations/
│   │   └── geocode_util.py    # LocationIQ API integration
│   ├── transformers/
│   │   └── address_util.py    # Address cleaning & abbreviation logic
│   └── utils/
│       ├── reader.py          # JSON folder iterator
│       └── writer.py          # JSON file writer
├── tests/                     # Comprehensive Unit Tests
│   ├── test_reader.py
│   ├── test_geocode.py
│   └── test_writer.py
├── docker-compose.yaml        # Airflow environment setup
├── .env                       # API Keys and Path configurations
└── README.md
