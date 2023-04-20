from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = "[TC IV] in ('A10N1 DPP-IV INH A-DIAB PLAIN|DPP-IV（二肽基肽酶IV）抑制剂，单用(A10B6)')"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)


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

# mask = df["MOLECULE"] == "阿卡波糖"
# df.loc[mask, "MOLECULE"] = "阿卡波糖片剂"

vbp_list = ["维格列汀", "沙格列汀"]
mask = df["MOLECULE"].isin(vbp_list)
df.loc[mask, "VBP"] = "VBP品种"
mask = df["MOLECULE"].isin(vbp_list) == False
df.loc[mask, "VBP"] = "非VBP品种"


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])

convert_std_volume(df, "MOLECULE", "沙格列汀", "2.5MG", 0.5)
convert_std_volume(df, "MOLECULE", "维格列汀", "50MG", 0.5)

r = chpa(df, name="DPP4抑制剂单方市场")

# r.plot_overall_performance(
#     dimension="MOLECULE", sorter=["西格列汀", "利格列汀", "沙格列汀", "维格列汀", "阿格列汀"]
# )

# r.plot_overall_performance(
#     dimension="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     sorter=["西格列汀", "利格列汀", "沙格列汀", "维格列汀", "阿格列汀"],
# )

# r.plot_overall_performance(dimension="VBP")

# r.plot_overall_performance(
#     dimension="VBP",
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
#     labelLimit=7,
# )
# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.03,
#     series_limit=250,
#     showLabel=True,
#     labelLimit=10,
#     unit="Volume (Std Counting Unit)",
# )

r.plot_share_trend(
    dimension="MOLECULE",
    column=None,
    series_limit=10,
)
r.plot_share_trend(
    dimension="MOLECULE",
    column=None,
    unit="Volume (Std Counting Unit)",
    series_limit=10,
)

r.plot_share_trend(
    dimension="PRODUCT",
    column=None,
    series_limit=10,
)
r.plot_share_trend(
    dimension="PRODUCT",
    column=None,
    unit="Volume (Std Counting Unit)",
    series_limit=10,
)