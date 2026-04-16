from LeIA import SentimentIntensityAnalyzer

analisador = SentimentIntensityAnalyzer()

testes = [
    ("Foi uma decepção...restaurante Caro e sem qualidade, camarão estava meio borrachudo e meu macarrão veio seco, a única coisa boa foi a salada q servem de entrada... não volto", 1),
    ("Pratos muito bem servidos e muito gostosos. O pãozinho quentinho que servem é uma delícia. o atendimento ê razoável, não são muito amigáveis.", 5),
    ("Tudo foi perfeito desde o atendimento, todos os funcionários foram super atenciosos, simpáticos e bem solícitos. A refeição estava muito gostosa.", 5),
    ("A porção é muito pequena. A sopa era de frango com gnocchi, se veio três gnocchi é muito.", 2),
    ("Pouco crouton", 4),
    ("Não conhecia o local. Ficamos surpresos com a qualidade da comida e com o atendimento. Alem do custo bastante justo. Recomendo demais.", 5),
    ("Um pouco salgado", 3),
    ("Amei o chicken alfredo - serviu bem 3 pessoas - o pãozinho de alho faltou o crocante em cima mas estava tudo bem gostoso!", 5),
]

print(f"{'Nota':<6} {'LeIA':<12} {'Score':<8} {'Texto[:60]'}")
print("-" * 80)
for texto, nota in testes:
    scores = analisador.polarity_scores(texto)
    compound = scores["compound"]
    if compound >= 0.05:
        sentimento = "Positivo"
    elif compound <= -0.05:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"
    print(f"{nota:<6} {sentimento:<12} {compound:<8.3f} {texto[:60]}")