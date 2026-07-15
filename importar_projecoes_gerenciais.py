# -*- coding: utf-8 -*-
"""
importar_projecoes_gerenciais.py
Lê as planilhas de projeção por unidade (aba 'projeção de vendas') e importa:
  - Projeção gerencial do mês (linha 9, col 3)
  - Budget do mês (linha 8, col 3)
  - Meta diária por dia (linhas 31-61, cols 5/7/8/9)

USO:
    cd C:\\olive-garden-reviews
    .\\venv\\Scripts\\Activate.ps1
    python importar_projecoes_gerenciais.py

Coloque os arquivos xlsx na pasta: data\\projecoes_gerenciais\\
Formato de nome esperado: XXX___PROJEÇÕES__MES_ANO.xlsx
"""
import os, glob, sys
import pandas as pd
from db import get_conn
from datetime import datetime

PASTA = r"data\projecoes_gerenciais"

MAPA_FILIAIS = {
    "GRU3": "Olive Garden - Guarulhos GRU3",
    "GRU2": "Olive Garden - Guarulhos GRU2",
    "DPO":  "Olive Garden - Dom Pedro",
    "ARI":  "Olive Garden - Aricanduva",
    "MOR":  "Olive Garden - Morumbi",
    "CNO":  "Olive Garden - Center Norte",
}

def safe_num(v):
    """Converte qualquer formato de número para float."""
    if pd.isna(v) or v is None: return None
    if isinstance(v, (int, float)): return float(v)
    s = str(v).strip()
    # Remove pontos de milhar e troca virgula decimal
    # Formato BR: 1.060.078,00 -> 1060078.00
    # Formato US: 1,060,078.00 -> 1060078.00
    if s.count('.') > 1:
        s = s.replace('.', '')  # remove pontos de milhar BR
    elif s.count(',') > 1:
        s = s.replace(',', '')  # remove virgulas de milhar US
    s = s.replace(',', '.')
    try:
        return float(s)
    except:
        return None

def extrair_cod_filial(nome_arquivo):
    """Extrai o código da filial do nome do arquivo (ex: GRU3___PROJ... -> GRU3)."""
    base = os.path.basename(nome_arquivo)
    for cod in MAPA_FILIAIS:
        if base.upper().startswith(cod):
            return cod
    return None

def ler_projecao(caminho):
    """Lê a aba 'projeção de vendas' e retorna dict com dados extraídos."""
    df = pd.read_excel(caminho, sheet_name='projeção de vendas', header=None)

    proj_mensal = safe_num(df.iloc[9, 3])
    budget_mes  = safe_num(df.iloc[8, 3])

    # Determina o mês a partir da data na linha 31, coluna 5
    mes = None
    for i in range(31, 62):
        val = df.iloc[i, 5]
        if pd.notna(val):
            try:
                dt = pd.to_datetime(val)
                mes = dt.replace(day=1).date()
                break
            except:
                pass

    # Lê dias: linhas 31-61, cols 5(data), 7(meta_salao), 8(meta_dlv), 9(meta_dia)
    dias = []
    for i in range(31, 62):
        row = df.iloc[i]
        data = row[5]
        if pd.isna(data): continue
        try:
            data = pd.to_datetime(data).date()
        except:
            continue
        meta_salao = safe_num(row[7])
        meta_dlv   = safe_num(row[8])
        meta_dia   = safe_num(row[9])
        if meta_dia and meta_dia > 0:
            dias.append({
                "data":       data,
                "meta_salao": round(meta_salao, 2) if meta_salao else None,
                "meta_dlv":   round(meta_dlv,   2) if meta_dlv   else None,
                "meta_dia":   round(meta_dia,   2) if meta_dia   else None,
            })

    return {
        "mes":          mes,
        "proj_mensal":  proj_mensal,
        "budget_mes":   budget_mes,
        "dias":         dias,
    }

def main():
    os.makedirs(PASTA, exist_ok=True)
    arquivos = sorted(glob.glob(os.path.join(PASTA, "*.xlsx")))
    print(f"Arquivos encontrados: {len(arquivos)}")
    if not arquivos:
        print(f"Coloque os arquivos xlsx em: {PASTA}")
        sys.exit(0)

    conn = get_conn()
    cur  = conn.cursor()

    total_ins = total_upd = total_err = 0

    for arq in arquivos:
        nome = os.path.basename(arq)
        cod  = extrair_cod_filial(nome)
        if not cod:
            print(f"  [SKIP] {nome} — código de filial não reconhecido")
            continue
        filial = MAPA_FILIAIS[cod]
        print(f"\nImportando: {nome}")
        print(f"  Filial: {filial}")

        try:
            dados = ler_projecao(arq)
        except Exception as e:
            print(f"  ERRO ao ler arquivo: {e}")
            total_err += 1
            continue

        if not dados["mes"]:
            print(f"  ERRO: não foi possível determinar o mês")
            total_err += 1
            continue

        print(f"  Mês:              {dados['mes'].strftime('%m/%Y')}")
        print(f"  Projeção gerencial: R$ {dados['proj_mensal']:>10,.0f}".replace(",","."))
        print(f"  Budget do mês:      R$ {dados['budget_mes']:>10,.0f}".replace(",","."))
        print(f"  Dias com meta:      {len(dados['dias'])}")
        if dados["dias"]:
            total_meta = sum(d["meta_dia"] for d in dados["dias"] if d["meta_dia"])
            print(f"  Soma meta diária:   R$ {total_meta:>10,.0f}".replace(",","."))

        try:
            # Insere/atualiza projecoes_gerenciais
            cur.execute("""
                INSERT INTO projecoes_gerenciais
                    (mes, filial, proj_gerencial, budget_mes, arquivo_origem)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (mes, filial) DO UPDATE
                    SET proj_gerencial = EXCLUDED.proj_gerencial,
                        budget_mes     = EXCLUDED.budget_mes,
                        arquivo_origem = EXCLUDED.arquivo_origem,
                        importado_em   = CURRENT_TIMESTAMP
            """, (dados["mes"], filial, dados["proj_mensal"],
                  dados["budget_mes"], nome))
            acao = "inserido" if cur.rowcount == 1 else "atualizado"
            print(f"  projecoes_gerenciais: {acao}")

            conn.commit()
            total_ins += 1

        except Exception as e:
            conn.rollback()
            print(f"  ERRO no banco: {e}")
            total_err += 1
            continue

    print(f"\n{'='*50}")
    print(f"Concluído: {total_ins} inseridos/atualizados | {total_err} erros")

    # Resumo do banco
    cur.execute("""
        SELECT filial, mes, proj_gerencial, budget_mes
        FROM projecoes_gerenciais
        ORDER BY mes, filial
    """)
    rows = cur.fetchall()
    if rows:
        print(f"\n=== Banco: projecoes_gerenciais ===")
        for r in rows:
            print(f"  {r[1].strftime('%m/%Y')} | {r[0]:<35} | Proj: R${r[2]:>10,.0f} | Budget: R${r[3]:>10,.0f}".replace(",","."))
        total_proj = sum(r[2] for r in rows if r[2])
        total_budg = sum(r[3] for r in rows if r[3])
        print(f"\n  REDE TOTAL | Proj: R${total_proj:>10,.0f} | Budget: R${total_budg:>10,.0f}".replace(",","."))

    conn.close()

if __name__ == "__main__":
    main()
