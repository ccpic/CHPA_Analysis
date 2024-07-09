from CHPA2 import CHPA, convert_std_volume
from sqlalchemy import create_engine
import pandas as pd
from figure import GridFigure
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

# RAAS市场
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
mask = df["MOLECULE"] == "氯沙坦钾"
df.loc[mask, "MOLECULE"] = "氯沙坦"
mask = df["MOLECULE"] == "氯沙坦钾氢氯噻嗪"
df.loc[mask, "MOLECULE"] = "氯沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "奥美沙坦酯氢氯噻嗪"
df.loc[mask, "MOLECULE"] = "奥美沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "培哚普利叔丁胺"
df.loc[mask, "MOLECULE"] = "培哚普利"
mask = df["MOLECULE"] == "贝那普利,氨氯地平"
df.loc[mask, "MOLECULE"] = "贝那普利氨氯地平"
mask = df["MOLECULE"].isin(["氨氯地平贝那普利(II)", "氨氯地平贝那普利"])
df.loc[mask, "MOLECULE"] = "贝那普利氨氯地平"
mask = df["MOLECULE"] == "培哚普利氨氯地平片(III)"
df.loc[mask, "MOLECULE"] = "培哚普利氨氯地平"
mask = df["MOLECULE"] == "奥美沙坦酯氨氯地平片"
df.loc[mask, "MOLECULE"] = "奥美沙坦氨氯地平"
mask = df["MOLECULE"] == "美阿沙坦钾片"
df.loc[mask, "MOLECULE"] = "美阿沙坦"

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
]
mask = df["MOLECULE"].isin(vbp_molecules)
df.loc[mask, "VBP"] = "VBP品种"
mask = df["MOLECULE"].isin(vbp_molecules) == False
df.loc[mask, "VBP"] = "非VBP品种"

# df = df[df["VBP"] == "非VBP品种"]

# ARNI销量打55折
if condition == condition_raasi or condition_raasi_plain_arni:
    mask = df["MOLECULE"] == "沙库巴曲缬沙坦"
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] * 0.7


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])

convert_std_volume(df, "MOLECULE", "氯沙坦", "100MG", 2)
convert_std_volume(df, "MOLECULE", "厄贝沙坦", "75MG", 0.5)
convert_std_volume(df, "MOLECULE", "替米沙坦", "20MG", 0.25)
convert_std_volume(df, "MOLECULE", "替米沙坦", "40MG", 0.5)
convert_std_volume(df, "MOLECULE", "坎地沙坦", "4MG", 0.5)
convert_std_volume(df, "MOLECULE", "缬沙坦", "40MG", 0.5)
convert_std_volume(df, "MOLECULE", "缬沙坦", "160MG", 2)
convert_std_volume(df, "MOLECULE", "培哚普利", "8MG", 2)
convert_std_volume(df, "MOLECULE", "贝那普利", "5MG", 0.5)
convert_std_volume(df, "MOLECULE", "卡托普利", "12.5MG", 0.25)
convert_std_volume(df, "MOLECULE", "卡托普利", "25MG", 0.5)
convert_std_volume(df, "MOLECULE", "依那普利", "5MG", 0.5)
convert_std_volume(df, "MOLECULE", "雷米普利", "2.5MG", 0.5)
convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "100MG", 0.5)
convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "50MG", 0.25)
convert_std_volume(df, "MOLECULE", "阿齐沙坦", "20MG", 0.5)
convert_std_volume(df, "MOLECULE", "美阿沙坦钾", "80MG", 2)

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
mask = df["MOLECULE"].str.contains("沙库巴曲缬沙坦")
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


r = CHPA(df, name="RAAS+ARNI市场", date_column="DATE", period_interval=3)

df2 = df[df["TC III"].isin(["ARB", "ACEI", "A+C", "A+D"])]
r = CHPA(df2, name="RAAS市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(
#     index="TC III", sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"], unit_change="百万"
# )
# r.plot_overall_performance(
#     index="TC III",
#     unit="Volume (Std Counting Unit)",
#     sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"],
#     unit_change="百万",
# )

# r.plot_overall_performance(
#     index="TC III",
#     sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"],
#     unit_change="百万",
#     period="QTR",
# )
# r.plot_overall_performance(
#     index="TC III",
#     unit="Volume (Std Counting Unit)",
#     sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"],
#     unit_change="百万",
#     period="QTR",
# )

# r.plot_overall_performance(
#     index="VBP",
#     unit_change="百万",
# )
# r.plot_overall_performance(
#     index="VBP",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
# )

# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Value",
#     unit_change="百万",
#     label_limit=20,
#     label_topy=6,
#     hue="VBP",
# )

# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_limit=20,
#     label_topy=9,
#     hue="VBP",
# )

# r.plot_share_gr(index="MOLECULE", unit="Value", ylim=(-0.5, 1), label_topy=6, hue="VBP")
# r.plot_share_gr(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     ylim=(-0.5, 1),
#     label_topy=6,
#     hue="VBP",
# )


# r.plottable_latest(
#     index="MOLECULE", unit="Value", focus="阿利沙坦", hue=("TC III", "VBP")
# )
# r.plottable_latest(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     focus="阿利沙坦",
#     hue=("TC III", "VBP"),
# )

# r.plot_share_trend(index="MOLECULE", focus="阿利沙坦")
# r.plot_share_trend(
#     index="MOLECULE", focus="阿利沙坦", unit="Volume (Std Counting Unit)"
# )

# r.plottable_annual(index="MOLECULE", unit="Value", focus="阿利沙坦")
# r.plottable_annual(index="MOLECULE", unit="Volume (Std Counting Unit)", focus="阿利沙坦")


# r.plot_size_diff(index="PRODUCT", unit="Value", unit_change="百万", hue="CLASS")

# r.plot_size_diff(
#     index="PRODUCT", unit="Volume (Std Counting Unit)", unit_change="百万", hue="CLASS"
# )

# r.plot_share_gr(
#     index="PRODUCT", unit="Value", ylim=(-1, 1), label_topy=4, hue="CLASS"
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     ylim=(-1, 1),
#     label_topy=0,
#     hue="CLASS",
# )

D_MAP_PRODUCT = {
    "XIN LI TAN (SI6)": "信立坦",
    "AMLODIPINE&BENAZEP (S5O)": "贝那普利氨氯地平（地奥）",
    "BAI AN XIN (GRU)": "百安新",
    "COVERAM (SVR)": "开素达",
    "EXFORGE (NVR)": "倍博特",
    "OLMETEC PLUS (DSC)": "复傲坦",
    "BEI YI (ZJ5)": "倍怡",
    "LAN SHA (BW.)": "兰沙",
    "DIOVAN (NVR)": "代文",
    "XIE AN ZHI (ZHU)": "协安之",
    "APROVEL (SG9)": "安博维",
    "COAPROVEL (SG9)": "安博诺",
    "HYZAAR (ORG)": "海捷亚",
    "VALSARTAN AND HYDR (B7J)": "缬沙坦氢氯噻嗪片",
    "TIAN SHU PING (NJ2)": "天舒平",
    "AN LAI (ZJ5)": "安来",
    "YI DA LI (ZUP)": "伊达力",
    "JI JIA (JSH)": "吉加",
    "TUO PING (ZHT)": "托平",
    "BEI YUE (ZJ5)": "倍悦",
    "HENG LUO KAI (HCY)": "恒洛凯",
    "YI SU (JJJ)": "依苏",
    "XIE KE (JC4)": "缬克",
    "VALSARTAN (QJX)": "缬沙坦片",
    "RUI XIN AN (JSH)": "瑞心安",
    "OU MEI NING (HCN)": "欧美宁",
}
D_MAP_CORPORATION = {
    "SHENZHEN XINLITAI": "信立泰",
    "SC.CD DIAO GROUP": "成都地奥",
    "YANGTZERIVER GROUP": "扬子江",
    "SERVIER GROUP": "施维雅",
    "NOVARTIS GROUP": "诺华",
    "DAIICHI SANKYO GRO": "第一三共",
    "ZJ.HUAHAI PHARM": "华海药业",
    "BJ.FUYUAN PHARMACE": "北京福元",
    "ZJ.HUAYUAN PHARM": "花园药业",
    "SANOFI GROUP": "赛诺菲",
    "ORGANON": "欧加隆",
    "SHUANGHE GROUP": "北京双鹤",
    "C.T-TIANQING GP.": "正大天晴",
    "ZHEJIANG HISUN PHA": "瀚晖",
    "HENGRUI GROUP": "恒瑞",
    "ZHUHAI TIANDA PHAR": "珠海天大",
    "HN.CHINA YINYE PHA": "天地恒一",
    "JS.CHANGZHOU NO.4": "常州四药",
    "QIANJINXIANGJIANG": "千金湘江",
    "HB.YC.CHANGJIANG": "东阳光",
}


r.data["PRODUCT"] = r.data["PRODUCT"].map(D_MAP_PRODUCT).fillna(r.data["PRODUCT"])
r.data["CORPORATION"] = (
    r.data["CORPORATION"].map(D_MAP_CORPORATION).fillna(r.data["CORPORATION"])
)
r.data["PRODUCT_MOLECULE"] = r.data.apply(
    lambda x: (
        f"{x['PRODUCT']}\n{x['MOLECULE']}"
        if x["PRODUCT"] not in ["贝那普利氨氯地平（地奥）"]
        else x["PRODUCT"]
    ),
    axis=1,
)
# r.plottable_latest(
#     index="PRODUCT",
#     unit="Value",
#     # focus="XIN LI TAN (SI6)",
#     focus = "信立坦",
#     hue=("MOLECULE", "CORPORATION", "VBP"),
#     period="MAT",
#     topn=15,
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     # focus="XIN LI TAN (SI6)",
#     focus = "信立坦",
#     hue=("MOLECULE", "CORPORATION", "VBP"),
#     period="MAT",
#     topn=15
# )


f = plt.figure(
    FigureClass=GridFigure,
    ncols=2,
    width=15,
    height=6,
    style={
        "title": "RAAS市场Top产品滚动年表现趋势",
    },
    fontsize=11,
    color_dict={
        "信立坦\n阿利沙坦": "purple",
        "贝那普利氨氯地平（地奥）": "navy",
        "百安新\n贝那普利氨氯地平": "crimson",
        "开素达\n培哚普利氨氯地平": "darkgreen",
        "倍博特\n缬沙坦氨氯地平": "saddlebrown",
        "复傲坦\n奥美沙坦氢氯噻嗪": "olivedrab",
        "倍怡\n氯沙坦": "violet",
        "兰沙\n奥美沙坦": "gold",
        "代文\n缬沙坦": "deepskyblue",
        "安博诺\n厄贝沙坦氢氯噻嗪": "coral",
        "安来\n厄贝沙坦": "gold",
        "伊达力\n厄贝沙坦": "olivedrab",
        "吉加\n厄贝沙坦": "navy",
        "托平\n缬沙坦": "darkgreen",
        "倍悦\n厄贝沙坦氢氯噻嗪": "crimson",
        "缬克\n缬沙坦": "deepskyblue",
        "瑞心安\n缬沙坦氨氯地平": "teal",
    },
)

for i, unit in enumerate(["Value", "Volume (Std Counting Unit)"]):
    plot_data = (
        r.get_pivot(
            index="PRODUCT_MOLECULE",
            columns=r.date_column,
            values="AMOUNT",
            query_str=f"UNIT=='{unit}' and PERIOD=='MAT'",
        )
        .sort_values("2024-03", ascending=False)
        .head(10)
        .loc[:, ["2021-03", "2022-03", "2023-03", "2024-03"]]
        .div(r.unit_change("亿"))
    )
    print(plot_data)

    f.plot(
        data=plot_data.transpose(),
        kind="line",
        ax_index=i,
        fmt="{:.1f}",
        style={
            "title": "滚动年金额" if unit == "Value" else "滚动年PTD",
            "ylabel": "金额（亿元）" if unit == "Value" else "PTD（亿）",
            "remove_yticks": True,
        },
        show_label=plot_data.index,
        focus=["信立坦\n阿利沙坦"],
        linewidth=1,
    )

f.save()


# f = plt.figure(
#     FigureClass=GridFigure,
#     ncols=2,
#     width=15,
#     height=6,
#     style={
#         "title": "RAAS市场Top产品滚动年份额趋势",
#     },
# )

# for i, unit in enumerate(["Value", "Volume (Std Counting Unit)"]):
#     plot_data = r.get_pivot(
#         index="PRODUCT",
#         columns=r.date_column,
#         values="AMOUNT",
#         query_str=f"UNIT=='{unit}' and PERIOD=='MAT'",
#     ).sort_values("2024-03", ascending=False)
#     plot_data = (
#         plot_data.div(plot_data.sum(axis=0), axis=1)
#         .head(10)
#         .loc[:, ["2021-03", "2022-03", "2023-03", "2024-03"]]
#     )

#     f.plot(
#         data=plot_data.transpose(),
#         kind="line",
#         ax_index=i,
#         fmt="{:.1%}",
#         style={
#             "title": "滚动年金额" if unit == "Value" else "滚动年PTD",
#             "ylabel": "金额份额（%）" if unit == "Value" else "PTD份额（%）",
#             "remove_yticks": True,
#         },
#         show_label=plot_data.index,
#         focus=["信立坦"],
#     )

# f.save()

# r.plot_share_trend(
#     index="PRODUCT",
#     focus="XIN LI TAN (SI6)",
#     period="MAT",
# )
# r.plot_share_trend(
#     index="PRODUCT",
#     focus="XIN LI TAN (SI6)",
#     unit="Volume (Std Counting Unit)",
#     period="MAT",
# )

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")


# df2 = df[df["TC III"].isin(["ARB", "ACEI", "ARNI"])]
# r = CHPA(df2, name="RAAS单方+ARNI", date_column="DATE", period_interval=3)

df2 = df[df["TC III"].isin(["ARB", "ACEI"])]
r = CHPA(df2, name="RAAS单方", date_column="DATE", period_interval=3)

# r.plot_overall_performance(
#     index="TC III", sorter=["ARB", "ACEI", "ARNI"], unit_change="百万"
# )
# r.plot_overall_performance(
#     index="TC III",
#     unit="Volume (Std Counting Unit)",
#     sorter=["ARB", "ACEI", "ARNI"],
#     unit_change="百万",
# )

# r.plot_overall_performance(
#     index="TC III",
#     sorter=["ARB", "ACEI", "ARNI"],
#     unit_change="百万",
#     period="QTR",
# )
# r.plot_overall_performance(
#     index="TC III",
#     unit="Volume (Std Counting Unit)",
#     sorter=["ARB", "ACEI", "ARNI"],
#     unit_change="百万",
#     period="QTR",
# )

# r.plot_overall_performance(
#     index="VBP", unit_change="百万"
# )
# r.plot_overall_performance(
#     index="VBP",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
# )


# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Value",
#     unit_change="百万",
#     label_limit=20,
#     hue="VBP",
# )

# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_limit=20,
#     hue="VBP",
# )

# r.plot_share_gr(
#     index="MOLECULE",
#     unit="Value",
#     ylim=(-0.5, 1),
#     hue="VBP",
# )
# r.plot_share_gr(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     ylim=(-0.5, 1),
#     label_topy=2,
#     hue="VBP",
# )


# r.plottable_latest(index="MOLECULE", unit="Value", focus="阿利沙坦", hue=("TC III", "VBP"))
# r.plottable_latest(index="MOLECULE", unit="Volume (Std Counting Unit)", focus="阿利沙坦", hue=("TC III", "VBP"))

# r.plot_share_trend(index="MOLECULE", focus="阿利沙坦")
# r.plot_share_trend(
#     index="MOLECULE",
#     focus="阿利沙坦",
#     unit="Volume (Std Counting Unit)",
# )

# r.plottable_annual(index="MOLECULE", unit="Value", focus="阿利沙坦")
# r.plottable_annual(index="MOLECULE", unit="Volume (Std Counting Unit)", focus="阿利沙坦")


# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Value",
#     unit_change="百万",
#     hue="CLASS",
# )

# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     hue="CLASS",
# )

# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Value",
#     ylim=(-1, 1),
#     hue="CLASS",
# )

# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     ylim=(-1, 1),
#     label_topy=4,
#     hue="CLASS",
# )


# r.plottable_latest(
#     index="PRODUCT",
#     unit="Value",
#     focus="XIN LI TAN (SI6)",
#     hue=("MOLECULE", "CORPORATION", "VBP"),
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     focus="XIN LI TAN (SI6)",
#     hue=("MOLECULE", "CORPORATION", "VBP"),
# )

# r.plot_share_trend(index="PRODUCT", focus="XIN LI TAN (SI6)")
# r.plot_share_trend(
#     index="PRODUCT",
#     focus="XIN LI TAN (SI6)",
#     unit="Volume (Std Counting Unit)",
# )

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")

df2 = df[df["TC III"].isin(["ARB"])]
r = CHPA(df2, name="ARB市场", date_column="DATE", period_interval=3)


# r.plot_overall_performance(
#     index="TC III",  unit_change="百万"
# )
# r.plot_overall_performance(
#     index="TC III",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
# )

# r.plot_overall_performance(
#     index="TC III",
#     unit_change="百万",
#     period="QTR",
# )
# r.plot_overall_performance(
#     index="TC III",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     period="QTR",
# )

# r.plot_overall_performance(
#     index="VBP", unit_change="百万"
# )
# r.plot_overall_performance(
#     index="VBP",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
# )

# r.plot_size_diff(
#     index="MOLECULE", unit="Value", unit_change="百万", label_limit=20, hue="VBP"
# )

# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_limit=20,
#     hue="VBP",
# )

# r.plot_share_gr(index="MOLECULE", unit="Value", ylim=(-0.2, 1), hue="VBP")
# r.plot_share_gr(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     ylim=(-0.2, 1),
#     label_topy=2,
#     hue="VBP",
# )


# r.plottable_latest(index="MOLECULE", unit="Value", focus="阿利沙坦", hue="VBP")
# r.plottable_latest(
#     index="MOLECULE", unit="Volume (Std Counting Unit)", focus="阿利沙坦", hue="VBP"
# )

# r.plot_share_trend(index="MOLECULE", focus="阿利沙坦")
# r.plot_share_trend(
#     index="MOLECULE",
#     focus="阿利沙坦",
#     unit="Volume (Std Counting Unit)",
# )

# r.plottable_annual(index="MOLECULE", unit="Value", focus="阿利沙坦")
# r.plottable_annual(index="MOLECULE", unit="Volume (Std Counting Unit)", focus="阿利沙坦")


# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Value",
#     unit_change="百万",
#     hue="MOLECULE",
# )

# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     hue="MOLECULE",
# )

# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Value",
#     ylim=(-1, 1),
#     label_topy=2,
#     hue="MOLECULE",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     ylim=(-1, 1),
#     label_topy=1,
#     hue="MOLECULE",
# )

# r.plottable_latest(
#     index="PRODUCT",
#     unit="Value",
#     focus="XIN LI TAN (SI6)",
#     hue=("MOLECULE", "CORPORATION", "VBP"),
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     focus="XIN LI TAN (SI6)",
#     hue=("MOLECULE", "CORPORATION", "VBP"),
# )

# r.plot_share_trend(index="PRODUCT", focus="XIN LI TAN (SI6)")
# r.plot_share_trend(
#     index="PRODUCT",
#     focus="XIN LI TAN (SI6)",
#     unit="Volume (Std Counting Unit)",
# )

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")
