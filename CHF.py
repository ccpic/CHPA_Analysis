from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

# ARNI市场

condition_arni = "MOLECULE = 'SACUBITRIL+VALSARTAN|沙库巴曲缬沙坦'"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_arni
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])

convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "100MG", 0.5)
convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "50MG", 0.25)

df_arni = df.copy()

r = chpa(df, name="ARNI市场")

r.plot_overall_performance(
    dimension="MOLECULE",
    width=15,
    height=6,
)

r.plot_overall_performance(
    dimension="MOLECULE",
    unit="Volume (Std Counting Unit)",
    width=15,
    height=6,
)

# RAAS单方市场
condition_raasi_plain = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    # "'C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"
    # "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药')"
)

sql = "SELECT * FROM " + table_name + " WHERE " + condition_raasi_plain
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")

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

D_MAP = {
    "缬沙坦": "缬沙坦",
    "厄贝沙坦": "厄贝沙坦",
    "氯沙坦钾": "氯沙坦",
    "阿利沙坦": "阿利沙坦",
    "贝那普利": "贝那普利",
    "奥美沙坦": "奥美沙坦",
    "替米沙坦": "替米沙坦",
}

df["MOLECULE"] = df["MOLECULE"].map(D_MAP).fillna("其他")

df_raasi = df.copy()

r = chpa(df, name="RAAS平片(ARB+ACEI)市场")

r.plot_overall_performance(
    dimension="MOLECULE",
    width=15,
    height=6,
    sorter=["阿利沙坦", "厄贝沙坦", "氯沙坦", "缬沙坦", "奥美沙坦", "贝那普利", "替米沙坦", "其他"],
)


# Beta单方市场
condition_beta = "[TC III] in ('C07A BETA BLOCKING AGENT PLN|β受体阻断剂，单用')"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_beta
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")

D_MAP = {
    "美托洛尔": "美托洛尔",
    "艾司洛尔": "艾司洛尔",
    "比索洛尔": "比索洛尔",
    "阿罗洛尔": "阿罗洛尔",
    "拉贝洛尔": "拉贝洛尔",
}

df["MOLECULE"] = df["MOLECULE"].map(D_MAP).fillna("其他")

df_beta = df.copy()

r = chpa(df, name="β受体阻断剂市场")

r.plot_overall_performance(
    dimension="MOLECULE",
    width=15,
    height=6,
    sorter=["美托洛尔", "艾司洛尔", "比索洛尔", "阿罗洛尔", "拉贝洛尔", "其他"],
)



# 伊伐布雷定市场
condition_beta = "MOLECULE = 'IVABRADINE|伊伐布雷定'"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_beta
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")

df_iva = df.copy()

r = chpa(df, name="伊伐布雷定市场")

r.plot_overall_performance(
    dimension="MOLECULE",
    width=15,
    height=6,
)

# SGLT2市场
condition_sglt2 = "[TC IV] in ('A10P1 SGLT2 INHIB A-DIAB PLAIN|钠-葡萄糖协同转运蛋白2抑制剂，单用')"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_sglt2
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")

df_sglt2 = df.copy()

r = chpa(df, name="SGLT2市场")

r.plot_overall_performance(
    dimension="MOLECULE",
    width=15,
    height=6,
)

# MRA市场
condition_mra = "MOLECULE in ('SPIRONOLACTONE|螺内酯','FINERENONE|非奈利酮')"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_mra
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")

df_mra = df.copy()

r = chpa(df, name="MRA市场")

r.plot_overall_performance(
    dimension="MOLECULE",
    width=15,
    height=6,
)

df_arni["AMOUNT"] = df_arni["AMOUNT"] * 0.6
df_arni["CLASS"] = "ARNI"

df_raasi["AMOUNT"] = df_raasi["AMOUNT"] * 0.05
df_raasi["CLASS"] = "RAAS平片(ARB+ACEI)"

df_beta["AMOUNT"] = df_beta["AMOUNT"] * 0.45
df_beta["CLASS"] = "β受体阻断剂"

df_mra["AMOUNT"] = df_mra["AMOUNT"] * 0.8
df_mra["CLASS"] = "MRA"

df_sglt2["AMOUNT"] = df_sglt2["AMOUNT"] * 0.25
df_sglt2["CLASS"] = "SGLT2"

df_iva["AMOUNT"] = df_iva["AMOUNT"] * 1
df_iva["CLASS"] = "伊伐布雷定"

# df_arni_rassi = pd.concat([df_arni, df_raasi])
# r = chpa(df_arni_rassi, name="ARNI+RAAS市场")

# r.plot_overall_performance(
#     dimension="CLASS",
#     width=15,
#     height=6,
#     unit="Volume (Std Counting Unit)",
# )

df_chf = pd.concat([df_arni, df_raasi, df_beta, df_mra, df_sglt2, df_iva])

r = chpa(df_chf, name="慢性心衰市场")
r.plot_overall_performance(
    dimension="CLASS",
    width=15,
    height=6,
)

r.plot_group_size_diff(
    index="PRODUCT",
    date=[r.latest_date()],
    dimension=None,
    column=None,
    adjust_scale=0.01,
    series_limit=30,
    showLabel=True,
    unit="Value",
    labelLimit=15,
)