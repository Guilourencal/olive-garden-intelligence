import subprocess
import sys

print("=" * 50)
print("OLIVE GARDEN — Atualizacao parcial (sem Apify)")
print("=" * 50)

scripts = [
    ("Coletando Google Reviews...", "coletar_google.py"),
    ("Coletando noticias...", "coletar_noticias.py"),
    ("Coletando Instagram...", "coletar_instagram.py"),
    ("Unificando dados...", "unificar_dados.py"),
    ("Classificando sentimento...", "classificar_sentimento.py"),
    ("Atualizando banco local...", "criar_banco.py"),
    ("Classificando social...", "classificar_social.py"),
    ("Salvando noticias...", "salvar_noticias.py"),
    ("Atualizando Supabase...", "resetar_reviews.py"),
    ("Validando dados...", "validar_dados.py"),
]

import os
env = os.environ.copy()
env["TRANSFORMERS_OFFLINE"] = "1"

for mensagem, script in scripts:
    print(f"\n{mensagem}")
    resultado = subprocess.run([sys.executable, script], capture_output=False, env=env)
    if resultado.returncode != 0:
        print(f"ERRO em {script}. Abortando.")
        sys.exit(1)

print("\n✅ Atualizacao parcial concluida!")
