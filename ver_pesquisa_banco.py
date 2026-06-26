import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql('SELECT restaurant, periodo, overall_experience FROM pesquisa_performance ORDER BY periodo, restaurant', conn)
conn.close()

print('=== PERIODOS DISPONIVEIS ===')
print(sorted(df['periodo'].unique()))
print()
print('=== ULTIMO PERIODO ===')
ultimo = df['periodo'].max()
print(ultimo)
print()
print(df[df['periodo']==ultimo][['restaurant','overall_experience']].to_string(index=False))
