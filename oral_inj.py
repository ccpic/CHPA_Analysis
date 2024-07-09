from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition_pali = (
    "[MOLECULE] in ('PALIPERIDONE|帕利哌酮', 'PALIPERIDONE PALMITATE|帕利哌酮')"
)

sql = "SELECT * FROM " + table_name + " WHERE " + condition_pali
df = pd.read_sql(sql=sql, con=engine)

D_FORM = {
    "INVEGA TAB RTD FC 6MG 7": "口服",
    "INVEGA TAB RTD FC 3MG 7": "口服",
    "INVEGA SUSTENNA SYRINGE 75MG 0.75ML 1": "注射（月制剂）",
    "INVEGA SUSTENNA SYRINGE 100MG 1ML 1": "注射（月制剂）",
    "INVEGA SUSTENNA SYRINGE 150MG 1.5ML 1": "注射（月制剂）",
    "INVEGA TRINZA SYRINGE 525MG 2.62ML 1": "注射（3月制剂）",
    "INVEGA TRINZA SYRINGE 350MG 1.75ML 1": "注射（3月制剂）",
    "INVEGA TRINZA SYRINGE 263MG 1.31ML 1": "注射（3月制剂）",
    "AI LAN NING TAB RTD MC 6MG 7": "口服",
    "AI LAN NING TAB RTD MC 3MG 7": "口服",
    "AI LAN NING TAB RTD MC 3MG 14": "口服",
    "PALIPERIDONE TAB RTD MC 3MG 14": "口服",
    "PALIPERIDONE TAB RTD MC 6MG 30": "口服",
    "XING BI DA SYRINGE 100MG 1ML 1": "注射（月制剂）",
    "XING BI DA SYRINGE 150MG 1.5ML 1": "注射（月制剂）",
}

D_INDEX = {
    "INVEGA TAB RTD FC 6MG 7": 1,
    "INVEGA TAB RTD FC 3MG 7": 2,
    "INVEGA SUSTENNA SYRINGE 75MG 0.75ML 1": 1 / (30 * 0.75),
    "INVEGA SUSTENNA SYRINGE 100MG 1ML 1": 1 / 30,
    "INVEGA SUSTENNA SYRINGE 150MG 1.5ML 1": 1 / (30 * 1.5),
    "INVEGA TRINZA SYRINGE 525MG 2.62ML 1": 1 / (90 * 525 / 350),
    "INVEGA TRINZA SYRINGE 350MG 1.75ML 1": 1 / 90,
    "INVEGA TRINZA SYRINGE 263MG 1.31ML 1": 1 / (90 * 263 / 350),
    "AI LAN NING TAB RTD MC 6MG 7": 1,
    "AI LAN NING TAB RTD MC 3MG 7": 2,
    "AI LAN NING TAB RTD MC 3MG 14": 2,
    "PALIPERIDONE TAB RTD MC 3MG 14": 2,
    "PALIPERIDONE TAB RTD MC 6MG 30": 1,
    "XING BI DA SYRINGE 100MG 1ML 1": 1 / 30,
    "XING BI DA SYRINGE 150MG 1.5ML 1": 1 / (30 * 1.5),
}

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["FORM"] = df["PACKAGE"].map(D_FORM)
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

for index, value in D_INDEX.items():
    mask = (df["PACKAGE"] == index) & (df["UNIT"] == "PTD")
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / value

r = CHPA(df, name="帕利哌酮", date_column="DATE", period_interval=3)
r.plot_overall_performance_dual(index="FORM", unit_change="百万", width=15, height=6)

condition_zipra = "[MOLECULE] in ('ZIPRASIDONE|齐拉西酮')"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_zipra
df = pd.read_sql(sql=sql, con=engine)
print(df["PACKAGE"].unique())


D_FORM = {
    "SI BEI GE VIAL DRY IM 20MG 1": "注射（日制剂）",
    "SI BEI GE CAP 20MG 20": "口服",
    "LI FU JUN AN TAB FLM CTD 20MG 30": "口服",
    "LI FU JUN AN AMP IM 10MG 1ML 1": "注射（日制剂）",
    "LI FU JUN AN TAB FLM CTD 20MG 20": "口服",
    "ZELDOX CAP 40MG 10": "口服",
    "ZELDOX CAP 20MG 10": "口服",
    "ZELDOX VIAL DRY IM 30MG 1": "注射（日制剂）",
}

D_INDEX = {
    "SI BEI GE VIAL DRY IM 20MG 1": 1,
    "SI BEI GE CAP 20MG 20": 2,
    "LI FU JUN AN TAB FLM CTD 20MG 30": 2,
    "LI FU JUN AN AMP IM 10MG 1ML 1": 2,
    "LI FU JUN AN TAB FLM CTD 20MG 20": 2,
    "ZELDOX CAP 40MG 10": 1,
    "ZELDOX CAP 20MG 10": 2,
    "ZELDOX VIAL DRY IM 30MG 1": 1,
}


df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["FORM"] = df["PACKAGE"].map(D_FORM)
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

for index, value in D_INDEX.items():
    mask = (df["PACKAGE"] == index) & (df["UNIT"] == "PTD")
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / value

r = CHPA(df, name="齐拉西酮", date_column="DATE", period_interval=3)
r.plot_overall_performance_dual(index="FORM", unit_change="百万", width=15, height=6)

condition_risper = "[MOLECULE] in ('RISPERIDONE|利培酮')"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_risper
df = pd.read_sql(sql=sql, con=engine)
print(df["PACKAGE"].unique())

D_FORM = {
    "ZHUO FU TAB FLM CTD 3MG 10": "口服",
    "ZHUO FU TAB FLM CTD 1MG 20": "口服",
    "RISPERDAL ORAL SOL 30MG 30ML 1": "口服",
    "RISPERDAL TAB FLM CTD 1MG 20": "口服",
    "RISPERDAL TAB FLM CTD 2MG 20": "口服",
    "ZHUO FU TAB FLM CTD 1MG 30": "口服",
    "ZHUO FU TAB FLM CTD 1MG 60": "口服",
    "XING ZHI TAB O.D 1MG 30": "口服",
    "XING ZHI TAB O.D 1MG 20": "口服",
    "XING ZHI TAB O.D 2MG 20": "口服",
    "RISPERIDONE CAP 1MG 20": "口服",
    "KE TONG TAB O.D 1MG 20": "口服",
    "KE TONG TAB O.D 1MG 30": "口服",
    "SI LI SHU TAB FLM CTD 1MG 40": "口服",
    "RISPERIDAL CONSTA VIAL DRY IM 25MG 1": "注射(2周制剂)",
    "DAN KE TAB FLM CTD 1MG 30": "口服",
    "RISPERIDAL CONSTA VIAL DRY IM 37.5MG 1": "注射(2周制剂)",
    "ZHUO FEI TAB FLM CTD 1MG 20": "口服",
    "SI LI SHU TAB FLM CTD 1MG 20": "口服",
    "DAN KE TAB FLM CTD 2MG 20": "口服",
    "DAN KE TAB O.D 1MG 20": "口服",
    "DAN KE TAB FLM CTD 1MG 20": "口服",
    "DAN KE ORAL SOL 30MG 30ML 1": "口服",
    "KE LI TONG ORAL SOL 30MG 30ML 1": "口服",
    "JING DE XIN ORAL SOL 30MG 30ML 1": "口服",
    "SUO LE TAB FLM CTD 1MG 20": "口服",
    "SUO LE TAB FLM CTD 1MG 30": "口服",
    "SUO LE TAB DISP 1MG 60": "口服",
    "SUO LE TAB DISP 2MG 30": "口服",
    "SUO LE TAB DISP 1MG 30": "口服",
    "SUO LE TAB FLM CTD 1MG 60": "口服",
    "RISPERIDONE CAP 1MG 30": "口服",
    "JING PING TAB 1MG 20": "口服",
    "JING PING TAB 1MG 30": "口服",
    "SHAN SI MING TAB FLM CTD 1MG 20": "口服",
    "TAI WEI SI TAB DISP 1MG 20": "口服",
    "TAI WEI SI TAB DISP 1MG 40": "口服",
    "XI EN LI ORAL SOL 0.1% 60ML 1": "口服",
    "RYKINDO VIAL DRY IM 25MG 1": "注射(2周制剂)",
    "RYKINDO VIAL DRY IM 37.5MG 1": "注射(2周制剂)",
    "RYKINDO VIAL DRY IM 50MG 1": "注射(2周制剂)",
    "RISPERIDONE ORAL SOL 30MG 30ML 1": "口服",
}


D_INDEX = {
    "ZHUO FU TAB FLM CTD 3MG 10": 1,
    "ZHUO FU TAB FLM CTD 1MG 20": 4,
    "RISPERDAL ORAL SOL 30MG 30ML 1": 4 / 30,
    "RISPERDAL TAB FLM CTD 1MG 20": 4,
    "RISPERDAL TAB FLM CTD 2MG 20": 2,
    "ZHUO FU TAB FLM CTD 1MG 30": 4,
    "ZHUO FU TAB FLM CTD 1MG 60": 4,
    "XING ZHI TAB O.D 1MG 30": 4,
    "XING ZHI TAB O.D 1MG 20": 4,
    "XING ZHI TAB O.D 2MG 20": 2,
    "RISPERIDONE CAP 1MG 20": 4,
    "KE TONG TAB O.D 1MG 20": 4,
    "KE TONG TAB O.D 1MG 30": 4,
    "SI LI SHU TAB FLM CTD 1MG 40": 4,
    "RISPERIDAL CONSTA VIAL DRY IM 25MG 1": 1 / 14,
    "DAN KE TAB FLM CTD 1MG 30": 4,
    "RISPERIDAL CONSTA VIAL DRY IM 37.5MG 1": 1 / (14 * 1.5),
    "ZHUO FEI TAB FLM CTD 1MG 20": 4,
    "SI LI SHU TAB FLM CTD 1MG 20": 4,
    "DAN KE TAB FLM CTD 2MG 20": 2,
    "DAN KE TAB O.D 1MG 20": 4,
    "DAN KE TAB FLM CTD 1MG 20": 4,
    "DAN KE ORAL SOL 30MG 30ML 1": 4 / 30,
    "KE LI TONG ORAL SOL 30MG 30ML 1": 4 / 30,
    "JING DE XIN ORAL SOL 30MG 30ML 1": 4 / 30,
    "SUO LE TAB FLM CTD 1MG 20": 4,
    "SUO LE TAB FLM CTD 1MG 30": 4,
    "SUO LE TAB DISP 1MG 60": 4,
    "SUO LE TAB DISP 2MG 30": 2,
    "SUO LE TAB DISP 1MG 30": 4,
    "SUO LE TAB FLM CTD 1MG 60": 4,
    "RISPERIDONE CAP 1MG 30": 4,
    "JING PING TAB 1MG 20": 4,
    "JING PING TAB 1MG 30": 4,
    "SHAN SI MING TAB FLM CTD 1MG 20": 4,
    "TAI WEI SI TAB DISP 1MG 20": 4,
    "TAI WEI SI TAB DISP 1MG 40": 4,
    "XI EN LI ORAL SOL 0.1% 60ML 1": 4 / 60,
    "RYKINDO VIAL DRY IM 25MG 1": 1 / 14,
    "RYKINDO VIAL DRY IM 37.5MG 1": 1 / (14 * 1.5),
    "RYKINDO VIAL DRY IM 50MG 1": 1 / (14 * 2),
    "RISPERIDONE ORAL SOL 30MG 30ML 1": 4 / 30,
}


df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["FORM"] = df["PACKAGE"].map(D_FORM)
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

for index, value in D_INDEX.items():
    mask = (df["PACKAGE"] == index) & (df["UNIT"] == "PTD")
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / value

r = CHPA(df, name="利培酮", date_column="DATE", period_interval=3)
r.plot_overall_performance_dual(index="FORM", unit_change="百万", width=15, height=6)

condition_meth = "[MOLECULE] in ('METHOTREXATE|甲氨蝶呤')"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_meth
df = pd.read_sql(sql=sql, con=engine)
print(df["PACKAGE"].unique())

D_FORM = {
    "METHOTREXATE INFUSION VLS 1G 10ML 1":
    "METHOTREXATE VIAL IV 1G 10ML 5"
    "METHOTREXATE VIAL 500MG 20ML 10"
    "MEI SU SHENG VIAL 1G 10ML 1"
    "METHOTREXATE VIAL 500MG 20ML 1"
    "METHOTREXATE VIAL DRY 100MG 1"
    "METHOTREXATE VIAL DRY 5MG 1"
    "METHOTREXATE VIAL DRY 1G 1"
    "METHOTREXATE (MTX) VIAL DRY 50MG 1"
    "METHOTREXATE TAB 2.5MG 16"
    "METHOTREXATE TAB 2.5MG 100"
    "METHOTREXATE VIAL 50MG 2ML 1"
    "LANG JIE TAB 2.5MG 18"
    "LANG JIE TAB 2.5MG 16"
    "METOJECT SYRINGE 10MG 0.2ML 1"
    "METHOTREXATE AMP DRY 5MG 1"
    "METHOTREXATE (MTX) AMP DRY 5MG 1"
}
