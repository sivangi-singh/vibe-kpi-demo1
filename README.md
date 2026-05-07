# Applied Analytics Mini Project

A beginner-friendly analytics project demonstrating ETL, KPI calculation, and SQL injection protection.

## Project Structure
```
vibe-kpi-demo/
├── data/
│   ├── raw/
│   │   └── customers_raw.csv      # Raw customer data
│   └── db/
│       └── analytics.db           # SQLite database
├── src/
│   ├── etl_load_sqlite.py        # ETL script to load CSV to DB
│   └── kpi_city.py               # KPI calculation with SQL protection
├── tests/
│   └── test_kpi_city.py          # Pytest tests
├── requirements.txt              # Python dependencies
└── .gitignore                     # Git ignore file
```

## Setup Commands

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run ETL Script (Load CSV to SQLite)
```bash
python src/etl_load_sqlite.py
```

### 3. Run KPI Script
```bash
python src/kpi_city.py
```

### 4. Run Tests
```bash
pytest tests/
```

## File Descriptions
- **data/raw/customers_raw.csv**: Sample customer data with 12 rows across 4 cities
- **src/etl_load_sqlite.py**: Loads CSV data into SQLite database
- **src/kpi_city.py**: Calculates city-specific KPIs with SQL injection protection
- **tests/test_kpi_city.py**: Unit tests for KPI functionality
- **requirements.txt**: Python dependencies (pandas, pytest)
- **.gitignore**: Ignores virtual environment, cache, and database files