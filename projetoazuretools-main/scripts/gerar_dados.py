"""Gera azure/data/dados.json (dados FICTÍCIOS do painel executivo).

Uso (na raiz do projeto):
    python scripts/gerar_dados.py
"""
import json
from pathlib import Path

MESES = ["Nov/25", "Dez/25", "Jan/26", "Fev/26", "Mar/26", "Abr/26",
         "Mai/26", "Jun/26", "Jul/26", "Ago/26", "Set/26", "Out/26"]

# Receita total realizada (R$ mi). Out/26 = 4,2 e Set/26 = 4,2 / 1,083 (+8,3%).
REALIZADO_TOTAL = [3.02, 3.10, 2.95, 3.18, 3.30, 3.41,
                   3.49, 3.57, 3.66, 3.74, 3.8781, 4.20]
TICKET_TOTAL = [1085, 1092, 1078, 1101, 1120, 1138,
                1150, 1163, 1181, 1198, 1214.5, 1240]
INAD_TOTAL = [2.6, 2.7, 3.0, 2.9, 2.8, 2.7,
              2.6, 2.5, 2.6, 2.7, 2.8, 3.4]

# Participação de cada região em Out/26 (R$ mi: 1,9 / 1,1 / 0,7 / 0,4 / 0,1).
REGIOES = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
SHARE_OUT = [1.9 / 4.2, 1.1 / 4.2, 0.7 / 4.2, 0.4 / 4.2, 0.1 / 4.2]
DRIFT = [0.0020, 0.0005, -0.0010, -0.0010, -0.0005]   # soma zero
META_OUT = [0.975, 0.955, 0.93, 0.98, 0.90]           # realizado / orçado em Out/26
META_ONDA = [0.02, 0.015, -0.01, 0.01, 0.03, 0.0, 0.01, 0.02, 0.005, 0.015, 0.01, 0.0]
TICKET_FATOR = [1.08, 1.02, 0.92, 0.97, 0.88]
INAD_FATOR = [0.85, 0.90, 1.20, 1.00, 1.30]


def r(valor, casas):
    return round(valor, casas)


series = {}
total_orc = [0.0] * 12
for i, nome in enumerate(REGIOES):
    real, orc, tk, ina = [], [], [], []
    for m in range(12):
        share = SHARE_OUT[i] + DRIFT[i] * (11 - m)
        rv = REALIZADO_TOTAL[m] * share
        fator = META_OUT[i] + META_ONDA[m] * (1 if m < 11 else 0)
        ov = rv / fator
        real.append(r(rv, 4))
        orc.append(r(ov, 4))
        tk.append(r(TICKET_TOTAL[m] * TICKET_FATOR[i], 1))
        ina.append(r(INAD_TOTAL[m] * INAD_FATOR[i], 2))
        total_orc[m] += ov
    series[nome] = {"realizado": real, "orcado": orc,
                    "ticket": tk, "inadimplencia": ina}

series_todas = {
    "realizado": [r(v, 4) for v in REALIZADO_TOTAL],
    "orcado": [r(v, 4) for v in total_orc],
    "ticket": TICKET_TOTAL,
    "inadimplencia": INAD_TOTAL,
}

dados = {
    "aviso": "dados fictícios",
    "meses": MESES,
    "regioes": ["Todas"] + REGIOES,
    "series": {"Todas": series_todas, **series},
}

destino = Path(__file__).resolve().parent.parent / "azure" / "data" / "dados.json"
destino.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")

meta = series_todas["realizado"][-1] / series_todas["orcado"][-1] * 100
print(f"Gravado em {destino}")
print(f"Out/26: receita {series_todas['realizado'][-1]} mi | meta {meta:.1f}%")
