# Proyecto ETL en Python – JSON a SQLite

Este proyecto consiste en el desarrollo completo de un pipeline ETL (Extract, Transform, Load) utilizando archivos JSON como fuente de datos y una base de datos SQLite como destino. Se implementaron transformaciones, validaciones y consultas analíticas en Python, con foco en calidad y trazabilidad.

## Estructura del proyecto

Proyectos_ETL/
│
├── accounts.json                 # Fuente de datos: cuentas
├── customers.json               # Fuente de datos: clientes
├── transactions.json            # Fuente de datos: transacciones
│
├── etl_proyecto.py              # Script principal ETL (carga + transformación)
├── verificar_datos.py           # Validaciones y limpieza inicial
├── consultas_sql.py             # Consultas SQL para validación
├── consultas_dw.py              # Consultas orientadas a data warehouse
├── consulta_requerimiento_1.py # Requerimiento específico para análisis
│
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo

## Tecnologías utilizadas

- Python 3.10+
- SQLite3
- pandas
- json

## Cómo ejecutar

1. Clona este repositorio:

   git clone https://github.com/CiturrietaL/proyecto_etl.git
   cd proyecto_etl

2. Ejecuta el script principal:

   python etl_proyecto.py

3. (Opcional) Ejecuta consultas SQL:

   python consultas_sql.py

## Dataset de ejemplo

Los archivos JSON incluidos (`customers.json`, `accounts.json`, `transactions.json`) simulan un entorno de clientes bancarios y sus movimientos. Pueden adaptarse fácilmente a otros escenarios reales de negocio.

## Autor

Cristian Iturrieta López  
Analista QA & Junior Data Analyst  
cristianiturrieta@gmail.com  
LinkedIn: https://www.linkedin.com *(opcional agregar tu URL)*

## Licencia

Este proyecto se encuentra disponible bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.
