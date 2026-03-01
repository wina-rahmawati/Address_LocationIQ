# Address_LocationIQ
This project is an Apache Airflow pipeline that processes project address data from JSON files, cleans and standardizes addresses, enriches them using a geocoding service, and writes the enriched result back to a JSON output file.

project-root/
│
├── dags/
│ └── address_enrichment_dag.py
│
├── data/
│ ├── int_test_input
│ │ └── input_sample.json
│ ├── int_test_output
│ │ └── output.json
│
├── src/
│ ├── integrations/
│ │ └── geocode_util.py
│ ├── transformers/
│ │ └── address_transformer.py
│ │ └── abbreviation.txt
│
│ ├── utils/
│ │ └── reader.py
│ │ └── writer.py
│
├── docker-compose.yaml
├── .env
└── README.md
