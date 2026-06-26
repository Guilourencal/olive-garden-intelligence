lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

lines[1799] = '                                    tabela = "| " + " | ".join(cols) + " |\\n"\n'
lines[1800] = '                                    tabela += "| " + " | ".join(["---"]*len(cols)) + " |\\n"\n'
del lines[1801]
del lines[1801]
del lines[1801]
lines[1801] = '                                    for row in rows[:50]:\n'
lines[1802] = '                                        tabela += "| " + " | ".join([str(v) if v is not None else "\\u2014" for v in row]) + " |\\n"\n'
del lines[1803]

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
