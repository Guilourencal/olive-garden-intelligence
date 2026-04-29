import sys
print("Pipeline pausado - investigando runs excessivos.")
sys.exit(0)
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("OLIVE GARDEN — Atualização de dados")
print("=" * 50)

# ETAPA 1 — Backup
print("\n📦 ETAPA 1 — Backup dos dados atuais")
print("-" * 40)
resultado = subprocess.run([sys.executable, "backup_dados.py"], capture_output=False)
if resultado.returncode != 0:
    print("ERRO no backup. Abortando por segurança.")
    sys.exit(1)

# ETAPA 2 — Coleta obrigatória (sem Apify)
print("\n📡 ETAPA 2 — Coleta obrigatória")
print("-" * 40)

coletas_obrigatorias = [
    ("Coletando Google Reviews...", "coletar_google.py"),
    ("Coletando notícias...", "coletar_noticias.py"),
]

for mensagem, script in coletas_obrigatorias:
    print(f"\n{mensagem}")
    resultado = subprocess.run([sys.executable, script], capture_output=False)
    if resultado.returncode != 0:
        print(f"ERRO em {script}. Abortando.")
        sys.exit(1)

# ETAPA 3 — Coleta opcional (Apify)
print("\n📡 ETAPA 3 — Coleta via Apify (opcional)")
print("-" * 40)

coletas_apify = [
    ("Coletando TripAdvisor...", "coletar_tripadvisor.py"),
    ("Coletando iFood...", "coletar_ifood.py"),
]

apify_ok = True
for mensagem, script in coletas_apify:
    print(f"\n{mensagem}")
    resultado = subprocess.run([sys.executable, script], capture_output=False)
    if resultado.returncode != 0:
        print(f"⚠️  {script} falhou — limite Apify possivelmente esgotado.")
        print("    Usando dados existentes dos CSVs anteriores.")
        apify_ok = False

if not apify_ok:
    print("\n⚠️  Coleta Apify incompleta — continuando com dados existentes.")

# ETAPA 4 — Processamento
print("\n⚙️  ETAPA 4 — Processamento")
print("-" * 40)

env = os.environ.copy()
env["TRANSFORMERS_OFFLINE"] = "1"

processamentos = [
    ("Unificando dados...", "unificar_dados.py"),
    ("Classificando sentimento...", "classificar_sentimento.py"),
    ("Atualizando banco local...", "criar_banco.py"),
    ("Coletando Instagram...", "coletar_instagram.py"),
    ("Classificando social...", "classificar_social.py"),
    ("Salvando notícias...", "salvar_noticias.py"),
]

for mensagem, script in processamentos:
    print(f"\n{mensagem}")
    resultado = subprocess.run([sys.executable, script], capture_output=False, env=env)
    if resultado.returncode != 0:
        print(f"ERRO em {script}. Abortando.")
        sys.exit(1)

# ETAPA 5 — Atualizar Supabase
print("\n☁️  ETAPA 5 — Atualizando Supabase")
print("-" * 40)
resultado = subprocess.run([sys.executable, "resetar_reviews.py"], capture_output=False)
if resultado.returncode != 0:
    print("ERRO ao atualizar Supabase. Abortando.")
    sys.exit(1)

# ETAPA 6 — Validação final
print("\n✅ ETAPA 6 — Validação final")
print("-" * 40)
resultado = subprocess.run([sys.executable, "validar_dados.py"], capture_output=False)
if resultado.returncode != 0:
    print("\n❌ VALIDAÇÃO FALHOU — dados podem estar incorretos!")
    print("Os backups estão disponíveis na pasta /backups")
    sys.exit(1)

print("\n" + "=" * 50)
if apify_ok:
    print("✅ Atualização completa concluída com sucesso!")
else:
    print("⚠️  Atualização parcial concluída — Apify indisponível.")
    print("   TripAdvisor e iFood não foram atualizados.")
print("=" * 50)