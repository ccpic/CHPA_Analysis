from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition_htn = "[TC II] in ('C03 DIURETICS|利尿剂', \
'C07 BETA BLOCKING AGENTS|β受体阻断剂',\
'C09 RENIN-ANGIOTEN SYST AGENT|作用于肾素-血管紧张素系统的药物',\
'C08 CALCIUM ANTAGONISTS|钙离子拮抗剂',\
'C02 ANTIHYPERTENSIVES|抗高血压药')"


sql = "SELECT * FROM " + table_name + " WHERE " + condition_htn
df = pd.read_sql(sql=sql, con=engine)

print("Finished importing...")

D_CLASS = {
    "C08A0": "CCB",
    "C07A0": "BB",
    "C09C0": "ARB",
    "C09D9": "ARNI",
    "C09D1": "A+D FDC",
    "C03A2": "DU",
    "C09D3": "A+C FDC",
    "C09B3": "A+C FDC",
    "C09A0": "ACEI",
    "C03A7": "DU",
    "C03A1": "DU",
    "C03A3": "DU",
    "C09B1": "A+D FDC",
}

D_COLOR = {
    "CCB": "navy",
    "BB": "crimson",
    "ARB": "darkgreen",
    "ACEI": "olivedrab",
    "ARNI": "deepskyblue",
    "A+C FDC": "Purple",
    "A+D FDC": "Violet",
    "DU": "darkorange",
    "Others": "grey",
}

df["CLASS"] = df["TC IV"].str[:5].map(D_CLASS).fillna("Others")

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)
df = df.drop(
    df[df["PACKAGE"].str.contains(" AMP | VIAL | DRY | IV | INFUSION ")].index
)  # 删除针剂

D_REMOVE = {
    "可乐定": "*",
    "乌拉地尔": ["25MG", "50MG"],
    "乌拉地尔氯化钠": "*",
    "硝普钠": "*",
    "洛非西定": "*",
    "氨苯蝶啶": "*",
    "布美他尼": "*",
    "托伐普坦": "*",
    "马来酸依那普利叶酸片": "*",
    "非奈利酮": "*",
}
for key, value in D_REMOVE.items():
    if value == "*":
        df = df.drop(df[df["MOLECULE"] == key].index)
    else:
        df = df.drop(df[(df["MOLECULE"] == key) & (df["STRENGTH"].isin(value))].index)
print("Finished removing...")

D_RENAME = {
    "复方盐酸阿米洛利片": "阿米洛利氢氯噻嗪",
    "复方卡托普利": "卡托普利氢氯噻嗪",
    "阿利吉仑片": "阿利吉仑",
    "氨氯地平贝那普利(II)": "贝那普利氨氯地平",
    "培哚普利氨氯地平片(III)": "培哚普利氨氯地平",
    "坎地氢噻": "坎地沙坦氢氯噻嗪",
    "奥美沙坦酯氨氯地平片": "奥美沙坦氨氯地平",
    "氨氯地平叶酸片(Ⅱ)": "氨氯地平叶酸",
    "比索洛尔氨氯地平片": "比索洛尔氨氯地平",
    "美阿沙坦钾片": "美阿沙坦",
    "尼群洛尔": "尼群地平阿替洛尔",
    "奥美沙坦酯氢氯噻嗪": "奥美沙坦氢氯噻嗪",
    "氯沙坦钾": "氯沙坦",
}
df["MOLECULE"] = df["MOLECULE"].map(D_RENAME).fillna(df["MOLECULE"])

print("Finished renaming...")

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

df.to_excel("test.xlsx")
df_ptd = pd.read_excel("高血压PTD系数_0712.xlsx")
for row in df_ptd.iterrows():
    mask = (
        (df["MOLECULE"] == row[1]["MOLECULE"])
        & (df["STRENGTH"] == row[1]["STRENGTH"])
        & (df["UNIT"] == "PTD")
    )
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / row[1]["INDEX"]

print("Finished converting PTD...")


df.loc[df["CLASS"] == "BB", "AMOUNT"] = df.loc[df["CLASS"] == "BB", "AMOUNT"] * 0.55
df.loc[df["CLASS"] == "ARNI", "AMOUNT"] = df.loc[df["CLASS"] == "ARNI", "AMOUNT"] * 0.7
df.loc[df["CLASS"] == "DU", "AMOUNT"] = df.loc[df["CLASS"] == "DU", "AMOUNT"] * 0.8

print("Finished adding weights...")

r = CHPA(df, name="口服降压药市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(
#     index="CLASS", unit_change="百万", label_threshold=0.01, color_dict=D_COLOR
# )
# r.plot_overall_performance(
#     index="CLASS",
#     unit_change="百万",
#     label_threshold=0.01,
#     color_dict=D_COLOR,
#     unit="PTD",
# )
# r.plot_overall_performance(
#     index="CLASS",
#     unit_change="百万",
#     label_threshold=0.01,
#     color_dict=D_COLOR,
#     period="QTR",
# )
# r.plot_overall_performance(
#     index="CLASS",
#     unit_change="百万",
#     label_threshold=0.01,
#     color_dict=D_COLOR,
#     unit="PTD",
#     period="QTR",
# )

# r.plottable_latest(index="CLASS", unit="Value", show_total=False, focus="ARNI")
# r.plottable_latest(index="CLASS", unit="PTD", show_total=False, focus="ARNI")

# r.plottable_annual(index="CLASS", unit="Value")
# r.plottable_annual(index="CLASS", unit="PTD")

# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Value",
#     unit_change="百万",
#     label_limit=20,
#     hue="CLASS",
#     focus="阿利沙坦",
# )
# r.plot_size_diff(
#     index="MOLECULE",
#     unit="PTD",
#     unit_change="百万",
#     label_topy=5,
#     label_limit=20,
#     hue="CLASS",
#     focus="阿利沙坦",
# )

# r.plot_share_gr(
#     index="MOLECULE",
#     unit="Value",
#     ylim=(-0.4, 0.6),
#     label_limit=20,
#     hue="CLASS",
#     focus="阿利沙坦",
# )
# r.plot_share_gr(
#     index="MOLECULE",
#     unit="PTD",
#     label_topy=5,
#     label_limit=20,
#     ylim=(-0.4, 0.8),
#     hue="CLASS",
#     focus="阿利沙坦",
# )

# r.plottable_latest(index="MOLECULE", unit="Value", hue="CLASS", focus="沙库巴曲缬沙坦")
# r.plottable_latest(index="MOLECULE", unit="PTD", hue="CLASS", focus="沙库巴曲缬沙坦")

# r.plot_share_trend(index="MOLECULE", unit="Value")
# r.plot_share_trend(index="MOLECULE", unit="PTD")

# r.plottable_annual(index="MOLECULE", unit="Value")
# r.plottable_annual(index="MOLECULE", unit="PTD")

# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Value",
#     unit_change="百万",
#     label_limit=20,
#     hue="CLASS",
#     focus="XIN LI TAN (SI6)",
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="PTD",
#     unit_change="百万",
#     label_topy=7,
#     label_limit=20,
#     hue="CLASS",
#     focus="XIN LI TAN (SI6)",
# )

# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Value",
#     label_topy=5,
#     ylim=(-0.5, 1),
#     label_limit=20,
#     hue="CLASS",
#     focus="XIN LI TAN (SI6)",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     unit="PTD",
#     label_topy=5,
#     label_limit=20,
#     ylim=(-0.5, 1),
#     hue="CLASS",
#     focus="XIN LI TAN (SI6)",
# )


# r.plottable_latest(
#     index="PRODUCT",
#     unit="Value",
#     hue=("MOLECULE", "CORPORATION"),
#     focus="ENTRESTO (NVR)",
# )
# r.plottable_latest(
#     index="PRODUCT", unit="PTD", hue=("MOLECULE", "CORPORATION"), focus="ENTRESTO (NVR)"
# )

# r.plot_share_trend(index="PRODUCT", unit="Value")
# r.plot_share_trend(index="PRODUCT", unit="PTD")

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="PTD")


df = df[df["CLASS"] == "ARNI"]
r = CHPA(df, name="ARNI市场", date_column="DATE", period_interval=3)

# r.plot_trend_with_gr(
#     index=None, unit_change="百万", color_dict={"AMOUNT": "Navy"}, width=6, height=5
# )
# r.plot_trend_with_gr(
#     index=None,
#     unit_change="百万",
#     unit="PTD",
#     color_dict={"AMOUNT": "Crimson"},
#     width=6,
#     height=5,
# )

# r.plot_trend_with_gr(
#     index=None,
#     unit_change="百万",
#     color_dict={"AMOUNT": "Navy"},
#     period="QTR",
#     width=15,
#     height=6,
# )
# r.plot_trend_with_gr(
#     index=None,
#     unit_change="百万",
#     unit="PTD",
#     color_dict={"AMOUNT": "Crimson"},
#     period="QTR",
#     width=15,
#     height=6,
# )

r.plottable_latest(
    index="PACKAGE",
    unit="Value",
    hue="CORPORATION",
)
r.plottable_latest(
    index="PACKAGE",
    unit="PTD",
    hue="CORPORATION",
)
