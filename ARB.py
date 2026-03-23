from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd
from chart.figure import GridFigure
import matplotlib.pyplot as plt

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

# ARB单方
condition_arb = (
    "[TC III] in ('C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"
)

# RAAS单方市场
condition_raasi_plain = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    # "'C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"
    # "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药')"
)

# RAAS单方市场+ARNI
condition_raasi_plain_arni = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"
    " or MOLECULE = 'SACUBITRIL+VALSARTAN|沙库巴曲缬沙坦'"
)

# RAAS市场除沙库巴曲缬沙坦
condition_arni_excl = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    "'C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药' ,"
    "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药')  ,"
    "and MOLECULE != '沙库巴曲缬沙坦|SACUBITRIL+VALSARTAN' and MOLECULE !='ENALAPRIL+FOLIC ACID|马来酸依那普利叶酸片'"
)

# RAAS+ARNI市场 含复方
condition_raasi = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    "'C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药' ,"
    "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药') and MOLECULE !='ENALAPRIL+FOLIC ACID|马来酸依那普利叶酸片'"
)

# 诺欣妥+信立坦
# condition = "[MOLECULE] in ('沙库巴曲,缬沙坦|SACUBITRIL+VALSARTAN', '阿利沙坦|ALLISARTAN ISOPROXIL')"

# 所有高血压药
# condition = "[TC II]  in ('C03 DIURETICS|利尿剂', " \
#             "'C07 BETA BLOCKING AGENTS|β受体阻断剂', " \
#             "'C08 CALCIUM ANTAGONISTS|钙离子拮抗剂', " \
#             "'C09 RENIN-ANGIOTEN SYST AGENT|作用于肾素-血管紧张素系统的药物')"


# ！！！！！注意修改condition，只用修改复方和单方的condition，即condition_raasi或者condition_raasi_plain_arni
condition = condition_raasi
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)
# print(df['MOLECULE'].unique())

# for col in ['TC III', 'MOLECULE']:
#     df[col] = df[col].map(d_rename).fillna('其他')

# df['TC III'] = df['TC III'].str.split('|').str[1]
df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
# df["PRODUCT"] = (
#     (df["PRODUCT"].str.split("|").str[0])
#     + "（"
#     + df["PRODUCT"].str.split("|").str[1].str[-3:]
#     + "）"
# )
# df["PRODUCT_CORP"] = (
#     df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
#     + "\n"
#     + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
# )
D_RENAME = {
    "复方盐酸阿米洛利片": "阿米洛利氢氯噻嗪",
    "复方卡托普利": "卡托普利氢氯噻嗪",
    "阿利吉仑片": "阿利吉仑",
    "氨氯地平贝那普利(II)": "贝那普利氨氯地平",
    "培哚普利氨氯地平片(III)": "培哚普利氨氯地平",
    "坎地氢噻": "坎地沙坦氢氯噻嗪",
    "奥美沙坦酯氨氯地平片": "奥美沙坦氨氯地平",
    "奥美沙坦酯氨氯地平": "奥美沙坦氨氯地平",
    "氨氯地平叶酸片(Ⅱ)": "氨氯地平叶酸",
    "比索洛尔氨氯地平片": "比索洛尔氨氯地平",
    "美阿沙坦钾片": "美阿沙坦",
    "尼群洛尔": "尼群地平阿替洛尔",
    "奥美沙坦酯氢氯噻嗪": "奥美沙坦氢氯噻嗪",
    "氯沙坦钾": "氯沙坦",
    "氯沙坦钾氢氯噻嗪": "氯沙坦氢氯噻嗪",
    "阿利沙坦酯氨氯地平": "阿利沙坦氨氯地平",
}
df["MOLECULE"] = df["MOLECULE"].map(D_RENAME).fillna(df["MOLECULE"])

vbp_molecules = [
    "厄贝沙坦",
    "缬沙坦",
    "氯沙坦",
    "奥美沙坦",
    "坎地沙坦",
    "福辛普利",
    "卡托普利",
    "赖诺普利",
    "依那普利",
    "培哚普利",
    "贝那普利",
    "替米沙坦",
    "缬沙坦氨氯地平",
    "缬沙坦氢氯噻嗪",
    "厄贝沙坦氢氯噻嗪",
    "氯沙坦氢氯噻嗪",
    "奥美沙坦氨氯地平",
    "奥美沙坦氢氯噻嗪",
    "替米沙坦氢氯噻嗪",
]
mask = df["MOLECULE"].isin(vbp_molecules)
df.loc[mask, "VBP"] = "VBP品种"
mask = ~df["MOLECULE"].isin(vbp_molecules)
df.loc[mask, "VBP"] = "非VBP品种"

# df = df[df["VBP"] == "非VBP品种"]

# ARNI销量打7折
if condition == condition_raasi or condition_raasi_plain_arni:
    mask = df["MOLECULE"] == "沙库巴曲缬沙坦"
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] * 0.8


mask = df["UNIT"] == "Volume (Counting Unit)"
df_ptd = df.loc[mask, :]
df_ptd["UNIT"] = "PTD"
df = pd.concat([df, df_ptd])

df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)

df_ptd = pd.read_excel("高血压PTD系数_0821.xlsx")
for row in df_ptd.iterrows():
    mask = (
        (df["MOLECULE"] == row[1]["MOLECULE"])
        & (df["STRENGTH"] == row[1]["STRENGTH"])
        & (df["UNIT"] == "PTD")
    )
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / row[1]["INDEX"]

print("Finished converting PTD...")

mask = df["TC III"] == "C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药"
df.loc[mask, "TC III"] = "ACEI"
mask = df["TC III"] == "C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药"
df.loc[mask, "TC III"] = "ARB"
mask = df["TC IV"].isin(
    [
        "C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药",
        "C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药",
    ]
)
df.loc[mask, "TC III"] = "A+C"
mask = df["TC IV"].isin(
    [
        "C09D1 AT2 ANTG COMB C2 &/O DIU|血管紧张素II拮抗剂与抗高血压药（C02）和/利尿剂联合用药（C03）",
        "C09B1 ACE INH COMB+A-HYP/DIURET|血管紧张素转换酶掏抑制剂，与抗高血压药（C02）和/或利尿药（C03）联合用药",
    ]
)
df.loc[mask, "TC III"] = "A+D"
mask = df["MOLECULE"].str.contains("沙库巴曲")
df.loc[mask, "TC III"] = "ARNI"

df["CLASS"] = df["TC III"]

# d_rename = {
#     "ENTRESTO (NVR)": "诺欣妥\n沙库巴曲缬沙坦",
#     "XIN LI TAN (SI6)": "信立坦\n阿利沙坦",
#     "AMLODIPINE BESYLAT (S5O)": "地奥氨贝\n贝那普利氨氯地平",
#     "BAI AN XIN (GRU)": "百安新\n贝那普利氨氯地平",
#     "OLMETEC PLUS (DSC)": "复傲坦\n奥美沙坦氢氯噻嗪",
#     "COVERAM (SVR)": "开素达\n培哚普利氨氯地平",
#     "BIPREL (TSV)": "百普乐\n培哚普利吲达帕胺",
#     "RUI SU TAN (R7R)": "瑞素坦\n雷米普利",
#     "TIAN SHU PING (NJ2)": "天舒平\n奥美沙坦氨氯地平",
#     "RUI TUO PING (JSH)": "瑞妥平\n阿齐沙坦",
#     "EDARBI (TAK)": "易达比\n美阿沙坦",
# }

# df["PRODUCT"] = df["PRODUCT"].map(d_rename).fillna(df["PRODUCT"])

# writer = pd.ExcelWriter('output.xlsx')
# df.to_excel(writer,'Sheet1')
# writer.save()

# dimension = "MOLECULE"
# target = "阿利沙坦"
# filter_list = ["缬沙坦", "厄贝沙坦", "氯沙坦", "奥美沙坦", "坎地沙坦", "阿利沙坦", "缬沙坦,氨氯地平", "厄贝沙坦,氢氯噻嗪", "培哚普利", "贝那普利,氨氯地平"]
# # filter_list = ["缬沙坦", "厄贝沙坦", "氯沙坦", "奥美沙坦", "坎地沙坦", "阿利沙坦", "培哚普利" , '贝那普利', '替米沙坦']
# # dimension = "PRODUCT"
# # target = "信立坦"
# # filter_list = ["代文", "安博维", "雅施达", "倍博特", "科素亚", "傲坦", "信立坦", '百安新']
# # filter_list = ["代文", "安博维", "雅施达", "洛汀新", "科素亚", "傲坦", "信立坦"]
# r.plot_share_trend(dimension=dimension, column=target, show_list=filter_list)
# r.plot_share_trend(dimension=dimension, column=target, period="QTR", show_list=filter_list)
# r.plot_share_trend(dimension=dimension, column=target, unit="Volume (Std Counting Unit)", show_list=filter_list)
# r.plot_share_trend(
#     dimension=dimension, column=target, period="QTR", unit="Volume (Std Counting Unit)", show_list=filter_list
# )
# r.plot_overall_performance(dimension='MOLECULE')
# r.plot_overall_performance(dimension='MOLECULE', unit='Volume (Std Counting Unit)')
# r.plot_annual_performance(dimension='MOLECULE', sorter=['缬沙坦', '厄贝沙坦', '氯沙坦钾', '替米沙坦', '坎地沙坦', '奥美沙坦', '阿利沙坦', '培哚普利', '贝那普利', '其他'])
# r.plot_annual_performance(dimension='MOLECULE', unit='Volume (Counting Unit)', sorter=['缬沙坦', '厄贝沙坦', '氯沙坦钾', '替米沙坦', '坎地沙坦', '奥美沙坦', '阿利沙坦', '培哚普利', '贝那普利', '其他'])


###前面除condition外不动
FOCUS_MOLECULES = ["阿利沙坦", "阿利沙坦氨氯地平", "沙库巴曲缬沙坦"]
FOCUS_PRODUCTS = [
    "XIN LI TAN (SI6)",
    "ENTRESTO (NVR)",
    "FU LI TAN (SI6)",
]

## RAAS+ARNI市场和RAAS市场分析
market_configs = [
    {
        "filter": None,
        "name": "RAAS+ARNI市场",
        "sorter": ["ARB", "ACEI", "A+C", "A+D", "ARNI"],
    },
    {
        "filter": ["ARB", "ACEI", "A+C", "A+D"],
        "name": "RAAS市场",
        "sorter": ["ARB", "ACEI", "A+C", "A+D", "ARNI"],
    },
]

for config in market_configs:
    if config["filter"] is None:
        df2 = df
    else:
        df2 = df[df["TC III"].isin(config["filter"])]
    r = CHPA(df2, name=config["name"], date_column="DATE", period_interval=3)

    r.plot_overall_performance_dual(
        index="TC III",
        unit_change="亿",
        label_threshold=0.01,
        fontsize=11,
        width=15,
        height=6,
        sorter=config["sorter"],
    )

    r.plot_overall_performance(
        index="TC III", sorter=config["sorter"], unit_change="亿"
    )
    r.plot_overall_performance(
        index="TC III",
        unit="PTD",
        sorter=config["sorter"],
        unit_change="亿",
    )

    r.plot_overall_performance(
        index="TC III",
        sorter=config["sorter"],
        unit_change="亿",
        period="QTR",
    )
    r.plot_overall_performance(
        index="TC III",
        unit="PTD",
        sorter=config["sorter"],
        unit_change="亿",
        period="QTR",
    )

    r.plot_overall_performance_dual(
        index="VBP",
        unit_change="亿",
        sorter=["VBP品种", "非VBP品种"],
        label_threshold=0.01,
        fontsize=11,
        width=15,
        height=6,
    )

    r.plot_size_diff_dual(
        index="MOLECULE",
        unit_change=("亿", "亿"),
        label_limit=15,
        label_topy=3,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plot_size_diff(
        index="MOLECULE",
        unit="Value",
        unit_change="亿",
        label_limit=20,
        label_topy=6,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plot_size_diff(
        index="MOLECULE",
        unit="PTD",
        unit_change="亿",
        label_limit=20,
        label_topy=9,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plot_share_gr(
        index="MOLECULE",
        unit="Value",
        ylim=(-0.4, 0.6),
        label_topy=6,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )
    r.plot_share_gr(
        index="MOLECULE",
        unit="PTD",
        ylim=(-0.4, 0.6),
        label_topy=6,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plottable_latest(
        index="MOLECULE",
        unit="Value",
        focus=FOCUS_MOLECULES,
        hue=("TC III", "VBP"),
    )

    r.plottable_latest(
        index="MOLECULE",
        unit="PTD",
        focus=FOCUS_MOLECULES,
        hue=("TC III", "VBP"),
    )

    r.plot_share_trend(
        index="MOLECULE",
        focus=FOCUS_MOLECULES,
    )
    r.plot_share_trend(
        index="MOLECULE",
        focus=FOCUS_MOLECULES,
        unit="PTD",
    )

    r.plottable_annual(index="MOLECULE", unit="Value", focus=FOCUS_MOLECULES)
    r.plottable_annual(index="MOLECULE", unit="PTD", focus=FOCUS_MOLECULES)

    r.plot_size_diff(
        index="PRODUCT",
        unit="Value",
        unit_change="亿",
        hue="CLASS",
        focus=FOCUS_PRODUCTS,
    )

    r.plot_size_diff(
        index="PRODUCT",
        unit="PTD",
        unit_change="亿",
        hue="CLASS",
        label_limit=25,
        focus=FOCUS_PRODUCTS,
    )

    r.plot_share_gr(
        index="PRODUCT",
        unit="Value",
        ylim=(-0.4, 0.6),
        label_topy=0,
        hue="CLASS",
        focus=FOCUS_PRODUCTS,
    )
    r.plot_share_gr(
        index="PRODUCT",
        unit="PTD",
        ylim=(-0.4, 0.6),
        label_topy=0,
        hue="CLASS",
        label_limit=25,
        focus=FOCUS_PRODUCTS,
    )

    r.plottable_latest(
        index="PRODUCT",
        unit="Value",
        focus=FOCUS_PRODUCTS,
        # focus = "信立坦",
        hue=("MOLECULE", "CORPORATION", "VBP"),
        period="MAT",
        topn=20,
    )
    r.plottable_latest(
        index="PRODUCT",
        unit="PTD",
        focus=FOCUS_PRODUCTS,
        # focus = "信立坦",
        hue=("MOLECULE", "CORPORATION", "VBP"),
        period="MAT",
        topn=20,
    )

    r.plot_share_trend(
        index="PRODUCT",
        focus=FOCUS_PRODUCTS,
        # focus="信立坦",
        period="MAT",
    )
    r.plot_share_trend(
        index="PRODUCT",
        focus=FOCUS_PRODUCTS,
        # focus="信立坦",
        unit="PTD",
        period="MAT",
    )

    r.plottable_annual(index="PRODUCT", unit="Value")
    r.plottable_annual(index="PRODUCT", unit="PTD")


## RAAS单方+ARNI市场和RAAS单方市场分析
market_configs = [
    {
        "filter": ["ARB", "ACEI", "ARNI"],
        "name": "RAAS单方+ARNI市场",
        "sorter": ["ARB", "ACEI", "ARNI"],
    },
    {
        "filter": ["ARB", "ACEI"],
        "name": "RAAS单方市场",
        "sorter": ["ARB", "ACEI"],
    },
]

for config in market_configs:
    df2 = df[df["TC III"].isin(config["filter"])]
    r = CHPA(df2, name=config["name"], date_column="DATE", period_interval=3)

    r.plot_overall_performance_dual(
        index="TC III",
        unit_change="亿",
        label_threshold=0.01,
        fontsize=11,
        width=15,
        height=6,
        sorter=config["sorter"],
    )

    r.plot_overall_performance(
        index="TC III", sorter=config["sorter"], unit_change="亿"
    )
    r.plot_overall_performance(
        index="TC III",
        unit="PTD",
        sorter=config["sorter"],
        unit_change="亿",
    )

    r.plot_overall_performance(
        index="TC III",
        sorter=config["sorter"],
        unit_change="亿",
        period="QTR",
    )
    r.plot_overall_performance(
        index="TC III",
        unit="PTD",
        sorter=config["sorter"],
        unit_change="亿",
        period="QTR",
    )

    r.plot_overall_performance_dual(
        index="VBP",
        unit_change="亿",
        label_threshold=0.01,
        fontsize=11,
        width=15,
        height=6,
        sorter=["VBP品种", "非VBP品种"],
    )

    r.plot_size_diff_dual(
        index="MOLECULE",
        unit_change=("亿", "亿"),
        label_limit=15,
        label_topy=3,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plot_size_diff(
        index="MOLECULE",
        unit="Value",
        unit_change="亿",
        label_limit=20,
        hue="TC III",
        width=7,
        height=6,
        focus=FOCUS_MOLECULES,
    )

    r.plot_size_diff(
        index="MOLECULE",
        unit="Value",
        unit_change="亿",
        label_limit=20,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plot_size_diff(
        index="MOLECULE",
        unit="PTD",
        unit_change="亿",
        label_limit=20,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plot_share_gr(
        index="MOLECULE",
        unit="Value",
        ylim=(-0.2, 0.6),
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )
    r.plot_share_gr(
        index="MOLECULE",
        unit="PTD",
        ylim=(-0.2, 0.6),
        label_topy=2,
        hue="VBP",
        focus=FOCUS_MOLECULES,
    )

    r.plottable_latest(
        index="MOLECULE",
        unit="Value",
        focus=FOCUS_MOLECULES,
        hue=("TC III", "VBP"),
    )
    r.plottable_latest(
        index="MOLECULE",
        unit="PTD",
        focus=FOCUS_MOLECULES,
        hue=("TC III", "VBP"),
    )

    r.plot_share_trend(
        index="MOLECULE",
        focus=FOCUS_MOLECULES,
    )
    r.plot_share_trend(
        index="MOLECULE",
        focus=FOCUS_MOLECULES,
        unit="PTD",
    )

    r.plottable_annual(
        index="MOLECULE",
        unit="Value",
        focus=FOCUS_MOLECULES,
    )
    r.plottable_annual(
        index="MOLECULE",
        unit="PTD",
        focus=FOCUS_MOLECULES,
    )

    r.plot_size_diff(
        index="PRODUCT",
        unit="Value",
        unit_change="亿",
        hue="CLASS",
        focus=FOCUS_PRODUCTS,
    )

    r.plot_size_diff(
        index="PRODUCT",
        unit="PTD",
        unit_change="亿",
        hue="CLASS",
        label_limit=25,
        focus=FOCUS_PRODUCTS,
    )

    r.plot_share_gr(
        index="PRODUCT",
        unit="Value",
        ylim=(-0.3, 0.6),
        hue="CLASS",
        label_topy=0,
        focus=FOCUS_PRODUCTS,
    )

    r.plot_share_gr(
        index="PRODUCT",
        unit="PTD",
        ylim=(-0.3, 0.6),
        label_topy=0,
        hue="CLASS",
        label_limit=25,
        focus=FOCUS_PRODUCTS,
    )

    r.plottable_latest(
        index="PRODUCT",
        unit="Value",
        focus=FOCUS_PRODUCTS,
        hue=("MOLECULE", "CORPORATION", "VBP"),
    )
    r.plottable_latest(
        index="PRODUCT",
        unit="PTD",
        focus=FOCUS_PRODUCTS,
        hue=("MOLECULE", "CORPORATION", "VBP"),
    )

    r.plot_share_trend(
        index="PRODUCT",
        focus=FOCUS_PRODUCTS,
    )
    r.plot_share_trend(
        index="PRODUCT",
        focus=FOCUS_PRODUCTS,
        unit="PTD",
    )

    r.plottable_annual(index="PRODUCT", unit="Value")
    r.plottable_annual(index="PRODUCT", unit="PTD")


## ARB单方市场
df2 = df[df["TC III"].isin(["ARB"])]
r = CHPA(df2, name="ARB单方市场", date_column="DATE", period_interval=3)


r.plot_overall_performance_dual(
    index="TC III",
    unit_change="亿",
    label_threshold=0.01,
    fontsize=11,
    width=15,
    height=6,
)

r.plot_overall_performance(index="TC III", unit_change="亿")
r.plot_overall_performance(
    index="TC III",
    unit="PTD",
    unit_change="亿",
)

r.plot_overall_performance(
    index="TC III",
    unit_change="亿",
    period="QTR",
)
r.plot_overall_performance(
    index="TC III",
    unit="PTD",
    unit_change="亿",
    period="QTR",
)


r.plot_overall_performance_dual(
    index="VBP",
    unit_change="亿",
    label_threshold=0.01,
    fontsize=11,
    width=15,
    height=6,
    sorter=["VBP品种", "非VBP品种"],
)

r.plot_size_diff(
    index="MOLECULE",
    unit="Value",
    unit_change="亿",
    label_limit=20,
    hue="VBP",
    focus=FOCUS_MOLECULES,
)

r.plot_size_diff(
    index="MOLECULE",
    unit="PTD",
    unit_change="亿",
    label_limit=20,
    hue="VBP",
    focus=FOCUS_MOLECULES,
)

r.plot_share_gr(
    index="MOLECULE",
    unit="Value",
    ylim=(-0.2, 0.4),
    hue="VBP",
    focus=FOCUS_MOLECULES,
)
r.plot_share_gr(
    index="MOLECULE",
    unit="PTD",
    ylim=(-0.2, 0.4),
    label_topy=2,
    hue="VBP",
    focus=FOCUS_MOLECULES,
)


r.plottable_latest(index="MOLECULE", unit="Value", focus=FOCUS_MOLECULES, hue="VBP")
r.plottable_latest(index="MOLECULE", unit="PTD", focus=FOCUS_MOLECULES, hue="VBP")

r.plot_share_trend(
    index="MOLECULE",
    focus=FOCUS_MOLECULES,
)
r.plot_share_trend(
    index="MOLECULE",
    focus=FOCUS_MOLECULES,
    unit="PTD",
)

r.plottable_annual(
    index="MOLECULE",
    unit="Value",
    focus=FOCUS_MOLECULES,
)
r.plottable_annual(
    index="MOLECULE",
    unit="PTD",
    focus=FOCUS_MOLECULES,
)


r.plot_size_diff(
    index="PRODUCT",
    unit="Value",
    unit_change="亿",
    hue="MOLECULE",
    focus=FOCUS_PRODUCTS,
)

r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="亿",
    hue="MOLECULE",
    focus=FOCUS_PRODUCTS,
)

r.plot_share_gr(
    index="PRODUCT",
    unit="Value",
    ylim=(-0.3, 0.6),
    label_topy=2,
    hue="MOLECULE",
    focus=FOCUS_PRODUCTS,
)
r.plot_share_gr(
    index="PRODUCT",
    unit="PTD",
    ylim=(-0.3, 1),
    label_topy=1,
    hue="MOLECULE",
    focus=FOCUS_PRODUCTS,
)

r.plottable_latest(
    index="PRODUCT",
    unit="Value",
    focus=FOCUS_PRODUCTS,
    hue=("MOLECULE", "CORPORATION", "VBP"),
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    focus=FOCUS_PRODUCTS,
    hue=("MOLECULE", "CORPORATION", "VBP"),
)

r.plot_share_trend(
    index="PRODUCT",
    focus=FOCUS_PRODUCTS,
)
r.plot_share_trend(
    index="PRODUCT",
    unit="PTD",
    focus=FOCUS_PRODUCTS,
)

r.plottable_annual(index="PRODUCT", unit="Value")
r.plottable_annual(index="PRODUCT", unit="PTD")
