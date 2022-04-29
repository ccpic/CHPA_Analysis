from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = "[TC IV] in ('A10N1 DPP-IV INH A-DIAB PLAIN|DPP-IV（二肽基肽酶IV）抑制剂，单用(A10B6)')"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = (
    (df["PRODUCT"].str.split("|").str[0])
    + "（"
    + df["PRODUCT"].str.split("|").str[1].str[-3:]
    + "）"
)
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)

# mask = df["MOLECULE"] == "阿卡波糖"
# df.loc[mask, "MOLECULE"] = "阿卡波糖片剂"

vbp_list = ["维格列汀", '沙格列汀']
mask = df["MOLECULE"].isin(vbp_list)
df.loc[mask, "VBP"] = "带量品种"
mask = df["MOLECULE"].isin(vbp_list) == False
df.loc[mask, "VBP"] = "非带量品种"


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "沙格列汀", "2.5MG", 0.5)
convert_std_volume(df, "MOLECULE", "卡格列净", "25MG", 3)

r = chpa(df, name="DPP4抑制剂单方市场")
r.plot_overall_performance(dimension="VBP")

r.plot_overall_performance(
    dimension="VBP",
    unit="Volume (Std Counting Unit)",
)

