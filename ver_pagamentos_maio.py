import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("""
    SELECT periodo, forma_pagamento, pedidos, faturamento
    FROM ifood_pagamentos
    WHERE periodo LIKE '%05/2026%'
    ORDER BY periodo, forma_pagamento
""", conn)
conn.close()

print('Total registros:', len(df))
print('Periodos:', sorted(df['periodo'].unique()))
print()
print('Formas de pagamento:', df['forma_pagamento'].unique().tolist())
print()
print(df.groupby('forma_pagamento').agg(pedidos=('pedidos','sum'), fat=('faturamento','sum')).sort_values('fat', ascending=False).to_string())
