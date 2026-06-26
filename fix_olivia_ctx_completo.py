lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

nova_funcao = '''    # Contexto dinamico com dados reais de todo o banco
    def _gerar_contexto_banco():
        try:
            import psycopg2 as _pg
from db import get_conn
            _conn = get_conn()
            _cur = _conn.cursor()

            # iFood
            _cur.execute("SELECT filial, periodo, SUM(faturamento) as fat, SUM(pedidos) as ped FROM ifood_vendas WHERE logistica = \'Entrega parceira\' GROUP BY filial, periodo ORDER BY filial, periodo")
            _if = _cur.fetchall()

            # Vendas salao 2026
            _cur.execute("SELECT filial, EXTRACT(month FROM data::date) as mes, SUM(venda_salao) as salao, SUM(meta_venda) as budget FROM vendas_diarias WHERE EXTRACT(year FROM data::date) = 2026 GROUP BY filial, EXTRACT(month FROM data::date) ORDER BY filial, mes")
            _vd = _cur.fetchall()

            # Pesquisa GSS - ultimo periodo por filial
            _cur.execute("SELECT restaurant, periodo, overall_experience, value, service, taste, speed_of_service, clean FROM pesquisa_performance ORDER BY periodo DESC LIMIT 12")
            _gss = _cur.fetchall()

            # Reclamacoes resumo
            _cur.execute("SELECT unidade_curta, COUNT(*) as n, ROUND(AVG(avaliacao)::numeric,2) as nota, tema FROM (SELECT unidade_curta, avaliacao, tema FROM reclamacoes_buzzmonitor WHERE data >= \'2026-01-01\') t GROUP BY unidade_curta, tema ORDER BY unidade_curta, n DESC")
            _recl = _cur.fetchall()

            # Reviews resumo
            _cur.execute("SELECT plataforma, COUNT(*) as n, ROUND(AVG(nota)::numeric,2) as nota FROM reviews GROUP BY plataforma")
            _rev = _cur.fetchall()

            # Fila espera resumo
            _cur.execute("SELECT status, COUNT(*) as n, ROUND(AVG(duracao_minutos)::numeric,1) as espera_media FROM fila_espera WHERE dia_chegada >= \'2026-01-01\' GROUP BY status")
            _fila = _cur.fetchall()

            # Menu - ultima semana
            _cur.execute("SELECT item, type, number_of_checks, gross_sales, revenue_score FROM menu_analysis WHERE semana_ref = (SELECT MAX(semana_ref) FROM menu_analysis) ORDER BY revenue_score DESC LIMIT 20")
            _menu = _cur.fetchall()

            _cur.close(); _conn.close()
            _meses = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

            ctx = "\\nDADOS REAIS ATUALIZADOS DO BANCO:\\n"

            ctx += "\\n--- iFOOD (Entrega parceira) por periodo ---\\n"
            for r in _if:
                ctx += f"- {r[0].replace(\'Olive Garden - \',\'\')} | {r[1]} | R$ {r[2]:,.0f} | {r[3]} ped\\n".replace(",",".")

            ctx += "\\n--- VENDA SALAO 2026 por mes ---\\n"
            _fil_ant = ""
            for r in _vd:
                _fil = r[0].replace("Olive Garden - ","")
                if _fil != _fil_ant:
                    if _fil_ant: ctx += "\\n"
                    ctx += f"- {_fil}: "
                    _fil_ant = _fil
                else:
                    ctx += " | "
                ctx += f"{_meses.get(int(r[1]),\'?\')} salao Rk/budget Rk"
            ctx += "\\n"

            ctx += "\\n--- PESQUISA GSS (ultimos periodos) ---\\n"
            for r in _gss:
                ctx += f"- {r[0].replace(\'Olive Garden - \',\'\')} | {r[1]} | ExpGeral:{r[2]:.1f} Valor:{r[3]:.1f} Atend:{r[4]:.1f} Sabor:{r[5]:.1f} Veloc:{r[6]:.1f} Limp:{r[7]:.1f}\\n"

            ctx += "\\n--- RECLAMACOES BUZZMONITOR 2026 ---\\n"
            _recl_fil = {}
            for r in _recl:
                if r[0] not in _recl_fil:
                    _recl_fil[r[0]] = []
                _recl_fil[r[0]].append(f"{r[3]}:{r[1]}")
            for fil, temas in _recl_fil.items():
                ctx += f"- {fil}: {' | '.join(temas[:3])}\\n"

            ctx += "\\n--- REVIEWS PLATAFORMAS ---\\n"
            for r in _rev:
                ctx += f"- {r[0]}: {r[1]} reviews | nota media {r[2]}\\n"

            ctx += "\\n--- FILA DE ESPERA 2026 ---\\n"
            for r in _fila:
                ctx += f"- {r[0]}: {r[1]} ocorrencias | espera media {r[2]} min\\n"

            ctx += "\\n--- MENU INTELLIGENCE (ultima semana) ---\\n"
            for r in _menu:
                ctx += f"- {r[0]} | {r[1]} | {r[2]} checks | R$ {r[3]:,.0f} | score {r[4]:.1f}\\n".replace(",",".")

            ctx += "\\nATENCAO: Se sua query retornar valores muito diferentes destes, ha erro no SQL.\\n"
            ctx += "Para iFood consulte ifood_vendas diretamente sem JOIN com vendas_diarias.\\n"
            return ctx
        except Exception as _e:
            return f"\\n(Contexto indisponivel: {_e})\\n"
    _contexto_dinamico = _gerar_contexto_banco()

'''

lines[1671:1702] = [nova_funcao]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
