import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect('etl_proyecto.db')

# Consulta 1: Promedio, mínimo y máximo del account_limit
query1 = """
SELECT 
    ROUND(AVG(account_limit), 2) AS promedio_limite,
    MIN(account_limit) AS minimo_limite,
    MAX(account_limit) AS maximo_limite
FROM Dim_Accounts;
"""
print("\nConsulta 1:")
print(pd.read_sql(query1, conn))

# Consulta 2: Cantidad de clientes con más de una cuenta
query2 = """
SELECT 
    COUNT(*) AS cantidad_clientes_con_multiples_cuentas
FROM (
    SELECT customer_id
    FROM Dim_Accounts
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
    HAVING COUNT(account_id) > 1
) sub;
"""
print("\nConsulta 2:")
print(pd.read_sql(query2, conn))

# Consulta 3: Promedio de amount y total de transacciones
query3 = """
SELECT 
    ROUND(AVG(amount), 2) AS promedio_monto,
    SUM(amount) AS total_transacciones
FROM Fact_Transactions;
"""
print("\nConsulta 3:")
print(pd.read_sql(query3, conn))

# Consulta 4: Cuenta con mayor diferencia de montos
query4 = """
SELECT account_id, 
       ROUND(MAX(total) - MIN(total), 2) AS mayor_diferencia
FROM Fact_Transactions
GROUP BY account_id
ORDER BY mayor_diferencia DESC
LIMIT 1;
"""
print("\nConsulta 4:")
print(pd.read_sql(query4, conn))

# Consulta 5: Cuentas que tengan 3 productos (Dim_Products está vacía, por lo tanto dará siempre cero)
query5 = """
SELECT COUNT(*) AS cuentas_con_tres_productos_y_commodity
FROM (
    SELECT account_id
    FROM Dim_Products
    GROUP BY account_id
    HAVING COUNT(product) = 3 AND SUM(CASE WHEN product = 'commodity' THEN 1 ELSE 0 END) >= 1
) sub;
"""
print("\nConsulta 5:")
print(pd.read_sql(query5, conn))

# Consulta 6: Cliente con mayor cantidad de transacciones sell
query6 = """
SELECT c.name, COUNT(t.transaction_id) AS cantidad_sell
FROM Fact_Transactions t
JOIN Dim_Accounts a ON t.account_id = a.account_id
JOIN Dim_Customers c ON a.customer_id = c.customer_id
WHERE t.transaction_code = 'sell'
GROUP BY c.name
ORDER BY cantidad_sell DESC
LIMIT 1;
"""
print("\nConsulta 6:")
print(pd.read_sql(query6, conn))

# Consulta 7: Promedio total por usuario
query7 = """
SELECT c.username, ROUND(AVG(t.total), 2) AS promedio
FROM Fact_Transactions t
JOIN Dim_Accounts a ON t.account_id = a.account_id
JOIN Dim_Customers c ON a.customer_id = c.customer_id
GROUP BY c.username
ORDER BY promedio DESC
LIMIT 1;
"""
print("\nConsulta 7:")
print(pd.read_sql(query7, conn))

# Consulta 8: Promedio de buy y sell por símbolo
query8 = """
SELECT symbol, 
       ROUND(AVG(CASE WHEN transaction_code = 'buy' THEN total END), 2) AS promedio_buy,
       ROUND(AVG(CASE WHEN transaction_code = 'sell' THEN total END), 2) AS promedio_sell
FROM Fact_Transactions
GROUP BY symbol
ORDER BY symbol;
"""
print("\nConsulta 8:")
print(pd.read_sql(query8, conn))

# Consulta 9: Top 5 cuentas con más transacciones
query9 = """
SELECT account_id, COUNT(*) as cantidad_transacciones
FROM Fact_Transactions
GROUP BY account_id
ORDER BY cantidad_transacciones DESC
LIMIT 5;
"""
print("\nConsulta 9:")
print(pd.read_sql(query9, conn))

# Consulta 10: Total invertido por cliente (solo los que tienen customer_id)
query10 = """
SELECT c.customer_id, c.name, SUM(t.total) AS total_invertido
FROM Fact_Transactions t
JOIN Dim_Accounts a ON t.account_id = a.account_id
JOIN Dim_Customers c ON a.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_invertido DESC
LIMIT 10;
"""
print("\nConsulta 10:")
print(pd.read_sql(query10, conn))

# Cerrar la conexión
conn.close()
