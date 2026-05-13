import subprocess, sys, os
env = os.environ.copy()
env["TRANSFORMERS_OFFLINE"] = "1"
for mensagem, script in [
    ("Unificando dados...", "unificar_dados.py"),
    ("Classificando sentimento...", "classificar_sentimento.py"),
    ("Atualizando banco local...", "criar_banco.py"),
    ("Atualizando Supabase...", "resetar_reviews.py"),
    ("Validando...", "validar_dados.py"),
]:
    print(mensagem)
    r = subprocess.run([sys.executable, script], capture_output=False, env=env)
    if r.returncode != 0:
        print(f"ERRO em {script}")
        sys.exit(1)
print("Concluido!")
