import sqlite3
import os

ALLOWED_CITIES = {'Mumbai', 'Delhi', 'Bangalore', 'Chennai'}

def city_kpi(city: str):
    if city not in ALLOWED_CITIES:
        print(f"Error: City '{city}' is not in the allowed cities list")
        print(f"Allowed cities: {', '.join(sorted(ALLOWED_CITIES))}")
        return
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'db', 'analytics.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        city,
        COUNT(*) as total_customers,
        AVG(monthly_spend) as avg_monthly_spend,
        SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) as churned_customers,
        ROUND(SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
    FROM customers_raw 
    WHERE city = ?
    GROUP BY city
    """
    
    cursor.execute(query, (city,))
    result = cursor.fetchone()
    
    if result:
        print(f"KPI for {result[0]}:")
        print(f"  Total Customers: {result[1]}")
        print(f"  Avg Monthly Spend: ${result[2]:.2f}")
        print(f"  Churned Customers: {result[3]}")
        print(f"  Churn Rate: {result[4]}%")
    else:
        print(f"No data found for city: {city}")
    
    conn.close()

if __name__ == "__main__":
    print("=== Testing with valid city ===")
    city_kpi("Mumbai")
    
    print("\n=== Testing with SQL injection attempt ===")
    city_kpi("Mumbai' OR 1=1 --")
