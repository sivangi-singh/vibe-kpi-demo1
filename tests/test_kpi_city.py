import pytest
import sqlite3
import pandas as pd
import os
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from kpi_city import city_kpi

@pytest.fixture
def setup_test_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'db', 'test_analytics.db')
    
    test_data = [
        (1, 'Mumbai', 2500.50, 0),
        (2, 'Mumbai', 3200.00, 1),
        (3, 'Delhi', 1800.75, 0),
        (4, 'Mumbai', 2800.75, 0)
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS customers_raw")
    cursor.execute("""
        CREATE TABLE customers_raw (
            customer_id INTEGER,
            city TEXT,
            monthly_spend REAL,
            churned INTEGER
        )
    """)
    cursor.executemany("INSERT INTO customers_raw VALUES (?, ?, ?, ?)", test_data)
    conn.commit()
    conn.close()
    
    yield db_path
    
    try:
        os.remove(db_path)
    except PermissionError:
        pass  # File might be locked by Windows

def test_city_kpi_happy_path(setup_test_db):
    captured_output = StringIO()
    
    with patch('builtins.print', new=lambda *args: captured_output.write(' '.join(map(str, args)) + '\n')):
        with patch('kpi_city.os.path.join') as mock_path:
            mock_path.return_value = setup_test_db
            
            city_kpi("Mumbai")
            
            output = captured_output.getvalue()
            assert "KPI for Mumbai:" in output
            assert "Total Customers: 3" in output
            assert "Churn Rate:" in output

def test_city_kpi_sql_injection_attempt(setup_test_db):
    captured_output = StringIO()
    
    with patch('builtins.print', new=lambda *args: captured_output.write(' '.join(map(str, args)) + '\n')):
        with patch('kpi_city.os.path.join') as mock_path:
            mock_path.return_value = setup_test_db
            
            city_kpi("Mumbai' OR 1=1 --")
            
            output = captured_output.getvalue()
            assert "No data found for city: Mumbai' OR 1=1 --" in output

def test_city_kpi_nonexistent_city(setup_test_db):
    captured_output = StringIO()
    
    with patch('builtins.print', new=lambda *args: captured_output.write(' '.join(map(str, args)) + '\n')):
        with patch('kpi_city.os.path.join') as mock_path:
            mock_path.return_value = setup_test_db
            
            city_kpi("NonexistentCity")
            
            output = captured_output.getvalue()
            assert "No data found for city: NonexistentCity" in output
