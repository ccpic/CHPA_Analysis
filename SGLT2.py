from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = "[TC III] in ('A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂')"
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

vbp_list = ["恩格列净", "卡格列净"]
mask = df["MOLECULE"].isin(vbp_list)
df.loc[mask, "VBP"] = "带量品种"
mask = df["MOLECULE"].isin(vbp_list) == False
df.loc[mask, "VBP"] = "非带量品种"

# show_list = []
# mask = df["MOLECULE"].isin(show_list) == False
# df.loc[mask, "MOLECULE"] = "其他品种"

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "恩格列净", "25MG", 2.5)
convert_std_volume(df, "MOLECULE", "卡格列净", "25MG", 3)

r = chpa(df, name="SGLT2抑制剂市场")
r.plot_overall_performance(dimension="VBP")
r.plot_overall_performance(
    dimension="VBP",
    unit="Volume (Std Counting Unit)",
)