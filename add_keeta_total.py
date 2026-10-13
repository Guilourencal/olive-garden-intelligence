import pathlib, py_compile

p = pathlib.Path("dashboard.py")
t = p.read_text(encoding="utf-8")

OLD = '                proj_total_ve = proj_total + fat_if_mtd + proj_if_ve if "proj_total" in dir() else fat_total_mtd'

NEW = '''                # Keeta: liquido realizado + projecao resto do mes
                try:
                    _conn_kt = get_conn()
                    _cur_kt = _conn_kt.cursor()
                    _cur_kt.execute("""
                        SELECT COALESCE(SUM(ganhos_liquidos),0) as liq,
                               COUNT(DISTINCT data) as dias
                        FROM keeta_diario
                        WHERE EXTRACT(month FROM data)=EXTRACT(month FROM %s::date)
                          AND EXTRACT(year FROM data)=EXTRACT(year FROM %s::date)
                    """, (str(_hoje_ve2), str(_hoje_ve2)))
                    _kt_row = _cur_kt.fetchone()
                    _conn_kt.close()
                    _kt_liq_mtd = float(_kt_row[0]) if _kt_row else 0
                    _kt_dias = int(_kt_row[1]) if _kt_row else 0
                    _kt_proj = _kt_liq_mtd + (_kt_liq_mtd / _kt_dias * (_dias_no_mes_ve - _kt_dias)) if _kt_dias > 0 else 0
                except:
                    _kt_proj = 0
                proj_total_ve = proj_total + fat_if_mtd + proj_if_ve + _kt_proj if "proj_total" in dir() else fat_total_mtd'''

assert OLD in t, "Linha alvo nao encontrada"
t = t.replace(OLD, NEW, 1)
print("OK: Keeta adicionado ao proj_total_ve")

p.write_text(t, encoding="utf-8")
py_compile.compile(str(p), doraise=True)
print("OK: compila sem erros")
