lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

calc_proj = '''            # Calcular projecao salao para o mes atual
            import numpy as _np_proj
            import calendar as _cal_proj
            from datetime import date as _date_proj
            _hoje_proj = _date_proj.today()
            _mes_proj = _hoje_proj.month
            _ano_proj = _hoje_proj.year
            _dias_no_mes_proj = _cal_proj.monthrange(_ano_proj, _mes_proj)[1]
            df_mes_proj = df_vd[
                (df_vd["data"].dt.month == _mes_proj) &
                (df_vd["data"].dt.year == _ano_proj) &
                df_vd["filial_curta"].isin(filiais_sel)
            ].copy()
            proj_total = 0
            if len(df_mes_proj) > 0:
                _dias_real_proj = int(df_mes_proj["data"].dt.day.max())
                _venda_real_proj = df_mes_proj["venda_salao"].sum()
                df_hist_proj = df_vd[(df_vd["venda_salao"] > 0)].copy()
                df_hist_proj["dow"] = df_hist_proj["data"].dt.dayofweek
                df_hist_proj["mes_n"] = df_hist_proj["data"].dt.month
                _proj_rest = 0
                for _fil_p in filiais_sel:
                    _dff_p = df_hist_proj[df_hist_proj["filial_curta"] == _fil_p].copy()
                    if len(_dff_p) < 30:
                        continue
                    _clean_p = []
                    for _dw in _dff_p["dow"].unique():
                        _g = _dff_p[_dff_p["dow"] == _dw]
                        _q1 = _g["venda_salao"].quantile(0.10)
                        _q3 = _g["venda_salao"].quantile(0.90)
                        _iqr = _q3 - _q1
                        _clean_p.append(_g[(_g["venda_salao"] >= _q1 - 1.5*_iqr) & (_g["venda_salao"] <= _q3 + 1.5*_iqr)])
                    _dff_c = pd.concat(_clean_p)
                    _media_p = _dff_c["venda_salao"].mean()
                    _fdow_p = _dff_c.groupby("dow")["venda_salao"].mean() / _media_p
                    _fmes_p = _dff_c.groupby("mes_n")["venda_salao"].mean() / _media_p
                    _frec_p = _dff_c[_dff_c["data"] >= _dff_c["data"].max() - pd.Timedelta(days=28)]["venda_salao"].mean() / _media_p
                    _frec_p = float(_np_proj.clip(_frec_p, 0.85, 1.15))
                    for _d in range(_dias_real_proj + 1, _dias_no_mes_proj + 1):
                        _dt = pd.Timestamp(_ano_proj, _mes_proj, _d)
                        _proj_rest += _media_p * _fdow_p.get(_dt.dayofweek, 1.0) * _fmes_p.get(_mes_proj, 1.0) * _frec_p
                proj_total = _venda_real_proj + _proj_rest

'''

# Inserir antes do bloco Layout 2x3
idx = next(i for i, l in enumerate(lines) if '# Layout 2x3 — grid CSS' in l)
lines.insert(idx, calc_proj)
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — inserido na linha {idx+1}')
