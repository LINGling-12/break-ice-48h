import akshare as ak, pandas as pd, matplotlib.pyplot as plt, numpy as np

# 1. 先尝试在线数据
try:
    df = ak.index_zh_a_hist(symbol="HS300", period="daily", start_date="20230901")
    if df is None or df.empty:
        raise RuntimeError("接口返回空表")
    print("✔ 在线数据行数：", len(df))
except Exception as e:
    print("✘ 在线失败，切换模拟数据：", e)
    dates = pd.date_range("2023-09-01", "2024-09-20", freq="B")
    idx = [3800]
    for _ in dates[1:]:
        idx.append(idx[-1] * (1 + (np.random.rand() - 0.5) * 0.02))   # 改用 np
    df = pd.DataFrame({"日期": dates, "收盘": idx})

# 2. 统一日期 & 计算收益
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期").reset_index(drop=True)
df["pct"] = df["收盘"].pct_change()

# 3. 累计净值 & 画图
cum = (df["pct"].fillna(0) + 1).cumprod()
plt.rcParams["font.family"] = "SimHei"
plt.figure(figsize=(12, 6))
plt.plot(df["日期"], cum, linewidth=2, label="HS300 累计收益")
plt.legend()
plt.title("Day1 闭环:沪深300累计收益(修复版)")
plt.tight_layout()
plt.savefig("hs300.png", dpi=300)
plt.show()