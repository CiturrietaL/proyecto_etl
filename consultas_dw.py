import sqlite3
import pandas as pd

# Conectar a la base de datos DW
conn = sqlite3.connect('etl_proyecto.db')

# ==========================================
# Consulta 1: Total de clientes
print("🔎 Total de clientes")
query = "SELECT COUNT(*) AS total_clientes FROM Dim_Customers"
df = pd.read_sql(query, conn)
print(df)

# ==========================================
# Consulta 2: Total de cuentas
print("\n🔎 Total de cuentas")
query = "SELECT COUNT(*) AS total_cuentas FROM Dim_Accounts"
df = pd.read_sql(query, conn)
print(df)

# ==========================================
# Consulta 3: Total de transacciones
print("\n🔎 Total de transacciones")
query = "SELECT COUNT(*) AS total_transacciones FROM Fact_Transactions"
df = pd.read_sql(query, conn)
print(df)

# ==========================================
# Consulta 4: Promedio, mínimo, máximo y desviación estándar del límite de cuentas
print("\n🔎 Estadísticas de límites de cuentas")
query = """
SELECT 
    ROUND(AVG(limit),2) AS promedio,
    MIN(limit) AS minimo,
    MAX(limit) AS maximo,
    ROUND(STDDEV(limit),2) AS desviacion
FROM Dim_Accounts
"""
# NOTA: Como Dim_Accounts no tiene el campo limit aún (no fue cargado), por ahora esta consulta se omite o reemplaza.
# Aquí solo como estructura de ejemplo si deseas agregar limit después.

# ==========================================
# Consulta 5: Top 5 cuentas con más transacciones
print("\n🔎 Top 5 cuentas con más transacciones")
query = """
SELECT account_id, COUNT(*) AS total_transacciones
FROM Fact_Transactions
GROUP BY account_id
ORDER BY total_transacciones DESC
LIMIT 5
"""
df = pd.read_sql(query, conn)
print(df)

# ==========================================
# Consulta 6: Top 5 clientes con más cuentas
print("\n🔎 Top 5 clientes con más cuentas")
query = """
SELECT customer_id, COUNT(*) AS total_cuentas
FROM Dim_Accounts
GROUP BY customer_id
ORDER BY total_cuentas DESC
LIMIT 5
"""
df = pd.read_sql(query, conn)
print(df)

# ==========================================
# Cerrar conexión
conn.close()
