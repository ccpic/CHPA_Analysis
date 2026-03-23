from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
# engine = create_engine(
#     "mssql+pymssql://sa:Luna1117@49.232.203.83/CHPA_1806"
# )  # 远程数据库

table_name = "data"

condition_htn = "[TC II] in ('C03 DIURETICS|利尿剂', \
'C07 BETA BLOCKING AGENTS|β受体阻断剂',\
'C09 RENIN-ANGIOTEN SYST AGENT|作用于肾素-血管紧张素系统的药物',\
'C08 CALCIUM ANTAGONISTS|钙离子拮抗剂',\
'C02 ANTIHYPERTENSIVES|抗高血压药')"

print("Start importing...")
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
    "多沙唑嗪": "*",
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
    "奥美沙坦酯氨氯地平": "奥美沙坦氨氯地平",
    "氨氯地平叶酸片(Ⅱ)": "氨氯地平叶酸",
    "比索洛尔氨氯地平片": "比索洛尔氨氯地平",
    "美阿沙坦钾片": "美阿沙坦",
    "尼群洛尔": "尼群地平阿替洛尔",
    "奥美沙坦酯氢氯噻嗪": "奥美沙坦氢氯噻嗪",
    "氯沙坦钾": "氯沙坦",
    "阿利沙坦酯氨氯地平": "阿利沙坦氨氯地平",
    "左氨氯地平": "左旋氨氯地平",
}
df["MOLECULE"] = df["MOLECULE"].map(D_RENAME).fillna(df["MOLECULE"])
# df.to_excel("口服降压药市场_test.xlsx", index=False)

print("Finished renaming...")

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

df_ptd = pd.read_excel("高血压PTD系数_0821.xlsx")
for row in df_ptd.iterrows():
    mask = (
        (df["MOLECULE"] == row[1]["MOLECULE"])
        & (df["STRENGTH"] == row[1]["STRENGTH"])
        & (df["UNIT"] == "PTD")
    )
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / row[1]["INDEX"]
    mask = df["MOLECULE"] == row[1]["MOLECULE"]
    df.loc[mask, "VBP"] = row[1]["VBP"]

print("Finished converting PTD...")


df.loc[df["CLASS"] == "BB", "AMOUNT"] = df.loc[df["CLASS"] == "BB", "AMOUNT"] * 0.55
df.loc[df["CLASS"] == "ARNI", "AMOUNT"] = df.loc[df["CLASS"] == "ARNI", "AMOUNT"] * 0.8
df.loc[df["CLASS"] == "DU", "AMOUNT"] = df.loc[df["CLASS"] == "DU", "AMOUNT"] * 0.8

# df.loc[~df["CLASS"].isin(["A+C FDC", 'ARB','ACEI','ARNI','A+D FDC']), "CLASS"] = "Others"

print("Finished adding weights...")

FOCUS_CLASS=["ARNI","ARB","A+C FDC"]
FOCUS_MOLECULES = ["阿利沙坦", "阿利沙坦氨氯地平", "沙库巴曲缬沙坦"]
FOCUS_PRODUCTS = [
    "XIN LI TAN (SI6)",
    "ENTRESTO (NVR)",
    "FU LI TAN (SI6)",
]

r = CHPA(df, name="口服降压药市场", date_column="DATE", period_interval=3)
# r.data.to_excel("口服降压药市场.xlsx")

r.plot_overall_performance_dual(
    index="CLASS",
    unit_change="亿",
    label_threshold=0.01,
    color_dict=D_COLOR,
    fontsize=11,
    width=15,
    height=6,
    # sorter=["ARB", "ACEI", "A+C FDC", "A+D FDC", "ARNI", "Others"],
)

r.plot_overall_performance(
    index="CLASS", unit_change="亿", label_threshold=0.01, color_dict=D_COLOR, width=12, height=7.2
)
r.plot_overall_performance(
    index="CLASS",
    unit_change="亿",
    label_threshold=0.01,
    color_dict=D_COLOR,
    unit="PTD",
    width=12, height=7.2
)

r.plot_overall_performance(
    index="CLASS",
    unit_change="亿",
    label_threshold=0.01,
    color_dict=D_COLOR,
    period="QTR",
)
r.plot_overall_performance(
    index="CLASS",
    unit_change="亿",
    label_threshold=0.01,
    color_dict=D_COLOR,
    unit="PTD",
    period="QTR",
)

r.plottable_latest(index="CLASS", unit="Value", show_total=False, focus=FOCUS_CLASS)
r.plottable_latest(index="CLASS", unit="PTD", show_total=False, focus=FOCUS_CLASS)

r.plottable_annual(index="CLASS", unit="Value")
r.plottable_annual(index="CLASS", unit="PTD")


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
    hue="VBP",
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
    label_topy=5,
    label_limit=20,
    hue="VBP",
    focus=FOCUS_MOLECULES,
)
r.plot_share_gr(
    index="MOLECULE",
    unit="Value",
    ylim=(-0.4, 0.6),
    label_limit=20,
    hue="VBP",
    focus=FOCUS_MOLECULES,
)
r.plot_share_gr(
    index="MOLECULE",
    unit="PTD",
    label_topy=5,
    label_limit=20,
    ylim=(-0.2, 0.6),
    hue="VBP",
    focus=FOCUS_MOLECULES,
)

r.plottable_latest(index="MOLECULE", unit="Value", hue="CLASS", focus=FOCUS_MOLECULES)
r.plottable_latest(index="MOLECULE", unit="PTD", hue="CLASS", focus=FOCUS_MOLECULES)

r.plot_share_trend(index="MOLECULE", unit="Value", focus=FOCUS_MOLECULES)
r.plot_share_trend(index="MOLECULE", unit="PTD", focus=FOCUS_MOLECULES)

r.plottable_annual(index="MOLECULE", unit="Value")
r.plottable_annual(index="MOLECULE", unit="PTD")

r.plot_size_diff(
    index="PRODUCT",
    unit="Value",
    unit_change="亿",
    label_limit=20,
    hue="CLASS",
    focus=FOCUS_PRODUCTS,
)
r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="亿",
    label_topy=7,
    label_limit=20,
    hue="CLASS",
    focus=FOCUS_PRODUCTS,
)

r.plot_share_gr(
    index="PRODUCT",
    unit="Value",
    label_topy=5,
    ylim=(-0.5, 1),
    label_limit=20,
    hue="CLASS",
    focus=FOCUS_PRODUCTS,
)
r.plot_share_gr(
    index="PRODUCT",
    unit="PTD",
    label_topy=5,
    label_limit=20,
    ylim=(-0.5, 1),
    hue="CLASS",
    focus=FOCUS_PRODUCTS,
)


# D_MAP_PRODUCT = {
#     "ENTRESTO (NVR)": "诺欣妥",
#     "NORVASC (VI/)": "络活喜",
#     "ADALAT (BY6)": "拜新同",
#     "XIN LI TAN (SI6)": "信立坦",
#     "BETALOC ZOK (AZN)": "倍他乐克",
#     "CARDURA XL (VI/)": "可多华",
#     "CONIEL (KKN)": "可力洛",
#     "YUAN ZHI (DWM)": "元治",
#     "AMLODIPINE&BENAZEP (S5O)": "贝那普利氨氯地平（地奥）",
#     "BAI AN XIN (GRU)": "百安新",
#     "COVERAM (SVR)": "开素达",
#     "EXFORGE (NVR)": "倍博特",
#     "OLMETEC PLUS (DSC)": "复傲坦",
#     "BEI YI (ZJ5)": "倍怡",
#     "LAN SHA (BW.)": "兰沙",
#     "DIOVAN (NVR)": "代文",
#     "XIE AN ZHI (ZHU)": "协安之",
#     "APROVEL (SG9)": "安博维",
#     "COAPROVEL (SG9)": "安博诺",
#     "HYZAAR (ORG)": "海捷亚",
#     "VALSARTAN AND HYDR (B7J)": "缬沙坦氢氯噻嗪片",
#     "TIAN SHU PING (NJ2)": "天舒平",
#     "AN LAI (ZJ5)": "安来",
#     "YI DA LI (ZUP)": "伊达力",
#     "JI JIA (JSH)": "吉加",
#     "TUO PING (ZHT)": "托平",
#     "BEI YUE (ZJ5)": "倍悦",
#     "HENG LUO KAI (HCY)": "恒洛凯",
#     "YI SU (JJJ)": "依苏",
#     "XIE KE (JC4)": "缬克",
#     "VALSARTAN (QJX)": "缬沙坦片",
#     "RUI XIN AN (JSH)": "瑞心安",
#     "OU MEI NING (HCN)": "欧美宁",
#     "SHI HUI DA (JTF)": "施慧达",
#     "PLENDIL (AZM)": "波依定",
# }
# D_MAP_CORPORATION = {
#     "SHENZHEN XINLITAI": "信立泰",
#     "VIATRIS INC": "晖致",
#     "BHC GROUP": "拜耳",
#     "SD.HWELLSO PHARMAC": "山东华素",
#     "ASTRAZENECA GROUP": "阿斯利康",
#     "SC.CD DIAO GROUP": "成都地奥",
#     "JL.SHIHUIDA PHARM": "吉林施慧达",
#     "YANGTZERIVER GROUP": "扬子江",
#     "SERVIER GROUP": "施维雅",
#     "NOVARTIS GROUP": "诺华",
#     "DAIICHI SANKYO GRO": "第一三共",
#     "ZJ.HUAHAI PHARM": "华海药业",
#     "BJ.FUYUAN PHARMACE": "北京福元",
#     "ZJ.HUAYUAN PHARM": "花园药业",
#     "SANOFI GROUP": "赛诺菲",
#     "ORGANON": "欧加隆",
#     "SHUANGHE GROUP": "北京双鹤",
#     "C.T-TIANQING GP.": "正大天晴",
#     "ZHEJIANG HISUN PHA": "瀚晖",
#     "HENGRUI GROUP": "恒瑞",
#     "ZHUHAI TIANDA PHAR": "珠海天大",
#     "HN.CHINA YINYE PHA": "天地恒一",
#     "JS.CHANGZHOU NO.4": "常州四药",
#     "QIANJINXIANGJIANG": "千金湘江",
#     "HB.YC.CHANGJIANG": "东阳光",
#     "KIRIN GROUP": "协和麒麟",
# }


# r.data["PRODUCT"] = r.data["PRODUCT"].map(D_MAP_PRODUCT).fillna(r.data["PRODUCT"])
# r.data["CORPORATION"] = (
#     r.data["CORPORATION"].map(D_MAP_CORPORATION).fillna(r.data["CORPORATION"])
# )


r.plottable_latest(
    index="PRODUCT",
    unit="Value",
    hue=("MOLECULE", "CORPORATION"),
    focus=FOCUS_PRODUCTS,
    # focus="XIN LI TAN (SI6)",
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    hue=("MOLECULE", "CORPORATION"),
    focus=FOCUS_PRODUCTS,
)

r.plot_share_trend(index="PRODUCT", unit="Value")
r.plot_share_trend(index="PRODUCT", unit="PTD")

r.plottable_annual(index="PRODUCT", unit="Value")
r.plottable_annual(index="PRODUCT", unit="PTD")


df = df[df["CLASS"] == "ARNI"]
r = CHPA(df, name="ARNI市场", date_column="DATE", period_interval=3)

r.plot_trend_with_gr(
    index=None, unit_change="亿", color_dict={"AMOUNT": "Navy"}, width=6, height=5
)
r.plot_trend_with_gr(
    index=None,
    unit_change="亿",
    unit="PTD",
    color_dict={"AMOUNT": "Crimson"},
    width=6,
    height=5,
)

r.plot_trend_with_gr(
    index=None,
    unit_change="亿",
    color_dict={"AMOUNT": "Navy"},
    period="QTR",
    width=15,
    height=6,
)
r.plot_trend_with_gr(
    index=None,
    unit_change="亿",
    unit="PTD",
    color_dict={"AMOUNT": "Crimson"},
    period="QTR",
    width=15,
    height=6,
)

r.plottable_latest(
    index="PRODUCT",
    unit="Value",
    hue="CORPORATION",
    fontsize=16,
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    hue="CORPORATION",
    fontsize=16,
)


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
