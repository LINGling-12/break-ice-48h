# day2.py  ── 双均线策略 vs 买入持有（已兼容在线/模拟）
import akshare as ak, pandas as pd, matplotlib.pyplot as plt, numpy as np

# 1. 数据获取（与 day1 同接口，保证连贯）
try:
    df = ak.index_zh_a_hist(symbol="HS300", period="daily", start_date="20230901")
    if df is None or df.empty:
        raise RuntimeError("接口空表")
    price_col = '收盘'
except Exception as e:
    print("✘ 在线失败，切换模拟数据：", e)
    dates = pd.date_range("2023-09-01", "2024-09-20", freq="B")
    idx = [3800]
    for _ in dates[1:]:
        idx.append(idx[-1] * (1 + (np.random.rand() - 0.5) * 0.02))
    df = pd.DataFrame({"日期": dates, "收盘": idx})
    price_col = '收盘'

# 2. 日期统一 & 基础字段
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期").reset_index(drop=True)
df["pct"] = df[price_col].pct_change()

# 3. 双均线信号
df["ma5"]  = df[price_col].rolling(5).mean()
df["ma20"] = df[price_col].rolling(20).mean()
df["pos"]  = (df["ma5"] > df["ma20"]).astype(int)
df["str"]  = df["pos"].shift(1) * df["pct"]   # 当日持仓才享受收益

# 4. 累计净值
df[["pct", "str"]] = df[["pct", "str"]].fillna(0)
hold = (df["pct"] + 1).cumprod()
stra = (df["str"]  + 1).cumprod()

# 5. 画图
plt.rcParams["font.family"] = "SimHei"
plt.figure(figsize=(12, 6))
plt.plot(df["日期"], hold, label="买入持有")
plt.plot(df["日期"], stra, label="双均线策略", linewidth=2)
plt.legend()
plt.title("Day2 闭环：策略 vs 指数")
plt.tight_layout()
plt.savefig("vs.png", dpi=300)
plt.show()

# 6. 终端打印关键指标
print("累计收益——买入持有:", hold.iloc[-1] - 1)
print("累计收益——双均线:", stra.iloc[-1] - 1)