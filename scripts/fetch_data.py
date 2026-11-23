"""Holt Daten für alle S&P-500-Aktien (yfinance, kein API-Key nötig) und schreibt data/*.json"""
import json, sys, time, io, pandas as pd, yfinance as yf, requests
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "data"; OUT.mkdir(exist_ok=True)
limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

def table():
    h = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                     headers={"User-Agent": "Mozilla/5.0"}).text
    return pd.read_html(io.StringIO(h))[0]

def row(df, *names):
    for n in names:
        if n in df.index: return [None if pd.isna(v) else float(v) for v in df.loc[n].iloc[::-1]]
    return []

def fetch(sym):
    t = yf.Ticker(sym.replace(".", "-")); i = t.info
    h = t.history(period="10y", interval="1wk")["Close"].dropna()
    fin = t.financials
    cf = t.cashflow.reindex(columns=fin.columns)  # gleiche Jahre wie fin
    div_y = {}
    for d, v in t.dividends.items(): div_y[d.year] = div_y.get(d.year, 0) + float(v)
    return {
        "symbol": sym, "name": i.get("longName", sym), "sector": i.get("sector", ""),
        "industry": i.get("industry", ""), "desc": i.get("longBusinessSummary", ""),
        "marketCap": i.get("marketCap"), "beta": i.get("beta"),
        "divYield": i.get("dividendYield"), "pe": i.get("trailingPE"),
        "ps": i.get("priceToSalesTrailing12Months"), "debtToEquity": i.get("debtToEquity"),
        "prices": [[d.strftime("%Y-%m-%d"), round(float(v), 2)] for d, v in h.items()],
        "years": [c.year for c in fin.columns[::-1]] if len(fin.columns) else [],
        "revenue": row(fin, "Total Revenue"), "grossProfit": row(fin, "Gross Profit"),
        "netIncome": row(fin, "Net Income"), "opCF": row(cf, "Operating Cash Flow"),
        "roe": i.get("returnOnEquity"), "roa": i.get("returnOnAssets"),
        "currentRatio": i.get("currentRatio"), "forwardPE": i.get("forwardPE"),
        "targetMeanPrice": i.get("targetMeanPrice"),
        "ebit": row(fin, "EBIT", "Operating Income"), "interest": row(fin, "Interest Expense"),
        "dps": div_y,
    }

idx = []
for n, (_, r) in enumerate(table().iterrows()):
    if limit and n >= limit: break
    s = r["Symbol"]
    try:
        d = fetch(s); (OUT / f"{s}.json").write_text(json.dumps(d))
        idx.append({"s": s, "n": d["name"], "sec": d["sector"]}); print("ok", s)
    except Exception as e: print("fail", s, e)
    time.sleep(0.5)
(OUT / "index.json").write_text(json.dumps(idx))
