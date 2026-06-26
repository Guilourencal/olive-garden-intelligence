# -*- coding: utf-8 -*-
"""Conexao unica ao Supabase. Le de st.secrets (Streamlit Cloud) ou de
variaveis de ambiente / .env (execucao local). Nenhuma credencial no codigo."""
import os
import psycopg2

try:                              # carrega .env quando roda local (scripts)
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _get(key, default=None):
    try:                          # 1) Streamlit Cloud -> st.secrets
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    val = os.environ.get(key, default)   # 2) local -> ambiente / .env
    if val is None:
        raise RuntimeError(
            f"Credencial ausente: {key} (defina em .env ou nos Secrets do Streamlit)"
        )
    return val


def get_conn():
    return psycopg2.connect(
        host=_get("SUPABASE_HOST"),
        port=_get("SUPABASE_PORT", "6543"),
        user=_get("SUPABASE_USER"),
        password=_get("SUPABASE_PASSWORD"),
        dbname=_get("SUPABASE_DB", "postgres"),
    )

def get_conn_ro():
    return psycopg2.connect(
        host=_get("SUPABASE_HOST"),
        port=_get("SUPABASE_PORT", "6543"),
        user=_get("SUPABASE_USER_RO"),
        password=_get("SUPABASE_PASSWORD_RO"),
        dbname=_get("SUPABASE_DB", "postgres"),
    )
