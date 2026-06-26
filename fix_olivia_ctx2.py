lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'OLIVIA_SYSTEM = """' in l)
print(f'OLIVIA_SYSTEM na linha {idx+1}')

funcao = '''    # Contexto dinamico com dados reais
    def _gerar_contexto_banco():
        try:
            import psycopg2 as _pg
from db import get_conn
            _conn = get_conn()
            _cur = _conn.cursor()
            _cur.execute("SELECT filial, periodo, SUM(faturamento) as fat, SUM(pedidos) as ped FROM ifood_vendas WHERE logistica = \'Entrega parceira\' GROUP BY filial, periodo ORDER BY filial, periodo")
            _if = _cur.fetchall()
            _cur.execute("SELECT filial, EXTRACT(month FROM data::date) as mes, SUM(venda_salao) as salao FROM vendas_diarias WHERE EXTRACT(year FROM data::date) = 2026 GROUP BY filial, EXTRACT(month FROM data::date) ORDER BY filial, mes")
            _vd = _cur.fetchall()
            _cur.close(); _conn.close()
            _meses = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
            ctx = "\\nDADOS REAIS ATUALIZADOS DO BANCO:\\n\\niFood (Entrega parceira) por periodo:\\n"
            for r in _if:
                ctx += f"- {r[0].replace(\'Olive Garden - \',\'\')} | {r[1]} | R$ {r[2]:,.0f} | {r[3]} ped\\n".replace(",",".")
            ctx += "\\nVenda Salao 2026 por mes:\\n"
            _fil_ant = ""
            for r in _vd:
                _fil = r[0].replace("Olive Garden - ","")
                if _fil != _fil_ant:
                    if _fil_ant: ctx += "\\n"
                    ctx += f"- {_fil}: "
                    _fil_ant = _fil
                else:
                    ctx += " | "
                ctx += f"{_meses.get(int(r[1]),\'?\')} Rk"
            ctx += "\\n\\nATENCAO: Se sua query retornar valores muito diferentes destes, ha erro no SQL. Para iFood consulte ifood_vendas diretamente.\\n"
            return ctx
        except Exception as _e:
            return f"\\n(Contexto indisponivel: {_e})\\n"
    _contexto_dinamico = _gerar_contexto_banco()

'''

lines.insert(idx, funcao)
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
