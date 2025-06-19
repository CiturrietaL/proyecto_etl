import pandas as pd
import json
import sqlite3
import os

# ============================================
# ETAPA 0: LIMPIEZA BASE
# ============================================
if os.path.exists('etl_proyecto.db'):
    os.remove('etl_proyecto.db')
    print("🗑️ Base de datos eliminada correctamente")

# ============================================
# FUNCIONES AUXILIARES
# ============================================
def convertir_fecha(valor):
    try:
        fecha_raw = valor.get('$date')
        if fecha_raw is None:
            return pd.NaT
        return pd.to_datetime(fecha_raw)
    except:
        return pd.NaT

# ============================================
# ETAPA 1: LECTURA JSON
# ============================================

# Customers
with open('customers.json') as f:
    customers_data = json.load(f)
customers_df = pd.DataFrame(customers_data)

# Accounts
with open('accounts.json') as f:
    accounts_data = json.load(f)
accounts_df = pd.DataFrame(accounts_data)

# ============================================
# ETAPA 2: TRANSFORMACIONES
# ============================================

# Normalización customers
customers_df['birthdate'] = customers_df['birthdate'].apply(convertir_fecha)
customers_df['customer_id'] = customers_df['username'] + customers_df['name']
customers_df.drop_duplicates(subset=['customer_id'], inplace=True)

# Mapeo de account_id -> customer_id (por los accounts anidados en customers)
account_customer_map = []
for _, row in customers_df.iterrows():
    for account in row['accounts']:
        account_customer_map.append({'account_id': account, 'customer_id': row['customer_id']})
account_customer_df = pd.DataFrame(account_customer_map)

# Normalización accounts
accounts_df['bucket_start_date'] = accounts_df['bucket_start_date'].apply(convertir_fecha)
accounts_df['bucket_end_date'] = accounts_df['bucket_end_date'].apply(convertir_fecha)
accounts_df.rename(columns={'limit': 'account_limit'}, inplace=True)

# Merge limpio de accounts + customer_id
accounts_df = pd.merge(accounts_df, account_customer_df, on='account_id', how='left')

# ✅ BLINDAJE FINAL: eliminar duplicados en account_id antes de cargar
accounts_df = accounts_df.drop_duplicates(subset=['account_id'])

# PRODUCTS
products_list = []
for _, row in accounts_df.iterrows():
    account_id = row['account_id']
    products = row.get('products', [])
    if isinstance(products, list):
        for product in products:
            products_list.append({'account_id': account_id, 'product': product})
products_df = pd.DataFrame(products_list)

# TRANSACTIONS
transactions_list = []
for _, row in accounts_df.iterrows():
    account_id = row['account_id']
    transactions = row.get('transactions', [])
    if isinstance(transactions, list):
        for trans in transactions:
            trans_date_raw = trans.get('date', {})
            trans_date = pd.NaT
            try:
                if '$date' in trans_date_raw:
                    trans_date = pd.to_datetime(trans_date_raw['$date'])
            except:
                pass
            transactions_list.append({
                'account_id': account_id,
                'date': trans_date,
                'amount': trans.get('amount'),
                'transaction_code': trans.get('transaction_code'),
                'symbol': trans.get('symbol'),
                'price': trans.get('price'),
                'total': trans.get('total')
            })

transactions_df = pd.DataFrame(transactions_list)
transactions_df['transaction_id'] = range(1, len(transactions_df) + 1)

# ============================================
# ETAPA 3: CREACIÓN Y CARGA EN SQLITE
# ============================================

conn = sqlite3.connect('etl_proyecto.db')
cursor = conn.cursor()

# Creación de tablas (siempre en limpio)
cursor.execute("DROP TABLE IF EXISTS Dim_Customers")
cursor.execute("DROP TABLE IF EXISTS Dim_Accounts")
cursor.execute("DROP TABLE IF EXISTS Dim_Products")
cursor.execute("DROP TABLE IF EXISTS Fact_Transactions")

cursor.execute("""
CREATE TABLE Dim_Customers (
    customer_id TEXT PRIMARY KEY,
    username TEXT,
    name TEXT,
    birthdate DATE,
    address TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE Dim_Accounts (
    account_id INTEGER PRIMARY KEY,
    transaction_count INTEGER,
    bucket_start_date DATE,
    bucket_end_date DATE,
    account_limit INTEGER,
    customer_id TEXT
)
""")

cursor.execute("""
CREATE TABLE Dim_Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    product TEXT
)
""")

cursor.execute("""
CREATE TABLE Fact_Transactions (
    transaction_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    date DATE,
    amount FLOAT,
    transaction_code TEXT,
    symbol TEXT,
    price FLOAT,
    total FLOAT
)
""")

# ============================================
# ETAPA 4: CARGA FINAL (SIEMPRE LIMPIA)
# ============================================

customers_df_final = customers_df[['customer_id', 'username', 'name', 'birthdate', 'address', 'email']]
customers_df_final.to_sql('Dim_Customers', conn, if_exists='append', index=False)

accounts_df_final = accounts_df[['account_id', 'transaction_count', 'bucket_start_date', 'bucket_end_date', 'account_limit', 'customer_id']]
accounts_df_final.to_sql('Dim_Accounts', conn, if_exists='append', index=False)

products_df.to_sql('Dim_Products', conn, if_exists='append', index=False)
transactions_df.to_sql('Fact_Transactions', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print("✅ Carga ultrablindada completada sin duplicados 🚀")
