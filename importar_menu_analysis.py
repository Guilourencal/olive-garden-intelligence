import pandas as pd
from db import get_conn
import psycopg2
from datetime import datetime
import os
import re

# Criar tabela
conn = get_conn()
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS menu_analysis (
        id SERIAL PRIMARY KEY,
        semana_ref DATE NOT NULL,
        arquivo_origem VARCHAR(255),
        category_group VARCHAR(100),
        category VARCHAR(100),
        item VARCHAR(255) NOT NULL,
        type VARCHAR(50),
        canal VARCHAR(50),
        percent_of_checks FLOAT,
        number_of_checks INTEGER,
        gross_sales FLOAT,
        net_sales FLOAT,
        gross_sales_per_check FLOAT,
        gross_total_check_avg FLOAT,
        net_total_check_avg FLOAT,
        quantity_per_check FLOAT,
        total_quantity INTEGER,
        discounts FLOAT,
        avg_discount_per_check FLOAT,
        profit FLOAT,
        profit_per_check FLOAT,
        avg_guests FLOAT,
        guest_average FLOAT,
        cover_average FLOAT,
        most_popular_revenue_center VARCHAR(255),
        most_popular_day VARCHAR(100),
        most_popular_day_part VARCHAR(100),
        percent_bought_alone FLOAT,
        basket_1 VARCHAR(255),
        basket_2 VARCHAR(255),
        basket_3 VARCHAR(255),
        basket_4 VARCHAR(255),
        basket_5 VARCHAR(255),
        basket_6 VARCHAR(255),
        basket_7 VARCHAR(255),
        basket_8 VARCHAR(255),
        basket_9 VARCHAR(255),
        basket_10 VARCHAR(255),
        rot_gross_total_check_avg FLOAT,
        rot_net_total_check_avg FLOAT,
        rot_discounts FLOAT,
        rot_avg_discount_per_check FLOAT,
        rot_quantity_per_check FLOAT,
        rot_guest_average FLOAT,
        ct_gross_total_check_avg FLOAT,
        ct_net_total_check_avg FLOAT,
        ct_discounts FLOAT,
        ct_avg_discount_per_check FLOAT,
        ct_quantity_per_check FLOAT,
        ct_guest_average FLOAT,
        ct_cover_average FLOAT,
        revenue_score FLOAT,
        check_uplift FLOAT,
        UNIQUE(semana_ref, item)
    )
""")
conn.commit()
print('Tabela criada!')

# Itens a excluir
ITENS_EXCLUIR = ['BROWNIE CORTESIA', 'SSB']
PREFIXOS_EXCLUIR = ['RF ']

def deve_excluir(item, gross_sales_per_check):
    if not isinstance(item, str):
        return True
    item_upper = item.upper()
    for exc in ITENS_EXCLUIR:
        if exc in item_upper:
            return True
    for pref in PREFIXOS_EXCLUIR:
        if item_upper.startswith(pref):
            return True
    if 'DLV' in item_upper and 'SOUP' in item_upper and gross_sales_per_check and float(gross_sales_per_check) <= 0.05:
        return True
    return False

def detectar_canal(item, revenue_center):
    if isinstance(item, str) and item.upper().startswith('DLV'):
        return 'Delivery'
    if isinstance(revenue_center, str) and 'Delivery' in revenue_center:
        return 'Delivery'
    return 'POS'

# Importar arquivos
pasta = r'data\menu_analysis'
os.makedirs(pasta, exist_ok=True)
arquivos = [f for f in os.listdir(pasta) if f.endswith('.xls') or f.endswith('.xlsx')]
print(f'Arquivos encontrados: {len(arquivos)}')

total_ins = total_dup = 0
for arquivo in sorted(arquivos):
    caminho = os.path.join(pasta, arquivo)
    engine = 'xlrd' if arquivo.endswith('.xls') else 'openpyxl'
    
    # Extrair data do nome do arquivo (formato MM-DD-YYYY)
    match = re.search(r'(\d{2})-(\d{2})-(\d{4})', arquivo)
    if match:
        mes, dia, ano = match.groups()
        semana_ref = datetime(int(ano), int(mes), int(dia)).date()
    else:
        semana_ref = datetime.today().date()
    
    print(f'\nImportando: {arquivo} | Semana ref: {semana_ref}')
    
    df = pd.read_excel(caminho, engine=engine, header=3)
    df = df[df['Item'].notna() & (df['Item'] != 'Click the \'+\' next to the row number to expand a category.')].copy()
    
    ins = dup = 0
    for _, row in df.iterrows():
        item = str(row.get('Item', ''))
        gsp = row.get('Gross Sales Per Check Of Item')
        if deve_excluir(item, gsp):
            continue
        
        canal = detectar_canal(item, row.get('Most Popular Revenue Center'))
        
        gross_sales = float(row['Gross Sales']) if pd.notna(row.get('Gross Sales')) else None
        ct_gross = float(row['Gross Total Check Average.1']) if pd.notna(row.get('Gross Total Check Average.1')) else None
        gross_avg = float(row['Gross Total Check Average']) if pd.notna(row.get('Gross Total Check Average')) else None
        checks = int(row['Number Of Checks With Item']) if pd.notna(row.get('Number Of Checks With Item')) else 0
        
        # Revenue Score = Gross Sales + (checks x Check Uplift)
        check_uplift = (ct_gross - gross_avg) if ct_gross and gross_avg else None
        revenue_score = (gross_sales + (checks * check_uplift)) if gross_sales and check_uplift else gross_sales
        
        try:
            cur.execute("""
                INSERT INTO menu_analysis (
                    semana_ref, arquivo_origem, category_group, category, item, type, canal,
                    percent_of_checks, number_of_checks, gross_sales, net_sales,
                    gross_sales_per_check, gross_total_check_avg, net_total_check_avg,
                    quantity_per_check, total_quantity, discounts, avg_discount_per_check,
                    profit, profit_per_check, avg_guests, guest_average, cover_average,
                    most_popular_revenue_center, most_popular_day, most_popular_day_part,
                    percent_bought_alone,
                    basket_1, basket_2, basket_3, basket_4, basket_5,
                    basket_6, basket_7, basket_8, basket_9, basket_10,
                    rot_gross_total_check_avg, rot_net_total_check_avg,
                    rot_discounts, rot_avg_discount_per_check,
                    rot_quantity_per_check, rot_guest_average,
                    ct_gross_total_check_avg, ct_net_total_check_avg,
                    ct_discounts, ct_avg_discount_per_check,
                    ct_quantity_per_check, ct_guest_average, ct_cover_average,
                    revenue_score, check_uplift
                ) VALUES (
                    %s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,
                    %s,%s
                ) ON CONFLICT (semana_ref, item) DO NOTHING
            """, (
                semana_ref, arquivo,
                str(row.get('Category Group','')) if pd.notna(row.get('Category Group')) else None,
                str(row.get('Category','')) if pd.notna(row.get('Category')) else None,
                item, str(row.get('Type','')) if pd.notna(row.get('Type')) else None, canal,
                float(row['Percent Of Checks']) if pd.notna(row.get('Percent Of Checks')) else None,
                checks,
                gross_sales,
                float(row['Net Sales']) if pd.notna(row.get('Net Sales')) else None,
                float(gsp) if pd.notna(gsp) else None,
                gross_avg,
                float(row['Net Total Check Average']) if pd.notna(row.get('Net Total Check Average')) else None,
                float(row['Quantity Per Check']) if pd.notna(row.get('Quantity Per Check')) else None,
                int(row['Total Quantity']) if pd.notna(row.get('Total Quantity')) else None,
                float(row['Discounts Or Coupons']) if pd.notna(row.get('Discounts Or Coupons')) else None,
                float(row['Average Discount Per Check']) if pd.notna(row.get('Average Discount Per Check')) else None,
                float(row['Profit']) if pd.notna(row.get('Profit')) else None,
                float(row['Profit Per Check']) if pd.notna(row.get('Profit Per Check')) else None,
                float(row['Average Number Of Guests']) if pd.notna(row.get('Average Number Of Guests')) else None,
                float(row['Guest Average']) if pd.notna(row.get('Guest Average')) else None,
                float(row['Cover Average']) if pd.notna(row.get('Cover Average')) else None,
                str(row.get('Most Popular Revenue Center',''))[:255] if pd.notna(row.get('Most Popular Revenue Center')) else None,
                str(row.get('Most Popular Day',''))[:100] if pd.notna(row.get('Most Popular Day')) else None,
                str(row.get('Most Popular Day Part',''))[:100] if pd.notna(row.get('Most Popular Day Part')) else None,
                float(row['Percent Bought Alone']) if pd.notna(row.get('Percent Bought Alone')) else None,
                str(row.get('Most Popular Basket 1',''))[:255] if pd.notna(row.get('Most Popular Basket 1')) else None,
                str(row.get('Most Popular Basket 2',''))[:255] if pd.notna(row.get('Most Popular Basket 2')) else None,
                str(row.get('Most Popular Basket 3',''))[:255] if pd.notna(row.get('Most Popular Basket 3')) else None,
                str(row.get('Most Popular Basket 4',''))[:255] if pd.notna(row.get('Most Popular Basket 4')) else None,
                str(row.get('Most Popular Basket 5',''))[:255] if pd.notna(row.get('Most Popular Basket 5')) else None,
                str(row.get('Most Popular Basket 6',''))[:255] if pd.notna(row.get('Most Popular Basket 6')) else None,
                str(row.get('Most Popular Basket 7',''))[:255] if pd.notna(row.get('Most Popular Basket 7')) else None,
                str(row.get('Most Popular Basket 8',''))[:255] if pd.notna(row.get('Most Popular Basket 8')) else None,
                str(row.get('Most Popular Basket 9',''))[:255] if pd.notna(row.get('Most Popular Basket 9')) else None,
                str(row.get('Most Popular Basket 10',''))[:255] if pd.notna(row.get('Most Popular Basket 10')) else None,
                float(row['Gross Total Check Average']) if pd.notna(row.get('Gross Total Check Average')) else None,
                float(row['Net Total Check Average']) if pd.notna(row.get('Net Total Check Average')) else None,
                float(row['Discounts Or Coupons.1']) if pd.notna(row.get('Discounts Or Coupons.1')) else None,
                float(row['Average Discount Per Check.1']) if pd.notna(row.get('Average Discount Per Check.1')) else None,
                float(row['Quantity Per Check.1']) if pd.notna(row.get('Quantity Per Check.1')) else None,
                float(row['Guest Average.1']) if pd.notna(row.get('Guest Average.1')) else None,
                ct_gross,
                float(row['Net Total Check Average.1']) if pd.notna(row.get('Net Total Check Average.1')) else None,
                float(row['Discounts Or Coupons.2']) if pd.notna(row.get('Discounts Or Coupons.2')) else None,
                float(row['Average Discount Per Check.2']) if pd.notna(row.get('Average Discount Per Check.2')) else None,
                float(row['Quantity Per Check.2']) if pd.notna(row.get('Quantity Per Check.2')) else None,
                float(row['Guest Average.2']) if pd.notna(row.get('Guest Average.2')) else None,
                float(row['Cover Average.1']) if pd.notna(row.get('Cover Average.1')) else None,
                revenue_score, check_uplift
            ))
            if cur.rowcount > 0:
                ins += 1
            else:
                dup += 1
        except Exception as e:
            conn.rollback()
            print(f'  Erro {item}: {e}')
            continue
    
    conn.commit()
    print(f'  Inseridos: {ins} | Duplicatas: {dup}')
    total_ins += ins
    total_dup += dup

cur.execute('SELECT COUNT(*), MIN(semana_ref), MAX(semana_ref) FROM menu_analysis')
row = cur.fetchone()
print(f'\nBanco: {row[0]} itens | {row[1]} a {row[2]}')
cur.close()
conn.close()
print('Concluido!')
