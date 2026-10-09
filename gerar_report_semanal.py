# -*- coding: utf-8 -*-
"""
gerar_report_semanal.py — OG Intelligence
Report semanal por unidade para WhatsApp (formato visual).

USO:
    python gerar_report_semanal.py --unidade "Morumbi" --salvar
    python gerar_report_semanal.py --data 2026-09-08
"""
import argparse
from datetime import date, timedelta
from db import get_conn

UNIDADES = ["Morumbi","Center Norte","Dom Pedro","Aricanduva","Guarulhos GRU2","Guarulhos GRU3","Tambore"]

ALERTA_META_PCT  = -5.0
ALERTA_RECL_MULT = 1.5
UNIDADES_IFOOD   = ["Morumbi","Center Norte","Dom Pedro","Aricanduva"]

# Mapa nome ifood_diario -> filial_curta
IFOOD_NOMES = {
    "Morumbi":      "Olive Garden - Shopping Morumbi",
    "Center Norte": "Olive Garden - Shopping Center Norte",
    "Dom Pedro":    "Olive Garden - Shopping Parque Dom Pedro",
    "Aricanduva":   "Olive Garden  - Shopping Aricanduva",
}

def sf(v):
    try: return float(v) if v is not None else None
    except: return None

def brl(v):
    if v is None: return "—"
    return "R$ {:,.0f}".format(v).replace(",",".")

def seta(v, emoji=True):
    if v is None: return "—"
    if emoji:
        e = "📈" if v >= 0 else "📉"
        return f"{e} {'▲' if v>=0 else '▼'} {abs(v):.1f}%"
    return f"{'▲' if v>=0 else '▼'} {abs(v):.1f}%"

def semaforo(v):
    if v is None: return "⚪"
    if v >= 0: return "🟢"
    if v >= -5: return "🟡"
    return "🔴"

def barra(pct, larg=20):
    p = min(max(pct, 0), 100)
    f = round(p / 100 * larg)
    return "▓" * f + "░" * (larg - f) + f"  {p:.0f}%"

def semana_ref(hoje=None):
    if hoje is None: hoje = date.today()
    ini = hoje - timedelta(days=hoje.weekday()+7)
    return ini, ini+timedelta(days=6)

def run(cur, sql, params=()):
    cur.execute(sql, params)
    return cur.fetchone()

def q_vendas(cur, filial, ini, fim):
    r = run(cur, """
        SELECT SUM(venda_salao), SUM(gc_salao), SUM(meta_venda),
               (SUM(venda_salao)/NULLIF(SUM(gc_salao),0))::numeric
        FROM vendas_diarias WHERE filial=%s AND data BETWEEN %s AND %s
    """, (filial, ini, fim))
    return {"salao": sf(r[0]) or 0, "gc": int(r[1] or 0),
            "meta": sf(r[2]) or 0, "ticket": round(sf(r[3]) or 0, 0)}

def q_salao(cur, filial, ini, fim):
    r = run(cur, "SELECT SUM(venda_salao) FROM vendas_diarias WHERE filial=%s AND data BETWEEN %s AND %s",
            (filial, ini, fim))
    return sf(r[0]) if r else None

def q_ifood(cur, un, ini, fim):
    nome_if = IFOOD_NOMES.get(un)
    if not nome_if:
        return {"fat": 0, "ped": 0, "ticket": 0}
    r = run(cur, """
        SELECT SUM(faturamento), SUM(pedidos),
               (SUM(faturamento)/NULLIF(SUM(pedidos),0))::numeric
        FROM ifood_diario WHERE filial=%s AND data BETWEEN %s AND %s
    """, (nome_if, ini, fim))
    return {"fat": sf(r[0]) or 0, "ped": int(r[1] or 0), "ticket": round(sf(r[2]) or 0, 0)}

def q_recl(cur, un, ini, fim):
    r = run(cur, """
        SELECT COUNT(*), STRING_AGG(DISTINCT tema, ', ') FILTER (WHERE tema IS NOT NULL)
        FROM reclamacoes_buzzmonitor
        WHERE unidade_curta=%s AND data::date BETWEEN %s AND %s
    """, (un, ini, fim))
    return {"n": int(r[0] or 0), "temas": r[1] or "—"}

def q_media_recl(cur, un):
    r = run(cur, """
        SELECT (COUNT(*))::float / NULLIF(COUNT(DISTINCT DATE_TRUNC('week', data::date)), 0)
        FROM reclamacoes_buzzmonitor WHERE unidade_curta=%s
    """, (un,))
    return sf(r[0]) or 0

def q_reviews(cur, filial, ini, fim):
    r = run(cur, """
        SELECT COUNT(*), AVG(nota)::numeric
        FROM reviews WHERE filial=%s AND criado_em::date BETWEEN %s AND %s
    """, (filial, ini, fim))
    return {"n": int(r[0] or 0), "nota": round(sf(r[1]), 1) if r[1] else None}

def q_dias_ruins(cur, filial, ini, fim, thr):
    cur.execute("""
        SELECT data, TRIM(TO_CHAR(data, 'Dy')),
               ((venda_salao/NULLIF(meta_venda,0))-1)*100
        FROM vendas_diarias
        WHERE filial=%s AND data BETWEEN %s AND %s
          AND meta_venda > 0 AND venda_salao < meta_venda * %s
        ORDER BY 3 ASC
    """, (filial, ini, fim, thr))
    return cur.fetchall()

def q_proj(cur, filial, ini, fim):
    r = run(cur, """
        SELECT SUM(valor_projetado) FROM projecoes_historico
        WHERE filial=%s AND data_alvo BETWEEN %s AND %s AND valor_realizado IS NULL
    """, (filial, ini, fim))
    return sf(r[0]) if r else None

def gerar(un, ini, fim, conn):
    cur = conn.cursor()
    filial  = f"Olive Garden - {un}"
    iso_w   = ini.isocalendar()[1]
    ini_p   = fim + timedelta(days=1)
    fim_p   = ini_p + timedelta(days=6)
    thr     = 1 + ALERTA_META_PCT / 100

    vd      = q_vendas(cur, filial, ini, fim)
    vd_ant  = q_salao(cur, filial, ini-timedelta(weeks=1), fim-timedelta(weeks=1))
    vd_2025 = q_salao(cur, filial, ini-timedelta(weeks=52), fim-timedelta(weeks=52))
    if_      = q_ifood(cur, un, ini, fim)
    recl    = q_recl(cur, un, ini, fim)
    med_r   = q_media_recl(cur, un)
    rev     = q_reviews(cur, filial, ini, fim)
    dias_r  = q_dias_ruins(cur, filial, ini, fim, thr)
    proj    = q_proj(cur, filial, ini_p, fim_p)

    salao  = vd["salao"]; meta = vd["meta"]
    ticket = vd["ticket"]; gc  = vd["gc"]
    vs_meta  = (salao/meta-1)*100    if meta > 0            else None
    vs_ant   = (salao/vd_ant-1)*100  if vd_ant and vd_ant>0 else None
    vs_2025  = (salao/vd_2025-1)*100 if vd_2025 and vd_2025>0 else None
    pct_meta = (salao/meta*100)      if meta > 0            else 0

    total_sem = salao + if_["fat"]
    sem = semaforo(vs_meta)

    # Alertas
    alertas = []
    if vs_meta is not None and vs_meta < ALERTA_META_PCT:
        alertas.append(f"🔴 Venda {vs_meta:.1f}% abaixo da meta")
    if len(dias_r) >= 3:
        alertas.append(f"🔴 {len(dias_r)} dias abaixo da meta na semana")
    if med_r > 0 and recl["n"] > med_r * ALERTA_RECL_MULT:
        alertas.append(f"🔴 Reclamações acima da média ({recl['n']} vs ~{med_r:.1f}/sem)")
    if rev["nota"] and rev["nota"] < 3.5:
        alertas.append(f"🔴 Nota média reviews: {rev['nota']} ⭐")
    if ticket and ticket < 120:
        alertas.append(f"🟡 Ticket médio abaixo de R$ 120 ({brl(ticket)})")

    # Oportunidades
    ops = []
    if vs_2025 is not None and vs_2025 < 0:
        ops.append(f"💡 Abaixo do mesmo período 2025 ({vs_2025:.1f}%) — revisar ações")
    if vs_meta is not None and -2 < vs_meta < 2:
        ops.append("💡 Próximo da meta — foco no FDS para superar")
    if ticket and ticket < 125:
        ops.append(f"💡 Ticket em {brl(ticket)} — upsell em sobremesas e bebidas")
    if un in UNIDADES_IFOOD and if_["fat"] == 0:
        ops.append("💡 iFood sem registros na semana — verificar operação")
    if not ops and not alertas:
        ops.append("✅ Semana dentro do esperado — manter o ritmo!")

    L = [
        f"━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📊 *REPORT SEMANAL*",
        f"🏠 *{un.upper()}*",
        f"📅 Semana {iso_w}  |  {ini.strftime('%d/%m')} a {fim.strftime('%d/%m/%Y')}",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        f"💰 *FINANCEIRO*",
        "",
        f"{sem}  *{brl(salao)}*  _({seta(vs_meta, emoji=False)} vs meta)_",
        "",
        f"`{barra(pct_meta)}`",
        f"_Meta: {brl(meta)}_",
        "",
        f"📈 vs sem. ant.:  {seta(vs_ant)}",
        f"📅 vs 2025:       {seta(vs_2025)}",
        f"🍽️ Covers: {gc:,}  |  🎟️ Ticket: {brl(ticket)}".replace(",","."),
    ]

    if if_["fat"] > 0:
        L += [
            "",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"🛵 *iFOOD*",
            "",
            f"💰 {brl(if_['fat'])}  |  📦 {if_['ped']} pedidos",
            f"🎟️ Ticket médio: {brl(if_['ticket'])}",
            f"📊 Total semana (salão + iFood): *{brl(total_sem)}*",
        ]

    recl_status = "✅ Dentro do normal" if recl["n"] <= (med_r * ALERTA_RECL_MULT or 999) else "⚠️ Acima da média"
    L += [
        "",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⭐ *REPUTAÇÃO*",
        "",
        f"😤 Reclamações:  {recl['n']}  _({recl_status})_",
    ]
    if recl["n"] > 0 and recl["temas"] != "—":
        L.append(f"   → {recl['temas'][:100]}")
    if rev["n"] > 0:
        est = "⭐" * round(rev["nota"]) if rev["nota"] else ""
        L += [f"⭐ Reviews novos:  {rev['n']}",
              f"   → Nota: {rev['nota']} {est}"]
    else:
        L.append("⭐ Reviews:  sem novos na semana")

    if alertas:
        L += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━",
              "⚠️ *ALERTAS*", ""] + alertas

    L += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━",
          "🎯 *OPORTUNIDADES*", ""] + ops

    proj_txt = brl(proj) if proj else "em cálculo"
    L += [
        "", "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🔮 *PRÓXIMA SEMANA*",
        "",
        f"📅 {ini_p.strftime('%d/%m')} a {fim_p.strftime('%d/%m/%Y')}",
        f"📊 Previsão salão: *{proj_txt}*",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "_OG Intelligence — gerado automaticamente_",
        f"_{date.today().strftime('%d/%m/%Y')} às 11:00_",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]
    return "\n".join(L)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unidade")
    parser.add_argument("--salvar", action="store_true")
    parser.add_argument("--data")
    args = parser.parse_args()
    hoje = date.fromisoformat(args.data) if args.data else date.today()
    ini, fim = semana_ref(hoje)
    print(f"=== REPORT SEMANAL OG INTELLIGENCE ===")
    print(f"Semana: {ini.strftime('%d/%m')} a {fim.strftime('%d/%m/%Y')}\n")
    unidades = [args.unidade] if args.unidade else UNIDADES
    conn = get_conn()
    for un in unidades:
        print(f"Gerando: {un}...")
        try:
            report = gerar(un, ini, fim, conn)
            print("\n" + report + "\n")
            if args.salvar:
                nome = f"report_sem{ini.isocalendar()[1]}_{un.replace(' ','_')}.txt"
                open(nome, "w", encoding="utf-8").write(report)
                print(f"  → Salvo: {nome}")
        except Exception as e:
            import traceback
            print(f"  ERRO em {un}: {e}")
            traceback.print_exc()
    conn.close()

if __name__ == "__main__":
    main()
