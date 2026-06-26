import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("""
    SELECT periodo, forma_pagamento, SUM(pedidos) as pedidos
    FROM ifood_pagamentos
    WHERE periodo LIKE '%05/2026%'
    GROUP BY periodo, forma_pagamento
    ORDER BY periodo, forma_pagamento
""", conn)
conn.close()

print('Periodos:', sorted(df['periodo'].unique()))
print()
print(df.groupby('forma_pagamento')['pedidos'].sum().sort_values(ascending=False).to_string())
