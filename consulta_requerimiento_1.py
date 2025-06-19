import sqlite3
import pandas as pd

# Conectar a SQLite
conn = sqlite3.connect('etl_proyecto.db')

# Primero veamos bien qué columnas tiene la tabla Dim_Accounts
query = "PRAGMA table_info('Dim_Accounts')"
columns_df = pd.read_sql(query, conn)
print(columns_df)

# Leer datos si existe el campo 'limit'
if 'limit' in columns_df['name'].values:
    accounts_df = pd.read_sql('SELECT limit FROM Dim_Accounts', conn)

    promedio = round(accounts_df['limit'].mean(), 2)
    minimo = accounts_df['limit'].min()
    maximo = accounts_df['limit'].max()
    desviacion = round(accounts_df['limit'].std(), 2)

    print("Promedio:", promedio)
    print("Mínimo:", minimo)
    print("Máximo:", maximo)
    print("Desviación estándar:", desviacion)
else:
    print("⚠ La tabla Dim_Accounts no contiene la columna 'limit'")

conn.close()
