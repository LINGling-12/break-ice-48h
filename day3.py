# day3_three.py  —— 三根曲线完整版
import akshare as ak, pandas as pd, matplotlib.pyplot as plt, numpy as np, ta

# 1. 数据获取
try:
    df = ak.index_zh_a_hist(symbol="沪深300", period="daily", start_date="20230901")
    if df is None or df.empty: raise RuntimeError("空表")
    price_col = '收盘'
except Exception as e:
    print("在线失败，切换模拟数据：", e)
    dates = pd.date_range("2023-09-01", "2024-09-20", freq="B")
    idx = [3800]
    for _ in dates[1:]: idx.append(idx[-1] * (1 + (np.random.rand() - 0.5) * 0.02))
    df = pd.DataFrame({"日期": dates, "收盘": idx})
    price_col = '收盘'

# 2. 日期 & 日收益
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期").reset_index(drop=True)
df["pct"] = df[price_col].pct_change()

# 3. 均线信号
df["ma5"]  = df[price_col].rolling(5).mean()
df["ma20"] = df[price_col].rolling(20).mean()
df["pos"]  = (df["ma5"] > df["ma20"]).astype(int)
df["str"]  = df["pos"].shift(1) * df["pct"]

# 4. RSI 滤波信号
df['rsi'] = ta.momentum.rsi(df[price_col], window=14)
df['rsi_sig'] = (df['rsi'] > 50).astype(int)
df['pos_rsi'] = df['pos'] & df['rsi_sig']
df['str_rsi'] = df['pos_rsi'].shift(1) * df["pct"]

# 5. 累计净值
df[['pct', 'str', 'str_rsi']] = df[['pct', 'str', 'str_rsi']].fillna(0)
hold = (df['pct'] + 1).cumprod()
stra = (df['str'] + 1).cumprod()
stra_rsi = (df['str_rsi'] + 1).cumprod()

# 6. 三根曲线
plt.rcParams['font.family'] = 'SimHei'
plt.figure(figsize=(12, 6))
plt.plot(df['日期'], hold,    label='买入持有', linewidth=1.5)
plt.plot(df['日期'], stra,   label='原始双均线', linewidth=2)
plt.plot(df['日期'], stra_rsi, label='RSI-均线滤波', linewidth=2.5)
plt.legend()
plt.title('Day3 三根曲线对比')
plt.tight_layout()
plt.savefig('vs_three.png', dpi=300)
plt.show()

# 7. 结果
print('买入持有累计收益:', hold.iloc[-1] - 1)
print('原始均线累计收益:', stra.iloc[-1] - 1)
print('RSI-均线累计收益:', stra_rsi.iloc[-1] - 1)
