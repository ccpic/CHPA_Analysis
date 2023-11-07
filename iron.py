from CHPA2 import CHPA, convert_std_volume, extract_strength
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = "([TC III] in ('B03A HAEMATINICS,IRON & COMBS|补血药，铁剂和所有联合用药'))"
sql = "SELECT * FROM " + table_name + " WHERE " + condition

df = pd.read_sql(sql=sql, con=engine)


df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)

mask = df["PACKAGE"].str.contains(" AMP | VIAL | DRY | IV | INFUSION ")
df.loc[mask, "CLASS"] = "静脉铁"
df["CLASS"].fillna("口服铁", inplace=True)


# IQVIA原数据通用名只有二价铁/三价铁，并且中文通用名错误，此处进行归类和修正

mask = (df["MOLECULE"] == "多糖铁复合物") & (df["STRENGTH"] == "500MG")
df.loc[mask, "MOLECULE"] = "二异麦芽糖铁"
mask = (df["MOLECULE"] == "多糖铁复合物") & (df["CLASS"] == "静脉铁")
df.loc[mask, "MOLECULE"] = "蔗糖铁"
mask = df["PRODUCT"] == "IRON PROTEINSUCCIN (JY5)"
df.loc[mask, "MOLECULE"] = "蛋白琥珀酸铁"
mask = (df["MOLECULE"] == "富马酸亚铁") & (df["STRENGTH"] == "150MG")
df.loc[mask, "MOLECULE"] = "多糖铁复合物"

mask = (df["PRODUCT"].str.contains("SUCCINATE")) | (
    df["PRODUCT"].isin(["SU LI FEI (JNG)", "LI FEI LONG (H3U)"])
)
df.loc[mask, "MOLECULE"] = "琥珀酸亚铁"
mask = df["PRODUCT"].str.contains("FUMARATE")
df.loc[mask, "MOLECULE"] = "富马酸亚铁"
mask = df["PRODUCT"].str.contains("LACTATE") | (
    df["PRODUCT"].isin(["LA KE FEI (TGD)", "DAN ZHU (TAJ)", "TIE XIN (JFH)"])
)
df.loc[mask, "MOLECULE"] = "乳酸亚铁"
mask = df["PRODUCT"].str.contains("GLUCONATE") | (
    df["PRODUCT"].isin(["XU TAI (ZJ&)", "XUE YI (HT8)"])
)
df.loc[mask, "MOLECULE"] = "葡萄糖酸亚铁"
mask = (df["MOLECULE"] == "富马酸亚铁") & (df["PRODUCT"].str.contains("SULFATE"))
df.loc[mask, "MOLECULE"] = "硫酸亚铁"


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "蔗糖铁", "100MG", 1)
convert_std_volume(df, "MOLECULE", "蔗糖铁", "200MG", 2)
convert_std_volume(df, "MOLECULE", "多糖铁复合物", "150MG", 1)
convert_std_volume(df, "MOLECULE", "右旋糖酐铁", "100MG", 1)
convert_std_volume(df, "MOLECULE", "右旋糖酐铁", "50MG", 0.5)
convert_std_volume(df, "MOLECULE", "右旋糖酐铁", "25MG", 0.25)
convert_std_volume(df, "MOLECULE", "蛋白琥珀酸铁", "40MG", 1)
convert_std_volume(df, "MOLECULE", "富马酸亚铁", "100MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "富马酸亚铁", "0.1G", 1 / 4)
convert_std_volume(df, "MOLECULE", "富马酸亚铁", "200MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "富马酸亚铁", "0.2G", 1 / 2)
convert_std_volume(df, "MOLECULE", "富马酸亚铁", "0.3G", 2 / 3)
convert_std_volume(df, "MOLECULE", "富马酸亚铁", "250MG", 2.5 / 4)
convert_std_volume(df, "MOLECULE", "富马酸亚铁", "15MG", 1 / 30)
convert_std_volume(df, "MOLECULE", "琥珀酸亚铁", "100MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "琥珀酸亚铁", "200MG", 1)
convert_std_volume(df, "MOLECULE", "琥珀酸亚铁", "30MG", 1 / 5)
convert_std_volume(df, "MOLECULE", "乳酸亚铁", "150MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "乳酸亚铁", "100MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "乳酸亚铁", "0.1G", 1 / 3)
convert_std_volume(df, "MOLECULE", "乳酸亚铁", "900MG", 3)
convert_std_volume(df, "MOLECULE", "乳酸亚铁", "1.8G", 6)
convert_std_volume(df, "MOLECULE", "复方硫酸亚铁叶酸", "50MG", 1 / 8)
convert_std_volume(df, "MOLECULE", "硫酸亚铁", "300MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "硫酸亚铁", "0.3G", 1 / 2)
convert_std_volume(df, "MOLECULE", "硫酸亚铁", "450MG", 1)
convert_std_volume(df, "MOLECULE", "葡萄糖酸亚铁", "300MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "葡萄糖酸亚铁", "400MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "葡萄糖酸亚铁", "0.3G", 1 / 2)
convert_std_volume(df, "MOLECULE", "葡萄糖酸亚铁", "100MG", 1 / 8)
convert_std_volume(df, "MOLECULE", "复方枸橼酸铁铵", "100MG", 2)
convert_std_volume(df, "MOLECULE", "复方枸橼酸铁铵", "120MG", 2.4)
convert_std_volume(df, "MOLECULE", "二维亚铁", "415MG", 1 / 3)
convert_std_volume(df, "PACKAGE", "YU NING TAB FLM CTD 36", None, 1 / 6)
convert_std_volume(df, "PACKAGE", "YU NING TAB FLM CTD 48", None, 1 / 6)
convert_std_volume(df, "PACKAGE", "AMMONIUM FERRIC CI SYR 100ML 1", None, 2)
convert_std_volume(df, "PACKAGE", "YONGSHENG XUEDA SYR 120ML 1", None, 2.4)
# df.to_excel("test.xlsx")
print(df)

r = CHPA(df, name="铁剂市场", date_column="DATE", period_interval=3)

r.plot_overall_performance(index="CLASS", unit_change="百万")
r.plot_overall_performance(index="CLASS", unit="PTD", unit_change="百万")

r.plot_overall_performance(index="CLASS", unit_change="百万", period="QTR")
r.plot_overall_performance(index="CLASS", unit_change="百万", unit="PTD", period="QTR")


df2 = df[df["CLASS"] == "口服铁"]
r = CHPA(df2, name="口服铁剂市场", date_column="DATE", period_interval=3)

r.plot_size_diff(
    index="MOLECULE",
    unit="Value",
    unit_change="百万",
)

r.plot_size_diff(
    index="MOLECULE",
    unit="PTD",
    unit_change="百万",
)

r.plottable_latest(index="MOLECULE", unit="Value", focus="琥珀酸亚铁", hue=None)
r.plottable_latest(index="MOLECULE", unit="PTD", focus="琥珀酸亚铁", hue=None)

r.plot_share_trend(index="MOLECULE", unit="Value")
r.plot_share_trend(index="MOLECULE", unit="PTD")

r.plot_size_diff(
    index="PRODUCT",
    unit="Value",
    unit_change="百万",
    label_limit=10,
)

r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="百万",
    label_limit=10,
)

r.plottable_latest(
    index="PRODUCT", unit="Value", focus="SU LI FEI (JNG)", hue="CORPORATION"
)
r.plottable_latest(
    index="PRODUCT", unit="PTD", focus="SU LI FEI (JNG)", hue="CORPORATION"
)

r.plot_share_trend(index="PRODUCT", unit="Value")
r.plot_share_trend(index="PRODUCT", unit="PTD")


df3 = df[df["PRODUCT"] == "SU LI FEI (JNG)"]
r = CHPA(df3, name="速力菲", date_column="DATE", period_interval=3)

r.plottable_latest(index="PACKAGE", unit="Value")
r.plottable_latest(index="PACKAGE", unit="PTD")
