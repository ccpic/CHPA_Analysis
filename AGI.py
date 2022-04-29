from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = "[TC III] in ('A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)')"
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

mask = df["MOLECULE"] == "阿卡波糖"
df.loc[mask, "MOLECULE"] = "阿卡波糖片剂"

vbp_list = ["阿卡波糖片剂"]
mask = df["MOLECULE"].isin(vbp_list)
df.loc[mask, "VBP"] = "带量品种"
mask = df["MOLECULE"].isin(vbp_list) == False
df.loc[mask, "VBP"] = "非带量品种"


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "阿卡波糖片剂", "100MG", 2)
convert_std_volume(df, "MOLECULE", "卡格列净", "25MG", 3)

r = chpa(df, name="α糖苷酶抑制剂市场")
r.plot_overall_performance(dimension="MOLECULE")
r.plot_overall_performance(
    dimension="MOLECULE",
    unit="Volume (Std Counting Unit)",
)

